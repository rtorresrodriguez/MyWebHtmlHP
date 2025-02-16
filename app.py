from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # ✅ Importar CORS
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import requests
import os

from database import SessionLocal, engine, Base
import models
import schemas
from datetime import datetime

# ✅ Crear la base de datos si no existe
Base.metadata.create_all(bind=engine)

# ✅ Inicializar la API
app = FastAPI()

# ✅ Configurar CORS para permitir solicitudes desde el frontend en Render
origins = [
    "https://mywebhtmlp.onrender.com",
    "http://127.0.0.1:5500",
    "http://localhost:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📌 Servir archivos estáticos
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ Ruta para probar si la API está funcionando
@app.get("/")
def home():
    return {"message": "¡Servidor en funcionamiento!"}

# 📌 Ruta para servir el HTML principal
@app.get("/")
def serve_home():
    return FileResponse("static/index.html")  # Asegúrate de que el HTML está en "static/"

# ✅ Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Ruta GET - Obtener todos los usuarios
@app.get("/usuarios/", response_model=list[schemas.UsuarioResponse])
def leer_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()

# ✅ Ruta POST - Agregar un usuario
@app.post("/usuarios/", response_model=schemas.UsuarioResponse)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = models.Usuario(nombre=usuario.nombre, correo=usuario.correo)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# ✅ Ruta GET con ID - Obtener un usuario por ID
@app.get("/usuarios/{usuario_id}", response_model=schemas.UsuarioResponse)
def leer_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# ✅ Ruta DELETE - Eliminar un usuario por ID
@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    return {"message": "Usuario eliminado correctamente"}

# ✅ Ruta para consumir una API externa (chistes)
@app.get("/random-joke/")
def obtener_chiste():
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="No se pudo obtener el chiste")
    return response.json()

# ✅ Ruta para obtener la hora actual
@app.get("/hora")
def obtener_hora():
    return {"hora_actual": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

# 📌 Documentación automática en Swagger (http://127.0.0.1:8000/docs)
