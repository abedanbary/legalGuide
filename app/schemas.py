from pydantic import BaseModel
from typing import List, Literal

Category = Literal["קניות_אונליין", "שכירות", "פרטיות", "חוזים", "נזקים_כספיים", "עבודה_ותעסוקה", "אחר"]
Complexity = Literal["נמוכה", "בינונית", "גבוהה"]

class Analysis(BaseModel):
    category: Category
    complexity: Complexity
    summary: str
    missing_info: List[str] = []
    confidence: float = 0.7