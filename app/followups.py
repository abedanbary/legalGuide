from typing import List, Dict, Any
from app.schemas import Analysis

def get_followups(a: Analysis) -> List[Dict[str, Any]]:
    """
    קבלת שאלות המשך המתאימות לפי סוג התיק
    
    Args:
        a: אובייקט הניתוח המכיל את סיווג התיק
    
    Returns:
        רשימת שאלות המשך המותאמות לסוג התיק
    """
    
    # שאלות לפי קטגוריה
    followup_questions = {
        "קניות_אונליין": [
            {
                "slot": "purchase_date",
                "kind": "text",
                "q": "מתי בוצעה הרכישה? (דוגמה: לפני שבועיים, בתאריך 01/12/2024)"
            },
            {
                "slot": "purchase_amount",
                "kind": "number",
                "q": "מה סכום התשלום? (הזן מספר בלבד בשקלים)"
            },
            {
                "slot": "has_invoice",
                "kind": "bool",
                "q": "האם יש לך חשבונית או קבלה? (כן/לא)"
            },
            {
                "slot": "contacted_seller",
                "kind": "bool",
                "q": "האם פנית למוכר או לשירות לקוחות? (כן/לא)"
            },
            {
                "slot": "seller_response",
                "kind": "text",
                "q": "מה הייתה תגובת המוכר? (אם לא פנית, כתוב: לא פניתי)"
            }
        ],
        
        "שכירות": [
            {
                "slot": "has_contract",
                "kind": "bool",
                "q": "האם קיים חוזה שכירות כתוב וחתום? (כן/לא)"
            },
            {
                "slot": "contract_duration",
                "kind": "text",
                "q": "מה משך חוזה השכירות? (דוגמה: שנה אחת, שלוש שנים)"
            },
            {
                "slot": "monthly_rent",
                "kind": "number",
                "q": "מה שכר הדירה החודשי? (הזן מספר בלבד בשקלים)"
            },
            {
                "slot": "deposit_amount",
                "kind": "number",
                "q": "מה סכום הפיקדון ששולם? (הזן מספר בלבד)"
            },
            {
                "slot": "handover_protocol",
                "kind": "bool",
                "q": "האם קיים פרוטוקול מסירה מתועד? (כן/לא)"
            },
            {
                "slot": "written_complaint",
                "kind": "bool",
                "q": "האם הגשת תלונה כתובה לבעל הבית/שוכר? (כן/לא)"
            }
        ],
        
        "פרטיות": [
            {
                "slot": "incident_date",
                "kind": "text",
                "q": "מתי התרחשה ההפרה? (דוגמה: לפני 3 ימים, בתאריך 10/12/2024)"
            },
            {
                "slot": "privacy_type",
                "kind": "text",
                "q": "מה סוג המידע שהופר? (דוגמה: תמונות אישיות, מידע פיננסי, נתונים רפואיים)"
            },
            {
                "slot": "violation_platform",
                "kind": "text",
                "q": "היכן התרחשה ההפרה? (דוגמה: פייסבוק, וואטסאפ, אתר אינטרנט)"
            },
            {
                "slot": "has_evidence",
                "kind": "bool",
                "q": "האם יש לך ראיות מתועדות (צילומי מסך, הקלטות)? (כן/לא)"
            },
            {
                "slot": "requested_removal",
                "kind": "bool",
                "q": "האם ביקשת להסיר את התוכן או להפסיק את ההפרה? (כן/לא)"
            },
            {
                "slot": "ongoing_threat",
                "kind": "bool",
                "q": "האם ההפרה ממשיכה או יש איום לפרסם עוד? (כן/לא)"
            }
        ],
        
        "חוזים": [
            {
                "slot": "has_written_contract",
                "kind": "bool",
                "q": "האם החוזה כתוב וחתום על ידי שני הצדדים? (כן/לא)"
            },
            {
                "slot": "contract_date",
                "kind": "text",
                "q": "מתי נחתם החוזה? (דוגמה: לפני חודשיים, ב-15/10/2024)"
            },
            {
                "slot": "contract_value",
                "kind": "number",
                "q": "מה הערך הכספי של החוזה? (הזן מספר בשקלים, או 0 אם אין)"
            },
            {
                "slot": "breach_type",
                "kind": "text",
                "q": "מה סוג ההפרה? (דוגמה: אי תשלום, אי אספקה, עיכוב בביצוע)"
            },
            {
                "slot": "notified_other_party",
                "kind": "bool",
                "q": "האם הודעת לצד השני בכתב על ההפרה? (כן/לא)"
            },
            {
                "slot": "damages_occurred",
                "kind": "bool",
                "q": "האם נגרמו לך נזקים כספיים? (כן/לא)"
            }
        ],
        
        "נזקים_כספיים": [
            {
                "slot": "damage_date",
                "kind": "text",
                "q": "מתי נגרם הנזק הכספי? (דוגמה: לפני חודש, ב-20/11/2024)"
            },
            {
                "slot": "damage_amount",
                "kind": "number",
                "q": "מה שווי הנזק הכספי? (הזן מספר בלבד בשקלים)"
            },
            {
                "slot": "damage_cause",
                "kind": "text",
                "q": "מה גרם לנזק? (דוגמה: הונאה, רמאות, רשלנות, תאונה)"
            },
            {
                "slot": "has_evidence",
                "kind": "bool",
                "q": "האם יש לך ראיות מסמכיות (חשבוניות, העברות, חוזים)? (כן/לא)"
            },
            {
                "slot": "responsible_party_known",
                "kind": "bool",
                "q": "האם אתה יודע מי אחראי לנזק? (כן/לא)"
            },
            {
                "slot": "compensation_requested",
                "kind": "bool",
                "q": "האם דרשת פיצוי באופן רשמי? (כן/לא)"
            }
        ],
        
        "עבודה_ותעסוקה": [
            {
                "slot": "has_employment_contract",
                "kind": "bool",
                "q": "האם יש לך חוזה עבודה כתוב? (כן/לא)"
            },
            {
                "slot": "employment_duration",
                "kind": "text",
                "q": "כמה זמן אתה עובד במקום? (דוגמה: שנתיים, 6 חודשים)"
            },
            {
                "slot": "monthly_salary",
                "kind": "number",
                "q": "מה שכרך החודשי? (הזן מספר בלבד בשקלים)"
            },
            {
                "slot": "issue_type",
                "kind": "text",
                "q": "מה בדיוק סוג הבעיה? (דוגמה: אי תשלום שכר, פיטורים שלא כדין, שעות נוספות)"
            },
            {
                "slot": "complaint_filed",
                "kind": "bool",
                "q": "האם הגשת תלונה פנימית להנהלה? (כן/לא)"
            },
            {
                "slot": "has_payslips",
                "kind": "bool",
                "q": "האם יש לך תלושי שכר ומסמכים? (כן/לא)"
            }
        ],
        
        # שאלות ברירת מחדל
        "אחר": [
            {
                "slot": "incident_date",
                "kind": "text",
                "q": "מתי התרחשה הבעיה? (ציין תאריך או תקופה בקירוב)"
            },
            {
                "slot": "financial_impact",
                "kind": "number",
                "q": "האם יש ערך כספי שנפגע? (הזן מספר בשקלים, או 0 אם אין)"
            },
            {
                "slot": "parties_involved",
                "kind": "text",
                "q": "מי הצדדים המעורבים? (דוגמה: פרט, חברה, מוסד ממשלתי)"
            },
            {
                "slot": "has_documentation",
                "kind": "bool",
                "q": "האם יש לך מסמכים או ראיות? (כן/לא)"
            },
            {
                "slot": "attempts_made",
                "kind": "text",
                "q": "אילו צעדים נקטת עד כה? (כתוב בקצרה או: לא נקטתי צעדים)"
            }
        ]
    }
    
    # החזרת השאלות המתאימות לקטגוריה
    return followup_questions.get(a.category, followup_questions["אחר"])