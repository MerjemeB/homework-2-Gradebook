# Gradebook CLI

A command-line application for managing students, courses, enrollments, and grades.  
This project demonstrates Python fundamentals including OOP, modules, file I/O, JSON persistence, logging, argument parsing, and unit testing.

---

## 📦 Project Structure

```
gradebook/
├── gradebook/
│   ├── __init__.py
│   ├── models.py
│   ├── storage.py
│   └── service.py
├── main.py
├── tests/
│   ├── __init__.py
│   └── test_service.py
├── scripts/
│   └── seed.py
├── data/
│   └── gradebook.json
├── logs/
│   └── app.log
└── README.md
```

---

## ✅ Features

- Add / list students and courses
- Enroll students into courses
- Add grades and compute averages
- Compute GPA (mean of course averages)
- JSON-based storage with error handling
- Logging to `logs/app.log`
- CLI interface using `argparse`
- Unit tests included (`unittest`)

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/MerjemeB/homework-2-Gradebook.git
cd gradebook
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate        # Windows
```

### 3. Install Dependencies
(No external libraries required, uses standard Python modules.)

```bash
pip install --upgrade pip
```

### 4. (Optional) Seed Sample Data
```bash
python scripts/seed.py
```
This will create example students, courses, and grades in `data/gradebook.json`.

---

## 🚀 Usage

All commands use the main CLI entry script:

```bash
python main.py <command> [options]
```

### Add a Student
```bash
python main.py add-student --name "John Doe"
```

### Add a Course
```bash
python main.py add-course --code CS101 --title "Intro to CS"
```

### Enroll a Student in a Course
```bash
python main.py enroll --student-id 1 --course CS101
```

### Add a Grade
```bash
python main.py add-grade --student-id 1 --course CS101 --grade 95
```

### List Students, Courses, or Enrollments
```bash
python main.py list students
python main.py list students --sort name
python main.py list courses
python main.py list enrollments
```

### Compute Average Grade for a Student in a Course
```bash
python main.py avg --student-id 1 --course CS101
```

### Compute GPA
```bash
python main.py gpa --student-id 1
```

---

## 🧪 Running Tests
```bash
python -m unittest discover tests
```

---

## 📝 Design Decisions & Limitations

- The application uses simple in-memory objects that are serialized to JSON after each operation.
- Student IDs auto-increment sequentially and are not reused.
- GPA is computed as a mean of course averages, not weighted by credit hours.
- Error handling prioritizes user-friendly messages while logging full details to `logs/app.log`.
- The CLI currently supports only basic data operations; advanced searching or editing would be future improvements.

---

## 📄 License
This project is for educational use.
