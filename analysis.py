import re

# Регулярные выражения для поиска email и телефона.
EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_RE = re.compile(r"(\+?\d[\d\-\s]{6,}\d)")

# Список ключевых навыков для простого поиска в тексте.
SKILLS_KEYWORDS = [
    "python", "java", "javascript", "c++", "c#", "go", "sql", "django",
    "flask", "react", "aws", "docker", "kubernetes", "machine learning",
    "ml", "tensorflow", "pytorch", "nlp", "git"
]

# Поиск контактных данных: emails и телефоны.
# Возвращает уникальные списки.
def find_contacts(text):
    emails = EMAIL_RE.findall(text)
    phones = PHONE_RE.findall(text)
    return list(set(emails)), list(set(phones))

# Поиск навыков по ключевым словам.
# Сравниваем в нижнем регистре.
def find_skills(text):
    low = text.lower()
    found = [kw for kw in SKILLS_KEYWORDS if kw in low]
    return found

# Простая эвристика для оценки опыта.
# Ищет явное указание лет ("X years", "X лет") или слова junior/mid/senior.
def estimate_experience(text):
    # Ищем числа перед словами "years/year/лет/года/год"
    m = re.findall(r"(\d{1,2})\s*(?:years|year|лет|года|год)", text.lower())
    if m:
        # Берем максимальное число (иногда указаны периоды)
        years = max(int(x) for x in m)
        return years
    # Если явных лет нет — пробуем по уровням
    if "senior" in text.lower() or "sr." in text.lower():
        return 6
    if "mid" in text.lower() or "middle" in text.lower():
        return 3
    if "junior" in text.lower() or "jr." in text.lower():
        return 1
    # Если ничего не найдено — возвращаем 0
    return 0

# Оценка резюме по простым критериям.
# Возвращает словарь с оценкой, категорией и найденными полями.
def score_resume(text):
    emails, phones = find_contacts(text)
    skills = find_skills(text)
    exp = estimate_experience(text)

    score = 0
    reasons = []

    # Наличие email добавляет баллы
    if emails:
        score += 20
    else:
        reasons.append("Нет email")

    # Наличие телефона добавляет баллы
    if phones:
        score += 15
    else:
        reasons.append("Нет телефона")

    # Навыки: по 5 баллов за найденный навык, максимум 30
    score += min(30, len(skills) * 5)
    if skills:
        reasons.append(f"Найдено навыков: {len(skills)}")

    # Опыт: более 5 лет — много баллов, 2-4 — средне, иначе мало
    if exp >= 5:
        score += 25
        reasons.append(f"Опыт ~{exp} лет")
    elif exp >= 2:
        score += 10
        reasons.append(f"Опыт ~{exp} лет")
    else:
        reasons.append("Мало явного опыта")

    # Оценка по порогам
    grade = "Не рекомендую"
    if score >= 70:
        grade = "Рекомендую"
    elif score >= 40:
        grade = "Нужны уточнения"

    return {
        "score": score,
        "grade": grade,
        "emails": emails,
        "phones": phones,
        "skills": skills,
        "exp": exp,
        "reasons": reasons
    }