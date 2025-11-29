import uuid
from django.db import models
from variants.models import GeneticVariant

class PatientVariantReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patientId = models.CharField(max_length=255)
    variant = models.ForeignKey(GeneticVariant, on_delete=models.CASCADE, related_name="patient_reports")
    detectionDate = models.DateField()
    alleleFrequency = models.DecimalField(max_digits=5, decimal_places=3)

    def __str__(self) -> str:
        return f"Report {self.id} for patient {self.patientId}"
