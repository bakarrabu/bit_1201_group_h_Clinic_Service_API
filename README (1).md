# 🏥 Group H — Clinic Service API for Searching Local Clinic Services

![FastAPI](https://img.shields.io/badge/FastAPI-0.103.2-009688?style=flat&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=flat&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791?style=flat&logo=postgresql)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![SDG3](https://img.shields.io/badge/SDG-3%20Good%20Health-4C9F38?style=flat)

> A FastAPI-based REST API to help people in Sierra Leone find, review, and book appointments at local clinics. Built for PROG315 — Object-Oriented Programming 2 at Limkokwing University of Creative Technology, Sierra Leone.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [SDG Alignment](#sdg-alignment)
- [Team](#team)

---

## 📖 Project Overview

The **Clinic Service API** is a professional-grade REST API that addresses a real problem in Sierra Leone — people struggle to find reliable clinics, read reviews, and book appointments. This system provides a digital directory of local clinics with full CRUD operations, JWT security, appointment booking, and advanced analytics.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **Authentication** | Register and login with JWT token security |
| 🏥 **Clinics** | Create, read, update, delete clinics |
| 🩺 **Services** | Manage services offered by each clinic |
| ⭐ **Reviews** | Patients can write, update and delete reviews |
| 📅 **Appointments** | Book, confirm, cancel doctor appointments |
| 📊 **Analytics** | Real-time statistics using SQL aggregation |
| 📧 **Email Notifications** | Confirmation emails on registration |
| 🎨 **Dashboard UI** | Separate admin and patient web interfaces |
| 📄 **Documentation** | Swagger UI and ReDoc auto-generated docs |

---

## 🛠️ Tech Stack

- **Backend Framework** — FastAPI (Python)
- **Database** — PostgreSQL
- **ORM** — SQLAlchemy
- **Authentication** — JWT (JSON Web Tokens) + bcrypt
- **Email** — SMTP via Gmail
- **Documentation** — Swagger UI (`/docs`) + ReDoc (`/redoc`)
- **Frontend** — HTML, CSS, JavaScript (vanilla)

---

## 📁 Project Structure

```
Client API/
├── main.py              # Application entry point, router registration
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic request/response schemas
├── database.py          # Database connection and session
├── auth.py              # Register, login, get current user
├── auth_handler.py      # JWT token creation and verification
├── clinics.py           # Clinic CRUD endpoints
├── services.py          # Service CRUD endpoints
├── reviews.py           # Review CRUD endpoints
├── appointments.py      # Appointment booking endpoints
├── stats.py             # Analytics & statistics endpoints
├── email_service.py     # Email notification service
├── .env                 # Environment variables (not in GitHub)
├── .env.example         # Example environment file
├── index.html           # Landing page (choose admin or patient)
├── dashboard-admin.html # Admin portal
├── dashboard-user.html  # Patient portal
└── requirements.txt     # Python dependencies
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- PostgreSQL installed and running
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/clinic-service-api.git
cd clinic-service-api
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

**Windows:**
```bash
.venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```env
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=clinic_db
SMTP_EMAIL=your_gmail@gmail.com
SMTP_PASSWORD=your_gmail_app_password
```

> **Note:** For Gmail, use an App Password from [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

### 5. Create the Database

Open pgAdmin or psql and run:

```sql
CREATE DATABASE clinic_db;
```

### 6. Run the Application

```bash
uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`

---

## 📚 API Documentation

Once the server is running, access the documentation at:

| Documentation | URL |
|---|---|
| **Swagger UI** | http://127.0.0.1:8000/docs |
| **ReDoc** | http://127.0.0.1:8000/redoc |
| **OpenAPI JSON** | http://127.0.0.1:8000/openapi.json |

---

## 🔗 API Endpoints

### Authentication
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/auth/register` | Register new user or admin | No |
| POST | `/auth/login` | Login and get JWT token | No |
| GET | `/auth/me` | Get current user profile | Yes |

### Clinics
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/clinics/` | List all clinics | No |
| GET | `/clinics/{id}` | Get one clinic | No |
| POST | `/clinics/` | Create clinic | Admin only |
| PUT | `/clinics/{id}` | Update clinic | Admin only |
| DELETE | `/clinics/{id}` | Delete clinic | Admin only |

### Services
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/services/` | List all services | No |
| GET | `/services/{id}` | Get one service | No |
| POST | `/services/{clinic_id}/services` | Add service to clinic | Admin only |
| PUT | `/services/{id}` | Update service | Admin only |
| DELETE | `/services/{id}` | Delete service | Admin only |

### Reviews
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/reviews/` | List all reviews | No |
| GET | `/reviews/{id}` | Get one review | No |
| POST | `/reviews/` | Submit a review | Yes |
| PUT | `/reviews/{id}` | Update your review | Yes |
| DELETE | `/reviews/{id}` | Delete your review | Yes |

### Appointments
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/appointments/` | Book appointment | Yes |
| GET | `/appointments/` | My appointments | Yes |
| GET | `/appointments/{id}` | Get one appointment | Yes |
| PUT | `/appointments/{id}` | Update appointment | Yes |
| PUT | `/appointments/{id}/cancel` | Cancel appointment | Yes |
| DELETE | `/appointments/{id}` | Delete appointment | Admin only |

### Analytics & Statistics ⭐ New Feature
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/stats/summary` | Total counts and average rating | No |
| GET | `/stats/top-clinics` | Clinics ranked by rating | No |
| GET | `/stats/rating-distribution` | Star rating breakdown | No |
| GET | `/stats/clinics-per-city` | Clinics grouped by city | No |

---

## 🔐 Authentication

This API uses **JWT (JSON Web Token)** authentication.

### How to authenticate in Swagger UI:

1. Go to `POST /auth/login`
2. Enter your email and password
3. Copy the `access_token` from the response
4. Click the **Authorize** button at the top of Swagger UI
5. Enter your email and password and click **Authorize**

### User Roles:

| Role | Permissions |
|---|---|
| `user` | Read clinics, write reviews, book appointments |
| `admin` | Full access — manage clinics, services, appointments |

---

## 🌍 SDG Alignment

This project supports **UN Sustainable Development Goal 3 — Good Health and Well-Being**.

**How it helps Sierra Leone:**
- Patients can find clinics by city without walking around
- Reviews help patients choose quality healthcare
- Appointment booking reduces waiting time
- Analytics help government plan where to build new clinics
- Accessible to people in rural areas like Kenema, Bo, and Makeni

---

## 📦 Requirements

```
fastapi==0.103.2
uvicorn==0.22.0
sqlalchemy==2.0.50
psycopg2-binary==2.9.9
python-jose==3.4.0
passlib==1.7.4
bcrypt==4.2.1
python-dotenv==0.21.1
python-multipart==0.0.8
pydantic[email]==2.5.3
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 👥 Team

**Group H — PROG315 Object-Oriented Programming 2**
Limkokwing University of Creative Technology, Sierra Leone
Semester 4 — March 2026 to July 2026

**Examiner:** Amandus Benjamin Coker
**Submission Deadline:** Week 11

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Group H — Limkokwing University Sierra Leone

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.
```

---

*Built with ❤️ for Sierra Leone 🇸🇱*
