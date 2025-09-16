# fastapi_app/main.py

import os
import sys, os
from pathlib import Path
from dotenv import load_dotenv

# Make project root importable so "import django_project.settings" will work
BASE_DIR = Path(__file__).resolve().parent.parent  # project root (E:\...quizz_app_project)
print("DEBUG: BASE_DIR =", BASE_DIR)
print("DEBUG: sys.path before:", sys.path[:5])

sys.path.insert(0, str(BASE_DIR))
print("DEBUG: sys.path after:", sys.path[:5])

# Load .env from project root
load_dotenv(BASE_DIR / ".env")

# Point to your Django settings before importing models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")

# Now initialize Django
import django
django.setup()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import api  # import routers after django.setup()

app = FastAPI(title="Teach Education API")
app.include_router(api.router, prefix="/api")

# CORS - for dev set '*' or restrict to your frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Teach Education API running"}
