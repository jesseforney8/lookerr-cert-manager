from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] 

class Device(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    ip_address: Mapped[str] = mapped_column(unique=True)
    os: Mapped[str]
    device_user: Mapped[str]
    device_password: Mapped[str]
    filepath: Mapped[str]
    ssl_cert: Mapped[str]