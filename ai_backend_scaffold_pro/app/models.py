from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True)
    password_hash = Column(String(255))

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    original_path = Column(String(255), nullable=False)
    result_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project")

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    status = Column(String(32), default="queued")
    params = Column(Text)  # JSON string
    result_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Preset(Base):
    __tablename__ = "presets"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, nullable=False)
    params = Column(Text)  # JSON dict of operations
    created_at = Column(DateTime, default=datetime.utcnow)
