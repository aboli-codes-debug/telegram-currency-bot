"""
ربات تلگرام نرخ ارز (USD → تومان)
====================================

این ربات هر ۱۰ ثانیه نرخ دلار را از tgju.org می‌خواند و فقط در صورت
تغییر قیمت، پیام جدید در کانال تلگرام ارسال می‌کند. همچنین هر روز در
ساعت مشخصی یک پیام خوش‌آمد همراه با تاریخ شمسی می‌فرستد.

اجرا:
    python bot.py

قبل از اجرا، فایل .env را طبق نمونه‌ی .env.example پر کنید
(توکن ربات و آیدی کانال هرگز نباید مستقیم داخل کد نوشته شوند).
"""

import asyncio
import os
import sys
from datetime import date, datetime

import jdatetime
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram import Bot

# =========================================================
#                       CONFIG (قابل تغییر)
# =========================================================

load_dotenv()  # مقادیر را از فایل .env می‌خواند

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL_USERNAME")

PRICE_URL = "https://www.tgju.org/profile/price_dollar_rl"
PRICE_CSS_SELECTOR = "span[data-col='info.last_trade.PDrCotVal']"
CHECK_INTERVAL_SECONDS = 10

GREETING_HOUR = 9
GREETING_MINUTE = 0

REQUEST_TIMEOUT_SECONDS = 10

# =========================================================
#                       END CONFIG
# =========================================================


def get_usd_toman() -> int:
    """نرخ لحظه‌ای دلار به تومان را با اسکرپ کردن صفحه‌ی tgju.org برمی‌گرداند."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(PRICE_URL, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    price_tag = soup.select_one(PRICE_CSS_SELECTOR)
    if price_tag is None:
        raise ValueError("عنصر قیمت در صفحه پیدا نشد؛ ممکن است ساختار سایت تغییر کرده باشد.")

    price_text = price_tag.text.strip().replace(",", "")
    return int(price_text)


async def send_daily_greeting(bot: Bot, today: date) -> None:
    """پیام خوش‌آمد روزانه همراه با تاریخ شمسی را ارسال می‌کند."""
    shamsi_date = jdatetime.date.fromgregorian(date=today)
    text = f"☀️ صبح بخیر!\n📅 امروز: {shamsi_date.strftime('%Y/%m/%d')}"
    await bot.send_message(chat_id=CHANNEL, text=text)
    print("پیام سلام روزانه ارسال شد.")


async def price_watcher() -> None:
    bot = Bot(token=TOKEN)
    last_price = None
    last_greeting_date = None  # آخرین روزی که پیام سلام فرستاده شده

    while True:
        now = datetime.now()

        # --- بخش ۱: چک قیمت ---
        try:
            price = get_usd_toman()
            if price != last_price:
                text = f"💵 نرخ جدید دلار: {price:,} ریال"
                await bot.send_message(chat_id=CHANNEL, text=text)
                print("پیام جدید ارسال شد:", price)
                last_price = price
            else:
                print("قیمت تغییر نکرده:", price)
        except Exception as e:
            print(f"[{now.strftime('%H:%M:%S')}] خطا در دریافت/ارسال قیمت: {e}")

        # --- بخش ۲: سلام روزانه ---
        today = now.date()
        if (
            now.hour == GREETING_HOUR
            and now.minute == GREETING_MINUTE
            and last_greeting_date != today
        ):
            try:
                await send_daily_greeting(bot, today)
                last_greeting_date = today
            except Exception as e:
                print("خطا در ارسال سلام روزانه:", e)

        await asyncio.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    if not TOKEN or not CHANNEL:
        print(
            "خطا: BOT_TOKEN یا CHANNEL_USERNAME در فایل .env تنظیم نشده است.\n"
            "فایل .env.example را به .env کپی کن و مقادیر را پر کن."
        )
        sys.exit(1)

    try:
        asyncio.run(price_watcher())
    except KeyboardInterrupt:
        print("\nربات با Ctrl+C متوقف شد.")
