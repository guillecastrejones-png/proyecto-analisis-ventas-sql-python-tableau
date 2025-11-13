from dotenv import load_dotenv
import os
import psycopg2

# Fuerza la carga explicita desde el .env en el directorio actual
load_dotenv('.env')

print("LEÍDO .env?", os.path.exists('.env'))
print("DB_HOST =", os.getenv("DB_HOST"))
print("DB_PORT =", os.getenv("DB_PORT"))
print("DB_NAME =", os.getenv("DB_NAME"))
print("DB_USER =", os.getenv("DB_USER"))

try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST") if os.getenv("DB_HOST") else None,
        port=os.getenv("DB_PORT") if os.getenv("DB_PORT") else None,
        dbname=os.getenv("DB_NAME") if os.getenv("DB_NAME") else None,
        user=os.getenv("DB_USER") if os.getenv("DB_USER") else None,
        password=os.getenv("DB_PASS") if os.getenv("DB_PASS") else None
    )
    params = conn.get_dsn_parameters()
    print("Conectado — parámetros de la conexión:", params)
    conn.close()
    print("CONEXIÓN OK")
except Exception as e:
    print("ERROR al conectar:", e)
