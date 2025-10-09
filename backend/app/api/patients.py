from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.patient import Patient, MedicalHistory, Allergy, Medication
from app.schemas.patient import (
    PatientCreate, PatientUpdate, PatientResponse,
    MedicalHistoryCreate, MedicalHistoryUpdate, MedicalHistoryResponse,
    AllergyCreate, AllergyUpdate, AllergyResponse,
    MedicationCreate, MedicationUpdate, MedicationResponse
)
from app.utils.security import get_current_active_user, require_roles
from app.utils.audit import log_audit_event, get_client_ip, get_user_agent
from typing import List

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("/me", response_model=PatientResponse)
async def get_my_patient_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's patient profile."""
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )
    
    return patient


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient_profile(
    patient_data: PatientCreate,
    request: Request,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create or update patient profile."""
    # Check if patient profile already exists
    existing_patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    
    if existing_patient:
        # Update existing profile
        for field, value in patient_data.dict(exclude_unset=True).items():
            setattr(existing_patient, field, value)
        
        db.commit()
        db.refresh(existing_patient)
        
        # Log audit event
        log_audit_event(
            db=db,
            user=current_user,
            action="update_patient_profile",
            resource="patient",
            resource_id=str(existing_patient.id),
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request)
        )
        
        return existing_patient
    else:
        # Create new profile
        patient = Patient(
            user_id=current_user.id,
            **patient_data.dict()
        )
        
        db.add(patient)
        db.commit()
        db.refresh(patient)
        
        # Log audit event
        log_audit_event(
            db=db,
            user=current_user,
            action="create_patient_profile",
            resource="patient",
            resource_id=str(patient.id),
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request)
        )
        
        return patient


@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient_profile(
    patient_id: int,
    current_user: User = Depends(require_roles(["doctor", "admin"])),
    db: Session = Depends(get_db)
):
    """Get patient profile by ID (doctors and admins only)."""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    return patient


# Medical History endpoints
@router.get("/me/medical-history", response_model=List[MedicalHistoryResponse])
async def get_my_medical_history(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's medical history."""
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )
    
    return patient.medical_history


@router.post("/me/medical-history", response_model=MedicalHistoryResponse, status_code=status.HTTP_201_CREATED)
async def add_medical_history(
    history_data: MedicalHistoryCreate,
    request: Request,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add medical history entry."""
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )
    
    medical_history = MedicalHistory(
        patient_id=patient.id,
        **history_data.dict()
    )
    
    db.add(medical_history)
    db.commit()
    db.refresh(medical_history)
    
    # Log audit event
    log_audit_event(
        db=db,
        user=current_user,
        action="add_medical_history",
        resource="medical_history",
        resource_id=str(medical_history.id),
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request)
    )
    
    return medical_history


# Allergy endpoints
@router.get("/me/allergies", response_model=List[AllergyResponse])
async def get_my_allergies(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's allergies."""
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )
    
    return patient.allergies


@router.post("/me/allergies", response_model=AllergyResponse, status_code=status.HTTP_201_CREATED)
async def add_allergy(
    allergy_data: AllergyCreate,
    request: Request,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add allergy entry."""
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )
    
    allergy = Allergy(
        patient_id=patient.id,
        **allergy_data.dict()
    )
    
    db.add(allergy)
    db.commit()
    db.refresh(allergy)
    
    # Log audit event
    log_audit_event(
        db=db,
        user=current_user,
        action="add_allergy",
        resource="allergy",
        resource_id=str(allergy.id),
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request)
    )
    
    return allergy


# Medication endpoints
@router.get("/me/medications", response_model=List[MedicationResponse])
async def get_my_medications(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's medications."""
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )
    
    return patient.medications


@router.post("/me/medications", response_model=MedicationResponse, status_code=status.HTTP_201_CREATED)
async def add_medication(
    medication_data: MedicationCreate,
    request: Request,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add medication entry."""
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient profile not found"
        )
    
    medication = Medication(
        patient_id=patient.id,
        **medication_data.dict()
    )
    
    db.add(medication)
    db.commit()
    db.refresh(medication)
    
    # Log audit event
    log_audit_event(
        db=db,
        user=current_user,
        action="add_medication",
        resource="medication",
        resource_id=str(medication.id),
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request)
    )
    
    return medication
