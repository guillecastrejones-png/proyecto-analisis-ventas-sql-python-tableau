import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
load_dotenv('.env')
DB_USER=os.getenv('DB_USER'); DB_PASS=os.getenv('DB_PASS')
DB_HOST=os.getenv('DB_HOST','localhost'); DB_PORT=os.getenv('DB_PORT','5432')
DB_NAME=os.getenv('DB_NAME')
url=f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print("DB URL:", url)
engine=create_engine(url)
with engine.connect() as conn:
    r = conn.execute(text("SELECT 'ok' AS status;"))
    print("Test query result:", r.fetchone())
