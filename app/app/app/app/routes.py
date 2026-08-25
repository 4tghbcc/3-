from fastapi import APIRouter, HTTPException, Depends, Header
from app.models import StudentRegister, StudentLogin, PaymentCreate, StudentProfile, PaymentHistory
from app.database import students_db, payments_db, get_student_by_email, update_balance, add_payment
from app.security import verify_password, get_password_hash, create_access_token, decode_access_token
from typing import List

router = APIRouter()

# --- Вспомогательная функция для получения текущего студента по токену ---
async def get_current_student(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload or "student_id" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    student_id = payload["student_id"]
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    return students_db[student_id]

# --- 1. Регистрация ---
@router.post("/register", summary="Регистрация нового студента")
async def register_student(student: StudentRegister):
    existing = get_student_by_email(student.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_id = max(students_db.keys()) + 1
    new_student = {
        "id": new_id,
        "full_name": student.full_name,
        "email": student.email,
        "group": student.group,
        "password_hash": get_password_hash(student.password),
        "balance": 0.0
    }
    students_db[new_id] = new_student
    return {"message": "Student registered successfully", "student_id": new_id}

# --- 2. Логин (получение JWT) ---
@router.post("/login", summary="Вход в систему")
async def login_student(student: StudentLogin):
    db_student = get_student_by_email(student.email)
    if not db_student or not verify_password(student.password, db_student["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(data={"student_id": db_student["id"]})
    return {"access_token": access_token, "token_type": "bearer"}

# --- 3. Получение профиля и баланса ---
@router.get("/profile", response_model=StudentProfile, summary="Получение профиля и баланса")
async def get_profile(current_student: dict = Depends(get_current_student)):
    return StudentProfile(
        id=current_student["id"],
        full_name=current_student["full_name"],
        email=current_student["email"],
        group=current_student["group"],
        balance=current_student["balance"]
    )

# --- 4. История платежей ---
@router.get("/payments", response_model=List[PaymentHistory], summary="История всех платежей")
async def get_payment_history(current_student: dict = Depends(get_current_student)):
    student_id = current_student["id"]
    history = [p for p in payments_db if p["student_id"] == student_id]
    return history

# --- 5. Создание нового платежа (инициация оплаты) ---
@router.post("/payments", summary="Инициация платежа")
async def create_payment(payment: PaymentCreate, current_student: dict = Depends(get_current_student)):
    student_id = current_student["id"]
    # В реальной системе здесь был бы шлюз. Мы просто добавляем запись.
    new_payment = add_payment(student_id, payment.amount, payment.description)
    # В демо-версии сразу подтверждаем платеж и меняем баланс
    new_payment["status"] = "completed"
    update_balance(student_id, payment.amount)
    return {"message": "Payment successful", "payment_id": new_payment["id"], "new_balance": current_student["balance"]}
