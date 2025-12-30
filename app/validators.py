import re
from typing import Tuple, Optional

# תשובות חיוביות
YES = {"כן", "כ", "yes", "y", "נכון", "נ", "אכן", "בטח", "יפ", "יפה"}

# תשובות שליליות
NO = {"לא", "ל", "no", "n", "שלילי", "לא נכון", "ממש לא"}


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
        # בדיקת תשובות כן/לא
        t_lower = t.lower()
        if t_lower in YES or t in YES:
            return True, "כן"
        if t_lower in NO or t in NO:
            return True, "לא"
        return False, None

    if kind == "number":
        # חילוץ מספרים מהטקסט
        # מאפשר "20000" או "20,000" או "20000 שקל"
        digits = re.sub(r"[^\d]", "", t)
        if len(digits) >= 1:  # לפחות ספרה אחת
            return True, digits
        return False, None

    if kind == "text":
        # קבלת כל טקסט באורך של יותר משני תווים
        if len(t) >= 2:
            return True, t
        return False, None

    # סוג לא ידוע
    return False, None