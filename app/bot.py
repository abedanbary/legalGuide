from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import datetime, timedelta
from typing import Optional

from app.ai_service import analyze_text
from app.rules import format_reply, get_legal_resources
from app.state import SESSIONS
from app.session import Session
from app.followups import get_followups
from app.validators import validate


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """הודעת ברוכים הבאים"""
    welcome_message = """ברוכים הבאים ל-AI LegalMind
העוזר המשפטי החכם

אנחנו כאן לעזור לך לקבל הכוונה משפטית ראשונית בתחומים:
- קניות אונליין וזכויות צרכן
- סכסוכי שכירות
- הפרות פרטיות
- סכסוכים חוזיים
- תביעות פיצוי
- נושאי עבודה ותעסוקה

פקודות זמינות:
/new - התחל תיק חדש
/end - סיים תיק
/resources - משאבים משפטיים
/help - עזרה

הערה: זהו ייעוץ ראשוני בלבד, לא תחליף לעורך דין.

להתחלת תיק חדש: /new"""
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """הצגת עזרה"""
    help_text = """איך משתמשים בבוט?

1. התחל תיק חדש: /new
2. תאר את הבעיה בשתי-שלוש משפטים
3. ענה על השאלות שהבוט שואל
4. קבל ניתוח, המלצות ומשאבים משפטיים
5. סיים את התיק: /end

טיפים:
- היה ברור ומדויק
- ציין תאריכים וסכומים אם אפשר
- ענה בכנות
- שמור העתק של הניתוח

פקודות:
/new - תיק חדש
/end - סיום תיק
/resources - משאבים משפטיים
/help - הודעה זו"""
    await update.message.reply_text(help_text)


async def new_case(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """התחלת תיק חדש"""
    user_id = update.effective_user.id
    
    session = Session()
    SESSIONS[user_id] = session

    session.active = True
    session.awaiting_problem = True
    session.analysis = None
    session.slots = {}
    session.pending_slot = None
    session.pending_kind = None
    session.pending_question = None
    session.last_activity = datetime.now()

    message = """התחלת תיק משפטי חדש

תאר את הבעיה המשפטית בצורה ברורה ותמציתית.

דוגמה:
"קניתי טלפון באתר באינטרנט ב-2000 ₪, המוצר הגיע פגום ולא עובד, והחברה מסרבת להחזיר את הכסף או להחליף."

שתי-שלוש משפטים מספיקות."""
    await update.message.reply_text(message)


async def end_case(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """סיום תיק"""
    user_id = update.effective_user.id
    session = SESSIONS.get(user_id)

    if not session or not session.active:
        await update.message.reply_text(
            "אין תיק פתוח כרגע.\n\n"
            "להתחלת תיק חדש: /new"
        )
        return

    if session.analysis:
        reply = format_reply(session.analysis, include_resources=True)
        
        if session.slots:
            collected = "\n".join([f"  • {k}: {v}" for k, v in session.slots.items()])
            reply += f"\n\nמידע שנאסף:\n{collected}"
        
        reply += "\n\n✓ התיק הסתיים בהצלחה"
        reply += "\n\nלתיק חדש: /new"
        
        await update.message.reply_text(reply)
    else:
        await update.message.reply_text(
            "התיק הסתיים ללא ניתוח.\n\n"
            "לתיק חדש: /new"
        )

    session.active = False
    session.awaiting_problem = False
    session.pending_slot = None
    session.pending_kind = None
    session.pending_question = None


async def show_resources(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """הצגת משאבים משפטיים"""
    resources_menu = """משאבים משפטיים זמינים

בחר תחום:

/resources_shopping - קניות וצרכנות
/resources_rent - שכירות
/resources_privacy - פרטיות
/resources_contracts - חוזים
/resources_damage - נזקים ופיצויים
/resources_work - עבודה ותעסוקה
/resources_general - כללי

חזרה לתפריט: /start"""
    await update.message.reply_text(resources_menu)


async def resources_shopping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """משאבים לקניות"""
    resources = get_legal_resources("קניות_אונליין")
    message = f"""משאבים משפטיים - קניות אונליין

{resources}

חזרה: /resources"""
    await update.message.reply_text(message)


async def resources_rent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """משאבים לשכירות"""
    resources = get_legal_resources("שכירות")
    message = f"""משאבים משפטיים - שכירות

{resources}

חזרה: /resources"""
    await update.message.reply_text(message)


async def resources_privacy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """משאבים לפרטיות"""
    resources = get_legal_resources("פרטיות")
    message = f"""משאבים משפטיים - פרטיות

{resources}

חזרה: /resources"""
    await update.message.reply_text(message)


async def resources_contracts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """משאבים לחוזים"""
    resources = get_legal_resources("חוזים")
    message = f"""משאבים משפטיים - חוזים

{resources}

חזרה: /resources"""
    await update.message.reply_text(message)


async def resources_damage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """משאבים לנזקים"""
    resources = get_legal_resources("נזקים_כספיים")
    message = f"""משאבים משפטיים - נזקים ופיצויים

{resources}

חזרה: /resources"""
    await update.message.reply_text(message)


async def resources_work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """משאבים לעבודה"""
    resources = get_legal_resources("עבודה_ותעסוקה")
    message = f"""משאבים משפטיים - עבודה ותעסוקה

{resources}

חזרה: /resources"""
    await update.message.reply_text(message)


async def resources_general(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """משאבים כלליים"""
    resources = get_legal_resources("אחר")
    message = f"""משאבים משפטיים כלליים

{resources}

חזרה: /resources"""
    await update.message.reply_text(message)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """עיבוד טקסט מהמשתמש"""
    user_id = update.effective_user.id
    text = update.message.text.strip()

    session = SESSIONS.get(user_id)
    if session is None:
        session = Session()
        SESSIONS[user_id] = session

    session.last_activity = datetime.now()

    if not session.active:
        await update.message.reply_text(
            "אין תיק פתוח.\n\n"
            "להתחלת תיק חדש: /new"
        )
        return

    # שלב 1: קבלת תיאור הבעיה
    if session.awaiting_problem:
        if len(text) < 20:
            await update.message.reply_text(
                "התיאור קצר מדי. אנא תאר את הבעיה ביתר פירוט.\n\n"
                "דוגמה: קניתי מוצר באתר והגיע פגום, והחברה מסרבת להחזיר כסף."
            )
            return

        processing_message = await update.message.reply_text(
            "מנתח את הבעיה...\nרגע אחד."
        )

        try:
            session.analysis = await analyze_text(text)
            session.awaiting_problem = False

            await processing_message.delete()

            followups = get_followups(session.analysis)
            
            if followups and len(followups) > 0:
                first = followups[0]
                session.pending_slot = first["slot"]
                session.pending_kind = first["kind"]
                session.pending_question = first["q"]
                
                intro_message = (
                    "הבעיה נותחה בהצלחה.\n\n"
                    "כמה שאלות נוספות לדיוק הניתוח:\n\n"
                    f"{session.pending_question}"
                )
                await update.message.reply_text(intro_message)
            else:
                reply = format_reply(session.analysis, include_resources=True)
                reply += "\n\nלסיום התיק: /end"
                await update.message.reply_text(reply)
                
        except Exception as e:
            await processing_message.delete()
            await update.message.reply_text(
                "אירעה שגיאה בניתוח.\n\n"
                "נסה שוב, או התחל תיק חדש: /new"
            )
            print(f"שגיאת ניתוח: {e}")
        return

    # שלב 2: תשובות לשאלות
    if session.pending_slot:
        is_valid, validated_value = validate(session.pending_kind, text)
        
        if not is_valid:
            await update.message.reply_text(
                "התשובה לא תקינה.\n\n"
                "נסה שוב:\n\n"
                f"{session.pending_question}"
            )
            return

        session.slots[session.pending_slot] = validated_value
        session.pending_slot = None
        session.pending_kind = None
        session.pending_question = None

    # שלב 3: שאלה הבאה או תוצאות
    followups = get_followups(session.analysis)
    
    for item in followups:
        if item["slot"] not in session.slots:
            session.pending_slot = item["slot"]
            session.pending_kind = item["kind"]
            session.pending_question = item["q"]
            
            remaining = len([f for f in followups if f["slot"] not in session.slots])
            progress_message = (
                f"{session.pending_question}\n\n"
                f"שאלות נותרו: {remaining}"
            )
            await update.message.reply_text(progress_message)
            return

    # כל השאלות נענו - תוצאות סופיות
    reply = format_reply(session.analysis, include_resources=True)
    
    if session.slots:
        collected = "\n".join([f"  • {k}: {v}" for k, v in session.slots.items()])
        reply += f"\n\nמידע שנאסף:\n{collected}"
    
    reply += "\n\nלסיום התיק: /end"
    
    await update.message.reply_text(reply)


async def cleanup_old_sessions():
    """ניקוי סשנים ישנים"""
    current_time = datetime.now()
    timeout = timedelta(hours=2)
    
    inactive_users = []
    for user_id, session in SESSIONS.items():
        if current_time - session.last_activity > timeout:
            inactive_users.append(user_id)
    
    for user_id in inactive_users:
        del SESSIONS[user_id]
    
    if inactive_users:
        print(f"נוקו {len(inactive_users)} סשנים לא פעילים")


def build_bot_app(token: str) -> Application:
    """בניית אפליקציית הבוט"""
    app = Application.builder().token(token).build()
    
    # פקודות בסיסיות
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("new", new_case))
    app.add_handler(CommandHandler("end", end_case))
    
    # פקודות משאבים
    app.add_handler(CommandHandler("resources", show_resources))
    app.add_handler(CommandHandler("resources_shopping", resources_shopping))
    app.add_handler(CommandHandler("resources_rent", resources_rent))
    app.add_handler(CommandHandler("resources_privacy", resources_privacy))
    app.add_handler(CommandHandler("resources_contracts", resources_contracts))
    app.add_handler(CommandHandler("resources_damage", resources_damage))
    app.add_handler(CommandHandler("resources_work", resources_work))
    app.add_handler(CommandHandler("resources_general", resources_general))
    
    # מעבד טקסט
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, 
        handle_text
    ))
    
    return app