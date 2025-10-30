
class Student:
    """Represents a student with ID and name."""
    
    def __init__(self, student_id: int, name: str):
        if not name or not name.strip():
            raise ValueError("Student name cannot be empty")
        if student_id < 1:
            raise ValueError("Student ID must be positive")
            
        self.id = student_id
        self.name = name.strip()
    
    def __str__(self):
        return f"Student(ID: {self.id}, Name: {self.name})"
    
    def __repr__(self):
        return f"Student({self.id}, '{self.name}')"


class Course:
    """Represents a course with code and title."""
    
    def __init__(self, code: str, title: str):
        if not code or not code.strip():
            raise ValueError("Course code cannot be empty")
        if not title or not title.strip():
            raise ValueError("Course title cannot be empty")
            
        self.code = code.strip().upper()
        self.title = title.strip()
    
    def __str__(self):
        return f"Course(Code: {self.code}, Title: {self.title})"
    
    def __repr__(self):
        return f"Course('{self.code}', '{self.title}')"


class Enrollment:
    """Represents a student's enrollment in a course with grades."""
    
    def __init__(self, student_id: int, course_code: str, grades: list = None):
        if student_id < 1:
            raise ValueError("Student ID must be positive")
        if not course_code or not course_code.strip():
            raise ValueError("Course code cannot be empty")
            
        self.student_id = student_id
        self.course_code = course_code.strip().upper()
        self.grades = grades or []
    
    def add_grade(self, grade: float):
        """Add a grade to the enrollment with validation."""
        if not isinstance(grade, (int, float)) or grade < 0 or grade > 100:
            raise ValueError("Grade must be a number between 0 and 100")
        self.grades.append(float(grade))
    
    def get_average(self) -> float:
        """Calculate the average grade for this enrollment."""
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)
    
    def __str__(self):
        avg = self.get_average()
        return f"Enrollment(Student: {self.student_id}, Course: {self.course_code}, Grades: {len(self.grades)}, Avg: {avg:.2f})"
    
    def __repr__(self):
        return f"Enrollment({self.student_id}, '{self.course_code}', {self.grades})"