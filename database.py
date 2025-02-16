import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 📌 Asegurar que la carpeta static existe
if not os.path.exists("static"):
    os.makedirs("static")

DATABASE_URL = "sqlite:///./static/test.db"  # 📌 Guardar la base de datos en static/

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()