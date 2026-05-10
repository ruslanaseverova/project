#pip install pdfminer.six
import os
from pdfminer.high_level import extract_text
#import docx
import io

# Функция для извлечения текста из DOCX.
# Принимает путь или байты файла. Возвращает строку текста.
def extract_text_from_docx(path_or_bytes):
    if isinstance(path_or_bytes, (bytes, bytearray)):
        # Если пришли байты — используем BytesIO для чтения через python-docx
        doc = docx.Document(io.BytesIO(path_or_bytes))
    else:
        # Иначе передали путь к файлу
        doc = docx.Document(path_or_bytes)
    full = []
    # Собираем текст из всех параграфов
    for p in doc.paragraphs:
        full.append(p.text)
    return "\n".join(full)

# Функция для извлечения текста из PDF.
# Если переданы байты — временно сохраняем файл и используем pdfminer.
def extract_text_from_pdf(path_or_bytes):
    if isinstance(path_or_bytes, (bytes, bytearray)):
        # Создаем временный файл PDF
        with open("temp_resume.pdf", "wb") as f:
            f.write(path_or_bytes)
        # Извлекаем текст
        text = extract_text("temp_resume.pdf")
        # Удаляем временный файл
        os.remove("temp_resume.pdf")
        return text
    else:
        # Если передали путь к файлу
        return extract_text(path_or_bytes)
