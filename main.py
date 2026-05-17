import telebot
from config import TOKEN
import os
from extract_text import extract_text_from_pdf, extract_text_from_docx
from analysis import score_resume
from io import BytesIO
#transformers для более сложного анализа, если понадобится
#extract_text_from_docx

# Этот токен ты получаешь от BotFather, чтобы бот мог работать
#TOKEN в config.py 
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start и /play
@bot.message_handler(commands=['start', "play"])
def send_welcome(message):
    text = (
        "Отправьте резюме (PDF, DOCX, TXT) или вставьте текст. "
        "Бот проанализирует и вернёт краткий отчёт."
    )
    bot.reply_to(message, text)

# Обработчик прикреплённых документов
@bot.message_handler(content_types=["document"])
def handle_document(message):
    doc = message.document
    # Получаем информацию о файле и скачиваем его
    if not message.document:
        return bot.send_message(message.chat.id, "Файл не получен. Пожалуйста, попробуйте снова.")
    info = bot.get_file(message.document.file_id)

    name = info.file_path.split("/")[-1]
    save_file = bot.download_file(info.file_path)
    with open(name, "wb") as f:
        f.write(save_file)
    fname = doc.file_name.lower()
    try:
        # В зависимости от расширения вызываем соответствующую функцию
        #!f"./{name}"
        if fname.endswith(".pdf"):
            text = extract_text_from_pdf(f"./{name}")
        elif fname.endswith(".docx"):
            text = extract_text_from_docx(f"./{name}")
        #elif fname.endswith(".txt"):
            #text = data.decode(errors="ignore")
        else:
            text ="Формат не поддерживается. Поддерживаются: pdf, docx, txt."
            bot.reply_to(message, text)
            return
    except Exception as e:
        text = f"Ошибка при чтении файла: {e}"
        bot.reply_to(message, text)
        return
    os.remove(f"./{name}") # удаляем файл после обработки
    res = score_resume(text)
    resp = (
        f"*Оценка*: {res['score']} / 100\n"
        f"*Рекомендация*: {res['grade']}\n"
        f"*Опыт (оценка)*: {res['exp']} лет\n"
        f"*Email*: {', '.join(res['emails']) or 'не найден'}\n"
        f"*Телефон*: {', '.join(res['phones']) or 'не найден'}\n"
        f"*Навыки*: {', '.join(res['skills']) or 'не найдены'}\n"
        f"*Примечания*: {'; '.join(res['reasons'])}")
    bot.reply_to(message, resp)

#Обработчик текстовых сообщений — позволяет вставлять резюме как текст@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text
    res = score_resume(text)
    resp = (
        f"*Оценка*: {res['score']} / 100\n"
        f"*Рекомендация*: {res['grade']}\n"
        f"*Опыт (оценка)*: {res['exp']} лет\n"
        f"*Email*: {', '.join(res['emails']) or 'не найден'}\n"
        f"*Телефон*: {', '.join(res['phones']) or 'не найден'}\n"
        f"*Навыки*: {', '.join(res['skills']) or 'не найдены'}\n"
        f"*Примечания*: {'; '.join(res['reasons'])}")
    bot.reply_to(message, resp)

bot.polling()
