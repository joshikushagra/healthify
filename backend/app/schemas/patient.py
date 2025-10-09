from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PatientBase(BaseModel):
    blood_type: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_number: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(PatientBase):
    pass


class PatientResponse(PatientBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MedicalHistoryBase(BaseModel):
    condition: str
    diagnosis_date: Optional[datetime] = None
    status: str
    notes: Optional[str] = None


class MedicalHistoryCreate(MedicalHistoryBase):
    pass


class MedicalHistoryUpdate(MedicalHistoryBase):
    pass


class MedicalHistoryResponse(MedicalHistoryBase):
    id: int
    patient_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AllergyBase(BaseModel):
    allergen: str
    severity: str
    reaction: Optional[str] = None


class AllergyCreate(AllergyBase):
    pass


class AllergyUpdate(AllergyBase):
    pass


class AllergyResponse(AllergyBase):
    id: int
    patient_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MedicationBase(BaseModel):
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: bool = True
    prescribed_by: Optional[str] = None
    notes: Optional[str] = None


class MedicationCreate(MedicationBase):
    pass


class MedicationUpdate(MedicationBase):
    pass


class MedicationResponse(MedicationBase):
    id: int
    patient_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
