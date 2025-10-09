from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.patient_simple import PatientCreate, PatientResponse
from datetime import datetime
import uuid

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("/", response_model=list[PatientResponse])
async def get_patients():
    """Get all patients (simplified)."""
    # Return empty list for now
    return []


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(patient_data: PatientCreate):
    """Create a new patient (simplified)."""
    patient_id = str(uuid.uuid4())
    return PatientResponse(
        id=patient_id,
        first_name=patient_data.first_name,
        last_name=patient_data.last_name,
        email=patient_data.email,
        phone=patient_data.phone,
        date_of_birth=patient_data.date_of_birth,
        created_at=datetime.utcnow()
    )
