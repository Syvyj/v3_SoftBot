"""
Модуль для роботи з FAQ та номерами звернень.
"""

import json
import logging
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from difflib import get_close_matches

# Визначаємо шляхи до файлів
DATA_DIR = Path(__file__).parent.parent / "data"
FAQ_PATH = DATA_DIR / "faq.json"
TICKET_FILE = DATA_DIR / "ticket_counter.txt"

# Створюємо директорію для даних, якщо її немає
DATA_DIR.mkdir(exist_ok=True)

def load_faq() -> Dict[str, str]:
    """Завантажує FAQ з файлу"""
    try:
        if not FAQ_PATH.exists():
            return {}
        return json.loads(FAQ_PATH.read_text(encoding='utf-8'))
    except Exception as e:
        logging.error(f"Ошибка загрузки FAQ: {e}")
        return {}

def preprocess_text(text: str) -> List[str]:
    """Підготовка тексту для пошуку"""
    # Переводимо в нижній регістр і розбиваємо на слова
    words = text.lower().split()
    # Видаляємо дуже короткі слова (артиклі, прийменники тощо)
    return [word for word in words if len(word) > 2]

def calculate_similarity(query_words: List[str], faq_words: List[str]) -> float:
    """Розрахунок схожості між запитом та питанням з FAQ"""
    if not query_words or not faq_words:
        return 0.0
    
    matches = 0
    for query_word in query_words:
        for faq_word in faq_words:
            # Перевіряємо чи слово є частиною іншого слова
            if query_word in faq_word or faq_word in query_word:
                matches += 1
                break
    
    # Розраховуємо схожість як відношення знайдених слів до загальної кількості слів у запиті
    return matches / len(query_words)

def find_best_match(question: str, faq: Dict[str, str]) -> Tuple[str, float]:
    """Знаходить найкраще співпадіння в FAQ"""
    query_words = preprocess_text(question)
    best_score = 0.0
    best_key = None
    
    for faq_question in faq.keys():
        faq_words = preprocess_text(faq_question)
        similarity = calculate_similarity(query_words, faq_words)
        
        if similarity > best_score:
            best_score = similarity
            best_key = faq_question
    
    return best_key, best_score

def find_answer(question: str) -> Optional[str]:
    """Пошук відповіді на питання в базі FAQ."""
    if not question:
        return None
    
    faq = load_faq()
    best_match, score = find_best_match(question, faq)
    
    # Якщо схожість більше 0.5 (50%), повертаємо відповідь
    if best_match and score > 0.5:
        return faq[best_match]
    
    return None

def get_next_ticket_number() -> int:
    """Повертає наступний номер звернення"""
    try:
        # Читаємо поточний номер з файлу
        current_number = 1
        if TICKET_FILE.exists():
            current_number = int(TICKET_FILE.read_text().strip() or '0') + 1
        
        # Зберігаємо новий номер
        TICKET_FILE.write_text(str(current_number))
        
        return current_number
    except Exception as e:
        logging.error(f"Error in get_next_ticket_number: {e}")
        return 1  # Повертаємо 1 у випадку помилки 