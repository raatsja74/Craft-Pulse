from fastapi import FastAPI
from .database import Base, engine
from .routers import profile, content

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Realtor Social Media AI")

app.include_router(profile.router)
app.include_router(content.router)
