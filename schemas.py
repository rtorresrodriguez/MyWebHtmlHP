from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nombre: str
    correo: str

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    correo: str

    class Config:
        from_attributes = True  # ✅ Esto es lo correcto en Pydantic V2
