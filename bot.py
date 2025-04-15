import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

# Логын тохиргоо
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Зурхайг илгэдэг функц
def send_horoscope(context: CallbackContext):
    chat_id = context.job.context
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    # Энд таны зурхайн мессежийг тохируулна уу.
    message = f"📅 {today}-ын зурхай:\n\n🐷 Гахай жил: Азтай, сэргэлэн сэтгэл!\n♓ Загасны орд: Бүтээлч, гүн гүнзгий сэтгэл."
    context.bot.send_message(chat_id=chat_id, text=message)

# /today командыг хүлээн авч зурхай илгээх функц
def today(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    send_horoscope(CallbackContext.from_update(update))
    update.message.reply_text("Өнөөдрийн зурхай илгээсэн ээ!")

def main():
    # BOT_TOKEN - орчны хувьсагчоос авагдана
    import os
    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN:
        logger.error("BOT_TOKEN орчны хувьсагч олдсонгүй!")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("today", today))

    # Ажлын хуваарь - өглөө бүр 08:30 (Улаанбаатар цагийн бүсээр) тохируулах
    scheduler = BackgroundScheduler(timezone="Asia/Ulaanbaatar")
    # Бот эхлүүлсэн chat_id-г тохирох шаардлагатай. Жишээ нь, сонгосон ID (үнэн chat id-г өөрөө тохируулна)
    chat_id = 123456789  
    scheduler.add_job(send_horoscope, 'cron', hour=8, minute=30, context=chat_id)
