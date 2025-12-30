import asyncio
from fastapi import FastAPI
from app.config import TELEGRAM_BOT_TOKEN
from app.bot import build_bot_app

api = FastAPI(title="AI LegalMind")

@api.get("/health")
def health():
    return {"status": "ok"}

@api.on_event("startup")
async def startup():
    if not TELEGRAM_BOT_TOKEN:
        print("⚠️ TELEGRAM_BOT_TOKEN غير موجود في .env")
        return

    bot_app = build_bot_app(TELEGRAM_BOT_TOKEN)

    # تشغيل البوت polling داخل نفس العملية
    await bot_app.initialize()
    await bot_app.start()
    asyncio.create_task(bot_app.updater.start_polling())
    print("✅ Telegram bot started (polling).")
