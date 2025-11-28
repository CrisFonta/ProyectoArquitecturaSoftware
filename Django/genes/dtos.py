from pydantic import BaseModel

class GeneDTO(BaseModel):
    symbol: str
    fullName: str
    functionSummary: str
