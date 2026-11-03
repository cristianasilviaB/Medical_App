from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import model
import schemas
from router.auth import get_current_user
from services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


# 1. SUMMARY STATS - Protected route
@router.get("/summary", response_model=schemas.AnalyticsSummaryResponse)
def get_analytics_summary(
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    analytics_service = AnalyticsService(db)
    return analytics_service.get_summary()


# 2. DOCTORS STATS - Protected route
@router.get("/doctors", response_model=List[schemas.DoctorAnalyticsResponse])
def get_doctors_analytics(
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    analytics_service = AnalyticsService(db)
    return analytics_service.get_doctors_analytics()


# 3. SERVICES STATS - Protected route
@router.get("/services", response_model=List[schemas.ServiceAnalyticsResponse])
def get_services_analytics(
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    analytics_service = AnalyticsService(db)
    return analytics_service.get_services_analytics()