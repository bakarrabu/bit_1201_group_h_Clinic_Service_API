# stats.py
# 📊 Advanced Analytics & Statistics Endpoint
# This uses SQL aggregation (AVG, COUNT, GROUP BY, subqueries) 
# - techniques beyond basic CRUD that show professional API design.

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, case
from typing import List, Optional

from database import get_db
import models
import schemas

router = APIRouter()


@router.get("/summary", response_model=schemas.SummaryStats)
def get_summary_stats(db: Session = Depends(get_db)):
    """
    Returns a high-level dashboard summary:
    - Total clinics, users, reviews, services
    - Overall average rating across all clinics
    - Number of active vs inactive clinics
    """
    total_clinics = db.query(func.count(models.Clinic.id)).scalar()
    active_clinics = db.query(func.count(models.Clinic.id)).filter(models.Clinic.is_active == True).scalar()
    total_users = db.query(func.count(models.User.id)).scalar()
    total_reviews = db.query(func.count(models.Review.id)).scalar()
    total_services = db.query(func.count(models.Service.id)).scalar()
    avg_rating = db.query(func.avg(models.Review.rating)).scalar()

    return {
        "total_clinics": total_clinics or 0,
        "active_clinics": active_clinics or 0,
        "inactive_clinics": (total_clinics or 0) - (active_clinics or 0),
        "total_users": total_users or 0,
        "total_reviews": total_reviews or 0,
        "total_services": total_services or 0,
        "overall_average_rating": round(float(avg_rating), 2) if avg_rating else 0.0,
    }


@router.get("/top-clinics", response_model=List[schemas.ClinicRankingResponse])
def get_top_clinics(
    limit: int = Query(5, ge=1, le=20, description="Number of top clinics to return"),
    min_reviews: int = Query(1, ge=1, description="Minimum number of reviews required"),
    db: Session = Depends(get_db)
):
    """
    Returns the top-rated clinics ranked by average rating.
    Only includes clinics with at least `min_reviews` reviews.
    Uses SQL GROUP BY + HAVING + ORDER BY - advanced aggregation.
    """
    results = (
        db.query(
            models.Clinic.id,
            models.Clinic.name,
            models.Clinic.city,
            func.avg(models.Review.rating).label("average_rating"),
            func.count(models.Review.id).label("review_count"),
        )
        .join(models.Review, models.Review.clinic_id == models.Clinic.id)
        .filter(models.Clinic.is_active == True)
        .group_by(models.Clinic.id, models.Clinic.name, models.Clinic.city)
        .having(func.count(models.Review.id) >= min_reviews)
        .order_by(desc("average_rating"))
        .limit(limit)
        .all()
    )

    return [
        {
            "rank": idx + 1,
            "clinic_id": row.id,
            "clinic_name": row.name,
            "city": row.city,
            "average_rating": round(float(row.average_rating), 2),
            "review_count": row.review_count,
        }
        for idx, row in enumerate(results)
    ]


@router.get("/rating-distribution", response_model=List[schemas.RatingDistribution])
def get_rating_distribution(
    clinic_id: Optional[int] = Query(None, description="Filter by a specific clinic, or leave empty for all"),
    db: Session = Depends(get_db)
):
    """
    Returns how many reviews exist for each star rating (1–5).
    Useful for showing a rating breakdown bar chart on the frontend.
    Uses SQL GROUP BY on rating value.
    """
    query = db.query(
        models.Review.rating,
        func.count(models.Review.id).label("count")
    )

    if clinic_id:
        query = query.filter(models.Review.clinic_id == clinic_id)

    results = query.group_by(models.Review.rating).order_by(models.Review.rating).all()

    # Fill in missing star ratings with 0
    rating_map = {row.rating: row.count for row in results}
    distribution = [
        {
            "stars": star,
            "count": rating_map.get(star, 0),
        }
        for star in range(1, 6)
    ]

    total = sum(d["count"] for d in distribution)
    for d in distribution:
        d["percentage"] = round((d["count"] / total * 100), 1) if total > 0 else 0.0

    return distribution


@router.get("/clinics-per-city", response_model=List[schemas.CityStats])
def get_clinics_per_city(db: Session = Depends(get_db)):
    """
    Returns the number of clinics grouped by city.
    Shows which cities have the most clinic coverage.
    Uses SQL GROUP BY + ORDER BY COUNT.
    """
    results = (
        db.query(
            models.Clinic.city,
            func.count(models.Clinic.id).label("clinic_count"),
            func.avg(models.Review.rating).label("avg_rating"),
        )
        .outerjoin(models.Review, models.Review.clinic_id == models.Clinic.id)
        .filter(models.Clinic.is_active == True)
        .group_by(models.Clinic.city)
        .order_by(desc("clinic_count"))
        .all()
    )

    return [
        {
            "city": row.city,
            "clinic_count": row.clinic_count,
            "average_rating": round(float(row.avg_rating), 2) if row.avg_rating else None,
        }
        for row in results
    ]
