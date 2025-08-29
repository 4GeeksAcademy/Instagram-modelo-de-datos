from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, DateTime, ForeignKey, Enum as SAEnum, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum as py_enum

db = SQLAlchemy()


class InteractionType(py_enum.Enum):
    LIKE = "like"
    FAV = "fav"


class Usuario(db.Model):
    __tablename__ = "usuario"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    nombre: Mapped[str] = mapped_column(String(80), nullable=True)
    apellido: Mapped[str] = mapped_column(String(80), nullable=True)
    biografia: Mapped[str] = mapped_column(Text, nullable=True)
    imagen: Mapped[str] = mapped_column(String(255), nullable=True)
    sexo: Mapped[str] = mapped_column(String(20), nullable=True)

    posts = relationship("Post", back_populates="usuario", cascade="all, delete-orphan")
    interacciones = relationship("Interaccion", back_populates="usuario", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "biografia": self.biografia,
            "imagen": self.imagen,
            "sexo": self.sexo,
            "fecha_subscripcion": self.fecha_subscripcion.isoformat() if self.fecha_subscripcion else None,
        }


class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)
    fecha_creado: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    usuario = relationship("Usuario", back_populates="posts")
    archivos = relationship("Archivo", back_populates="post", cascade="all, delete-orphan")
    interacciones = relationship("Interaccion", back_populates="post", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "descripcion": self.descripcion,
            "usuario_id": self.usuario_id,
            "fecha_creado": self.fecha_creado.isoformat() if self.fecha_creado else None,
        }


class Archivo(db.Model):
    __tablename__ = "archivo"
    id: Mapped[int] = mapped_column(primary_key=True)
    file: Mapped[str] = mapped_column(String(255), nullable=False)  
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    post = relationship("Post", back_populates="archivos")

    def serialize(self):
        return {"id": self.id, "file": self.file, "post_id": self.post_id}


class Interaccion(db.Model):
    __tablename__ = "interaccion"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    tipo_interaccion: Mapped[InteractionType] = mapped_column(SAEnum(InteractionType), nullable=False)
    fecha: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    usuario = relationship("Usuario", back_populates="interacciones")
    post = relationship("Post", back_populates="interacciones")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "tipo_interaccion": self.tipo_interaccion.value if self.tipo_interaccion else None,
            "fecha": self.fecha.isoformat() if self.fecha else None,
        }
