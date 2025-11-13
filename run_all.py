#!/usr/bin/env python3
"""
run_all.py
Script reproducible para:
- cargar CSV -> PostgreSQL (dos métodos: pandas.to_sql o COPY)
- ejecutar queries (validation + analysis) desde carpetas .sql
- exportar resultados a carpeta outputs/
- generar un Excel resumen
"""
import os
import glob
import logging
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# --- Config / paths ---
BASE = Path(__file__).resolve().parent
DATA_DIR = BASE / "data"
OUT_DIR = BASE / "outputs"            # cambiado a "outputs" (más lógico)
Q_VAL_DIR = BASE / "queries_validation"
Q_ANA_DIR = BASE / "queries_analysis"
LOG_DIR = BASE / "run_logs"
NOTEBOOKS_DIR = BASE / "notebooks"

OUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# --- Logging ---
logging.basicConfig(
    filename=str(LOG_DIR / "run_all.log"),
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

# --- Load env ---
load_dotenv(BASE / ".env")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
LOAD_METHOD = os.getenv("LOAD_METHOD", "copy")  # 'pandas' or 'copy'

if not all([DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME]):
    logging.error("Faltan variables de entorno DB_*. Comprueba .env")
    raise SystemExit("Faltan variables de entorno DB_*. Comprueba .env")

DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)

# --- Helper: listar CSVs de data dir ---
def list_csvs():
    if not DATA_DIR.exists():
        return []
    return sorted(list(DATA_DIR.glob("*.csv")))

# --- Method A: pandas.to_sql (reemplaza/crea tablas) ---
def load_with_pandas():
    logging.info("Cargando CSVs con pandas.to_sql (if_exists='replace') ...")
    for csv_path in list_csvs():
        table_name = csv_path.stem
        logging.info(f" -> {csv_path.name} -> tabla: {table_name}")
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, engine, if_exists="replace", index=False)
    logging.info("Carga con pandas finalizada.")

# --- Method B: COPY (recomendado si ya tienes esquema) ---
def load_with_copy():
    logging.info("Cargando CSVs con COPY (psycopg2) ...")
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    conn.autocommit = True
    cur = conn.cursor()
    for csv_path in list_csvs():
        table_name = csv_path.stem
        logging.info(f" -> {csv_path.name} -> tabla: {table_name}")
        cur.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables
                WHERE table_name = %s
            );
        """, (table_name,))
        exists = cur.fetchone()[0]
        if not exists:
            logging.warning(f"Tabla {table_name} NO existe en la BD. Saltando. (Crea la tabla primero o usa LOAD_METHOD=pandas)")
            continue
        with open(csv_path, "r", encoding="utf-8") as f:
            try:
                cur.copy_expert(sql.SQL("COPY {} FROM STDIN WITH CSV HEADER").format(sql.Identifier(table_name)), f)
                logging.info(f"  COPY OK -> {table_name}")
            except Exception as e:
                logging.exception(f"  ERROR en COPY para {table_name}: {e}")
    cur.close()
    conn.close()
    logging.info("Carga con COPY finalizada.")

# --- Ejecutar .sql files y exportar resultados a CSV ---
def run_queries_and_export(sql_dir: Path, prefix: str = ""):
    if not sql_dir.exists():
        logging.warning(f"No existe directorio {sql_dir}")
        return
    sql_files = sorted(sql_dir.glob("*.sql"))
    logging.info(f"Ejecutando {len(sql_files)} queries en {sql_dir}")
    for sql_file in sql_files:
        try:
            qname = sql_file.stem
            logging.info(f" -> Ejecutando {sql_file.name}")
            sql_text = sql_file.read_text()
            df = pd.read_sql_query(sql_text, engine)
            out_name = f"{prefix}{qname}.csv"
            out_path = OUT_DIR / out_name
            df.to_csv(out_path, index=False)
            logging.info(f"    Exportado: {out_name} ({len(df)} filas)")
        except Exception as e:
            logging.exception(f"    ERROR ejecutando {sql_file.name}: {e}")

# --- Generar summary Excel con hojas ejemplo ---
def make_excel_summary():
    logging.info("Generando summary_analysis.xlsx ...")
    excel_path = OUT_DIR / "summary_analysis.xlsx"
    try:
        with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
            for csv_path in list_csvs():
                try:
                    sheet_name = csv_path.stem[:31]
                    df = pd.read_csv(csv_path)
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                except Exception as e:
                    logging.exception(f"  No pude escribir sheet {csv_path.name}: {e}")
            for out_csv in sorted(OUT_DIR.glob("*.csv")):
                try:
                    name = out_csv.stem[:31]
                    df = pd.read_csv(out_csv)
                    df.to_excel(writer, sheet_name=name, index=False)
                except Exception:
                    pass
        logging.info("Excel generado.")
    except Exception as e:
        logging.exception(f"Error generando Excel: {e}")

# --- Main ---
def main():
    logging.info("RUN ALL: inicio")
    logging.info(f"LOAD_METHOD={LOAD_METHOD}")

    if LOAD_METHOD == "pandas":
        load_with_pandas()
    else:
        load_with_copy()

    if Q_VAL_DIR.exists():
        run_queries_and_export(Q_VAL_DIR, prefix="val_")
    else:
        logging.warning("No existe carpeta queries_validation/")

    if Q_ANA_DIR.exists():
        run_queries_and_export(Q_ANA_DIR, prefix="ana_")
    else:
        logging.warning("No existe carpeta queries_analysis/")

    make_excel_summary()
    logging.info("RUN ALL: FINISHED. Revisa carpeta outputs/ y run_logs/run_all.log")

if __name__ == "__main__":
    main()
