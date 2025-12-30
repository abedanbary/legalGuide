import re
from typing import Tuple, Optional

# תשובות חיוביות
YES_HE = {"כן", "כ", "yes", "y", "נכון", "נ", "אכן", "בטח"}

# תשובות שליליות
NO_HE = {"לא", "ל", "no", "n", "שלילי", "לא נכון"}


def validate(kind: str, text: str) -> Tuple[bool, Optional[str]]:
    """
    אימות נכונות התשובה לפי סוגה
    
    Args:
        kind: סוג התשובה המצופה (bool, number, text)
        text: הטקסט שהוזן מהמשתמש
    
    Returns:
        (האם התשובה נכונה, הערך המעובד)
    """
    t = text.strip()

    if kind == "bool":
        t_lower = t.lower()
        if t_lower in YES_HE or t in YES_HE:
            return True, "כן"
        if t_lower in NO_HE or t in NO_HE:
            return True, "לא"
        return False, None

    if kind == "number":
        # הסר כל מה שאינו ספרות
        digits = re.sub(r"[^\d]", "", t)
        if len(digits) >= 1:
            return True, digits
        return False, None

    if kind == "text":
        if len(t) >= 2:
            return True, t
        return False, None

    return False, None