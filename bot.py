import re
import csv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8541159917:AAEV4u3rBhi1VNdauq5P2V8sla9tm-9kxNc"

def load_answers():
    answers = {}
    with open("answers.csv", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:
                key = row[0].strip()
                value = row[1].strip()
                answers[key] = value
    return answers

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()

    answers = load_answers()

    match = re.search(r"\d+", user_text)

    if match:
        number = match.group()
        if number in answers:
            await update.message.reply_text(answers[number])
            return

    await update.message.reply_text("Задача не найдена")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))

app.run_polling()
