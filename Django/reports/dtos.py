from pydantic import BaseModel
from datetime import date

class ReportDTO(BaseModel):
    patientId: str
    variantId: str
    detectionDate: date
    alleleFrequency: float
