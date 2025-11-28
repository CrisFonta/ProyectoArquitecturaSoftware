from pydantic import BaseModel

class VariantDTO(BaseModel):
    geneId: int
    chromosome: str
    position: int
    referenceBase: str
    alternateBase: str
    impact: str
