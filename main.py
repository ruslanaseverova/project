import telebot
from config import TOKEN
import os
#from extract_text import extract_text_from_docx, extract_text_from_pdf 


# Замени 'TOKEN' на токен твоего бота
# Этот токен ты получаешь от BotFather, чтобы бот мог работать
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start и /play
@bot.message_handler(commands=['start', "play"])
def send_welcome(message):
    text = (
        "Отправьте резюме (PDF, DOCX, TXT) или вставьте текст. "
        "Бот проанализирует и вернёт краткий отчёт."
    )
    bot.reply_to(message, text)


bot.polling()