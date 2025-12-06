from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Bot
import asyncio

from config import TELEGRAM_TOKEN, CHAT_ID
from fetch_data import get_iran_prices, get_global_gold
from analyzer import analyze

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ربات تحلیل طلا و سکه فعال شد ✅\nبرای تحلیل: /analysis")

async def analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        iran = get_iran_prices()
        global_gold = get_global_gold()
        result = analyze(iran, global_gold)

        msg = f"""
📊 تحلیل لحظه‌ای بازار طلا و سکه

🥇 طلای جهانی: {global_gold} $
💵 دلار: {iran['dollar']:,} تومان
🟡 طلا ۱۸ عیار: {iran['geram18']:,} تومان
🪙 سکه امامی: {iran['sekke_emami']:,} تومان

📈 قیمت تئوریک سکه: {result['fair_price']:,}
📉 اختلاف بازار: {result['diff']:,}

🔔 سیگنال نهایی:
{result['signal']}
"""
        await update.message.reply_text(msg)

    except Exception as e:
        await update.message.reply_text("❌ خطا در دریافت اطلاعات – کمی بعد دوباره تلاش کن")
        print(e)

# ---------------- هشدار خودکار هر 10 دقیقه ----------------
async def auto_alert(bot: Bot):
    while True:
        try:
            iran = get_iran_prices()
            global_gold = get_global_gold()
            result = analyze(iran, global_gold)

            # فقط وقتی حباب خیلی مثبت یا منفی است، هشدار بده
            if "خرید عالی" in result["signal"] or "فروش" in result["signal"]:
                msg = f"⚠️ هشدار قیمت!\n\n{result['signal']}\n\nسکه: {iran['sekke_emami']:,}\nطلای ۱۸ عیار: {iran['geram18']:,}\nدلار: {iran['dollar']:,}"
                await bot.send_message(chat_id=CHAT_ID, text=msg)
        except Exception as e:
            print("خطا در هشدار خودکار:", e)
        await asyncio.sleep(600)  # هر 10 دقیقه

# ---------------- اجرای ربات ----------------
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analysis", analysis))

    bot_instance = Bot(TELEGRAM_TOKEN)
    asyncio.create_task(auto_alert(bot_instance))

    app.run_polling()