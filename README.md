# 🏊 Pool Management System

A minimal working application to manage swimming pool groups with support for roles: **Administrator**, **Instructor**, and **Visitor**.

## 📌 Tech Stack

- Python (3.10+)
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic (migrations)
- Pytest (tests)

## 📚 Features

### 👨‍🏫 Instructor

- Must work a **fixed number of hours** per week
- Has **preferred working hours** (time slots)

### 👨‍💼 Administrator

- Can **create groups** and **assign instructors**
- While assigning instructors:
  - Can view current instructor availability
  - Checks for time conflicts with preferred hours
  - Can **sort instructors** by load (overloaded instructors are **hidden**)
- Can **change group instructors**

### 👤 Visitor

- Can view groups
- Can register in one group
- Group has:
  - **Maximum number of participants**
  - **Gender-based limitations** (based on changing room size)

### 👥 Group

- Has participant limits
- Enforces male/female limits based on facilities

---

## ⚙️ Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/haroyan001/Task_Pool.git
cd Task_Pool
```
### 2. Setup and install dependencies
```bash
python -m venv venv
```
```bash
pip install -r requirements.txt
```
### 3. Start the project
```bash
python run.py
```

## Swagger UI is available at: http://localhost:8000/docs

### Testing
- Run tests

```bash
pytest tests/
```
