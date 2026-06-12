# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
import os

from database import Base, engine

import models
import auth
import clinics
import services
import reviews
import stats
import appointments

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Group H — Clinic Service API for Searching Local Clinic Services",
    description="""
## Clinic Service API for Searching Local Clinic Services

A FastAPI-based REST API to help people in **Sierra Leone** find, review and book appointments at local clinics.

### Features
- 🔐 **Authentication** — JWT token based security
- 🏥 **Clinics** — Find and manage clinics
- 🩺 **Services** — Clinic services and prices
- ⭐ **Reviews** — Patient reviews and ratings
- 📅 **Appointments** — Book doctor appointments
- 📊 **Analytics** — Statistics and insights

### SDG Alignment
This project supports **SDG 3 — Good Health and Well-Being** by helping people in Sierra Leone find quality healthcare.

**Group H — PROG315 — Limkokwing University Sierra Leone**
    """,
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json",
    contact={
        "name": "Group H — Limkokwing University Sierra Leone",
        "email": "salmakamara038@gmail.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(clinics.router, prefix="/clinics", tags=["Clinics"])
app.include_router(services.router, prefix="/services", tags=["Services"])
app.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
app.include_router(stats.router, prefix="/stats", tags=["Analytics & Statistics"])


# ── Serve HTML files directly from the browser ────────────────────────────────

@app.get("/docs", include_in_schema=False)
async def swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Group H — Clinic Service API Docs",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )

@app.get("/redoc", include_in_schema=False)
async def redoc_ui():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="Group H — Clinic Service API ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@latest/bundles/redoc.standalone.js",
    )

@app.get("/")
async def root():
    return FileResponse("index.html")

@app.get("/index.html")
async def index():
    return FileResponse("index.html")

@app.get("/dashboard-user.html")
async def user_dashboard():
    return FileResponse("dashboard-user.html")

@app.get("/dashboard-admin.html")
async def admin_dashboard():
    return FileResponse("dashboard-admin.html")

@app.get("/dashboard.html")
async def dashboard():
    return FileResponse("dashboard.html")
