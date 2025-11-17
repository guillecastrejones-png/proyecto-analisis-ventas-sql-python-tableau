#  Proyecto de Análisis de Ventas — SQL · Python · Jupyter · Tableau

**Autor:** Guillermo Castrejón**
**Rol:** Analista de Datos Junior / Administrador de Bases de Datos Junior**

---

##  Descripción del Proyecto

Este proyecto cubre **todo el ciclo de vida del dato**, desde su modelado en SQL hasta la creación de un dashboard interactivo en Tableau.

Incluye:

* Modelado y creación de una base de datos relacional
* Carga de datos desde CSV
* Validaciones de integridad
* Pipeline ETL reproducible con Python
* Cálculo de KPIs
* Análisis exploratorio en Jupyter Notebook
* Dashboard interactivo en Tableau Public

El objetivo es demostrar mi capacidad para trabajar como **Data Analyst Junior**, elaborando proyectos completos, ordenados y orientados a negocio.

---

##  Estructura del Proyecto


proyecto-analisis-ventas-sql-python-tableau/
│
├── data/                     # Datos originales (CSV)
├── queries_validation/       # Validaciones SQL
├── queries_analysis/         # Consultas analíticas SQL
├── notebooks/                # EDA con Jupyter Notebook
├── outputs/                  # Resultados generados por el pipeline
├── run_logs/                 # Registros de ejecución del ETL
├── run_all.py                # Script ETL principal
└── README.md                 # Documentación

---

##  Modelo Relacional

Tablas:

* **customers** → información del cliente
* **orders** → pedidos
* **products** → productos y categorías
* **order_items** → detalle del pedido + columna calculada `total`

Relaciones:

customers 1 ── n orders
orders    1 ── n order_items
products  1 ── n order_items


---

##  Tecnologías Utilizadas

* **PostgreSQL / SQL** — creación del esquema, validaciones, consultas
* **Python (Pandas)** — ETL, merges, KPIs, reportería
* **Jupyter Notebook** — análisis exploratorio
* **Tableau Public** — visualización interactiva
* **Git & GitHub** — versionado y documentación

---

##  KPIs y Análisis Realizado

* Ventas totales
* Ventas por ciudad
* Ventas por categoría
* Ventas por mes
* Ranking de productos
* Top clientes
* Ticket medio
* Comparativa por canal (online vs tienda)

---

## Pipeline ETL (Python)

El script **`run_all.py`** realiza:

1. Carga de CSV desde `/data/`
2. Validación de estructura
3. Inserción en PostgreSQL
4. Cálculo de totales y KPIs
5. Exportación de resultados a `/outputs/`
6. Generación de logs en `/run_logs/`

---

## ▶ Cómo reproducir el proyecto

### 1. Crear entorno virtual

bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependencias

bash
pip install -r requirements.txt


### 3. Ejecutar el ETL

bash
python run_all.py


Los resultados aparecerán en:
/outputs`
/run_logs`

---

##  Dashboard en Tableau

**Dashboard publicado en Tableau Public:**
*(Añade aquí tu enlace exacto de Tableau)*

Incluye visualizaciones de:

* Ventas por ciudad
* Ventas por categoría
* Top productos
* Evolución mensual
* KPI principal de ventas

---

##  Sobre el autor

Soy **Guillermo Castrejón**, Analista de Datos Junior en formación y desarrollo continuo.
Actualmente estoy construyendo un portfolio orientado a SQL, Python y visualización con Tableau, buscando una oportunidad para aprender y crecer en el sector.

---

##  Contacto

Email: **[guille.castrejon.es@gmail.com](mailto:guille.castrejon.es@gmail.com)**
LinkedIn: *(tu enlace aquí)*

---


