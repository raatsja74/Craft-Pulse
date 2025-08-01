from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Tenant(Base):
    __tablename__ = 'tenants'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    users = relationship('User', back_populates='tenant')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    tenant = relationship('Tenant', back_populates='users')
    profile = relationship('UserProfile', uselist=False, back_populates='user')

class UserProfile(Base):
    __tablename__ = 'user_profiles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    q1 = Column(String)
    q2 = Column(String)
    q3 = Column(String)
    q4 = Column(String)
    q5 = Column(String)
    user = relationship('User', back_populates='profile')

class GeneratedContent(Base):
    __tablename__ = 'generated_content'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    content_type = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class ScheduledPost(Base):
    __tablename__ = 'scheduled_posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    platform = Column(String)
    content = Column(Text)
    scheduled_time = Column(DateTime)
    status = Column(String, default='pending')
