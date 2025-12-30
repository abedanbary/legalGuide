import httpx
import json
import re
from typing import Optional, Dict, Any
from app.config import DEEPSEEK_API_KEY, DEEPSEEK_MODEL
from app.prompts import SYSTEM_PROMPT_HE
from app.schemas import Analysis

DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"


def _extract_json(text: str) -> dict:
    """
    חילוץ נתוני JSON מתשובת המודל
    """
    # ניסיון 1: JSON ישיר
    match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    
    # ניסיון 2: JSON בתוך code block
    match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    
    # ניסיון 3: ניקוי טקסט וניסיון חוזר
    cleaned = re.sub(r'[\n\r\t]', ' ', text)
    match = re.search(r'\{.*\}', cleaned)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    
    raise ValueError("לא ניתן לחלץ נתוני JSON תקינים מהתשובה")


def _create_fallback_analysis(message: str) -> Analysis:
    """יצירת ניתוח חלופי במקרה של כשל"""
    return Analysis(
        category="אחר",
        complexity="בינונית",
        summary=message,
        missing_info=[
            "תיאור מפורט יותר של הבעיה",
            "תאריכים מדויקים של האירועים",
            "סכומים כספיים רלוונטיים"
        ],
        confidence=0.2,
    )


async def analyze_text(
    user_text: str, 
    collected_info: Optional[Dict[str, Any]] = None
) -> Analysis:
    """
    ניתוח הטקסט שהוזן על ידי המשתמש באמצעות AI
    
    Args:
        user_text: תיאור הבעיה המשפטית מהמשתמש
        collected_info: מידע נוסף שנאסף משאלות המשך
    
    Returns:
        Analysis: אובייקט המכיל את תוצאות הניתוח
    """
    
    # במקרה שאין מפתח API
    if not DEEPSEEK_API_KEY:
        return Analysis(
            category="אחר",
            complexity="בינונית",
            summary="הניתוח אינו זמין כרגע. אנא בדוק את הגדרות המערכת.",
            missing_info=["תאריך מדויק של האירוע", "ערך הסכום או הנזק", "הצדדים המעורבים"],
            confidence=0.0,
        )

    # בניית הטקסט המלא עם מידע נוסף אם קיים
    full_context = user_text
    
    if collected_info:
        additional_context = "\n\nמידע נוסף שנאסף:\n"
        
        # תרגום שמות השדות לעברית
        field_translations = {
            # שאלות קנייה אונליין
            "purchase_date": "תאריך הרכישה",
            "purchase_amount": "סכום הרכישה",
            "has_invoice": "קיום חשבונית",
            "contacted_seller": "פנייה למוכר",
            "seller_response": "תגובת המוכר",
            
            # שאלות שכירות
            "has_contract": "קיום חוזה כתוב",
            "contract_duration": "משך החוזה",
            "monthly_rent": "שכר דירה חודשי",
            "deposit_amount": "סכום הפיקדון",
            "handover_protocol": "פרוטוקול מסירה",
            "written_complaint": "תלונה כתובה",
            
            # שאלות פרטיות
            "incident_date": "תאריך האירוע",
            "privacy_type": "סוג המידע שהופר",
            "violation_platform": "פלטפורמת ההפרה",
            "has_evidence": "קיום ראיות",
            "requested_removal": "בקשת הסרה",
            "ongoing_threat": "איום מתמשך",
            
            # שאלות חוזים
            "has_written_contract": "חוזה כתוב",
            "contract_date": "תאריך החוזה",
            "contract_value": "ערך החוזה",
            "breach_type": "סוג ההפרה",
            "notified_other_party": "הודעה לצד השני",
            "damages_occurred": "נגרמו נזקים",
            
            # שאלות נזקים כספיים
            "damage_date": "תאריך הנזק",
            "damage_amount": "שווי הנזק",
            "damage_cause": "סיבת הנזק",
            "responsible_party_known": "זיהוי הצד האחראי",
            "compensation_requested": "דרישת פיצוי",
            
            # שאלות עבודה ותעסוקה
            "has_employment_contract": "חוזה עבודה",
            "employment_duration": "משך התעסוקה",
            "monthly_salary": "שכר חודשי",
            "issue_type": "סוג הבעיה",
            "complaint_filed": "הגשת תלונה",
            "has_payslips": "תלושי שכר",
            
            # שאלות כלליות
            "financial_impact": "השפעה כספית",
            "parties_involved": "הצדדים המעורבים",
            "has_documentation": "קיום תיעוד",
            "attempts_made": "צעדים שננקטו"
        }
        
        for key, value in collected_info.items():
            field_name = field_translations.get(key, key)
            additional_context += f"- {field_name}: {value}\n"
        
        full_context += additional_context

    # הכנת בקשת API
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT_HE},
            {"role": "user", "content": full_context},
        ],
        "temperature": 0.15,
        "max_tokens": 600,
        "top_p": 0.9,
    }
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=40) as client:
            response = await client.post(
                DEEPSEEK_URL, 
                json=payload, 
                headers=headers
            )
            response.raise_for_status()
            data = response.json()

        # חילוץ התוכן
        content = data["choices"][0]["message"]["content"]
        parsed_data = _extract_json(content)
        
        # בדיקת שלמות הנתונים
        if "category" not in parsed_data:
            parsed_data["category"] = "אחר"
        if "complexity" not in parsed_data:
            parsed_data["complexity"] = "בינונית"
        if "summary" not in parsed_data:
            parsed_data["summary"] = "התיק התקבל ונמצא בבדיקה"
        if "missing_info" not in parsed_data:
            parsed_data["missing_info"] = []
        if "confidence" not in parsed_data:
            parsed_data["confidence"] = 0.5
            
        return Analysis(**parsed_data)
        
    except httpx.HTTPStatusError as e:
        print(f"שגיאת התחברות ל-API: {e.response.status_code}")
        return _create_fallback_analysis(
            "אירעה שגיאה בהתחברות לשירות הניתוח. נא לנסות שוב."
        )
    except httpx.TimeoutException:
        print("תם הזמן להתחברות ל-API")
        return _create_fallback_analysis(
            "הניתוח לקח זמן רב מהצפוי. נא לנסות שוב."
        )
    except ValueError as e:
        print(f"שגיאה בעיבוד הנתונים: {e}")
        return _create_fallback_analysis(
            "אירעה שגיאה בעיבוד התשובה. נא לנסח את הבעיה בצורה ברורה יותר."
        )
    except Exception as e:
        print(f"שגיאה בלתי צפויה: {type(e).__name__}: {e}")
        return _create_fallback_analysis(
            "אירעה שגיאה בלתי צפויה. נא ליצור קשר עם התמיכה הטכנית."
        )