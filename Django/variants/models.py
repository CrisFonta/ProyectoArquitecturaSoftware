import uuid
from django.db import models
from genes.models import Gene

class GeneticVariant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE, related_name="variants")
    chromosome = models.CharField(max_length=10)
    position = models.IntegerField()
    referenceBase = models.CharField(max_length=5)
    alternateBase = models.CharField(max_length=5)
    impact = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.gene.symbol} {self.chromosome}:{self.position} {self.referenceBase}>{self.alternateBase}"
