from django.db import models

class Gene(models.Model):
    id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=20)
    fullName = models.CharField(max_length=255)
    functionSummary = models.TextField()

    def __str__(self) -> str:
        return self.symbol
