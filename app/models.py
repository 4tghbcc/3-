from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Модель для регистрации нового студента
class StudentRegister(BaseModel):
    full_name: str
    email: str
    group: str
    password: str

# Модель для входа (логин)
class StudentLogin(BaseModel):
    email: str
    password: str

# Модель для отображения информации о студенте
class StudentProfile(BaseModel):
    id: int
    full_name: str
    email: str
    group: str
    balance: float  # текущий баланс (отрицательный = долг)

# Модель для создания платежа
class PaymentCreate(BaseModel):
    amount: float
    description: Optional[str] = "Оплата за обучение"

# Модель для ответа с историей платежей
class PaymentHistory(BaseModel):
    id: int
    student_id: int
    amount: float
    status: str  # "pending", "completed", "failed"
    description: str
    created_at: datetime
