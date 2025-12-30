# 🤖 AI LegalMind - העוזר המשפטי החכם


```
ai-legalmind/
├── app/
│   ├── __init__.py
│   ├── ai_service.py      # שירות AI (DeepSeek)
│   ├── bot.py             # לוגיקת הבוט
│   ├── config.py          # הגדרות
│   ├── followups.py       # שאלות המשך
│   ├── main.py            # FastAPI אפליקציה
│   ├── prompts.py         # פרומפט למודל
│   ├── rules.py           # כללים ומשאבים
│   ├── schemas.py         # מבני נתונים
│   ├── session.py         # ניהול סשן
│   ├── state.py           # מצב גלובלי
│   └── validators.py      # אימות קלט
├── .env.example           # תבנית למשתני סביבה
├── .gitignore
├── requirements.txt
└── README.md
```

---

התקנה והרצה

 דרישות מקדימות

- Python 3.8+
- טוקן בוט טלגרם (מ-[@BotFather](https://t.me/BotFather))
- מפתח API של DeepSeek ([platform.deepseek.com](https://platform.deepseek.com))

#שלבי התקנה

1.\\כפול הפרויקט:**
```bash
git clone https://github.com/abedanbary/legalGuide.git
cd legalGuide
```

2. **יצירת סביבה וירטואלית:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# או
venv\Scripts\activate     # Windows
```

3. **התקנת תלויות:**
```bash
pip install -r requirements.txt
```

4. **הגדרת משתני סביבה:**
```bash
cp .env.example .env
# ערוך את .env והוסף את המפתחות שלך
```

תוכן `.env`:
```env
TELEGRAM_TOKEN=your_telegram_bot_token
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_MODEL=deepseek-chat
```

5. **הרצת הבוט:**
```bash
uvicorn app.main:api --reload
```
*

⭐ אם הפרויקט עזר לך, אל תשכח לתת כוכב!

</div>
