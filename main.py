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

# Обработчик прикреплённых документов
@bot.message_handler(content_types=["document"])
def handle_document(message):
    doc = message.document
    # Получаем информацию о файле и скачиваем его
    file_info = bot.get_file(doc.file_id)
    file_bytes = bot.download_file(file_info.file_path)
    data = file_bytes.read()
    fname = doc.file_name.lower()
    try:
        # В зависимости от расширения вызываем соответствующую функцию
        if fname.endswith(".pdf"):
            text = extract_text_from_pdf(data)
        elif fname.endswith(".docx"):
            text = extract_text_from_docx(data)
        elif fname.endswith(".txt"):
            text = data.decode(errors="ignore")
        else:
            text ="Формат не поддерживается. Поддерживаются: pdf, docx, txt."
            bot.reply_to(message, text)
            return
    except Exception as e:
        text = f"Ошибка при чтении файла: {e}"
        bot.reply_to(message, text)
        return
    #res = score_resume(text)
    #resp = (
        #f"*Оценка*: {res['score']} / 100\n"
        #f"*Рекомендация*: {res['grade']}\n"
        #f"*Опыт (оценка)*: {res['exp']} лет\n"
        #f"*Email*: {', '.join(res['emails']) or 'не найден'}\n"
       # f"*Телефон*: {', '.join(res['phones']) or 'не найден'}\n"
        #f"*Навыки*: {', '.join(res['skills']) or 'не найдены'}\n"
        #f"*Примечания*: {'; '.join(res['reasons'])}")
    #bot.reply_to(message, resp)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text
    #res = score_resume(text)
    #resp = (
        #f"*Оценка*: {res['score']} / 100\n"
        #f"*Рекомендация*: {res['grade']}\n"
        #f"*Опыт (оценка)*: {res['exp']} лет\n"
        #f"*Email*: {', '.join(res['emails']) or 'не найден'}\n"
                #f"*Телефон*: {', '.join(res['phones']) or 'не найден'}\n"
                #f"*Навыки*: {', '.join(res['skills']) or 'не найдены'}\n"
                #f"*Примечания*: {'; '.join(res['reasons'])}"
            #)
           #message.reply(resp)



bot.polling()
