from datetime import datetime
import hashlib

# Эмулируем таблицу студентов
students_db = {
    1: {
        "id": 1,
        "full_name": "Иванов Иван Иванович",
        "email": "ivanov@synergy.ru",
        "group": "ИНФ-21",
        "password_hash": hashlib.sha256("secure123".encode()).hexdigest(),
        "balance": -15000.0  # отрицательный баланс = задолженность
    },
    2: {
        "id": 2,
        "full_name": "Петрова Анна Сергеевна",
        "email": "petrova@synergy.ru",
        "group": "МЕН-22",
        "password_hash": hashlib.sha256("qwerty".encode()).hexdigest(),
        "balance": 5000.0  # положительный = переплата
    }
}

# Эмулируем таблицу платежей
payments_db = [
    {
        "id": 1,
        "student_id": 1,
        "amount": 30000.0,
        "status": "completed",
        "description": "Оплата за 1 семестр 2025",
        "created_at": datetime(2025, 9, 1, 10, 30)
    },
    {
        "id": 2,
        "student_id": 1,
        "amount": 15000.0,
        "status": "pending",
        "description": "Оплата за 2 семестр 2026",
        "created_at": datetime(2026, 1, 15, 14, 20)
    },
    {
        "id": 3,
        "student_id": 2,
        "amount": 25000.0,
        "status": "completed",
        "description": "Оплата за год обучения",
        "created_at": datetime(2025, 8, 25, 9, 0)
    }
]

# Автоинкремент для новых платежей
next_payment_id = 4

# Вспомогательные функции
def get_student_by_email(email: str):
    for student in students_db.values():
        if student["email"] == email:
            return student
    return None

def update_balance(student_id: int, amount: float):
    if student_id in students_db:
        students_db[student_id]["balance"] += amount
        return True
    return False

def add_payment(student_id: int, amount: float, description: str):
    global next_payment_id
    new_payment = {
        "id": next_payment_id,
        "student_id": student_id,
        "amount": amount,
        "status": "pending",  # сначала pending, потом подтверждается
        "description": description,
        "created_at": datetime.now()
    }
    payments_db.append(new_payment)
    next_payment_id += 1
    return new_payment
