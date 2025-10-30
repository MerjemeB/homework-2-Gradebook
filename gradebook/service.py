
from typing import List, Dict, Any, Optional
from .models import Student, Course, Enrollment


class GradebookService:
    """Service class handling all different gradebook operations."""
    
    def __init__(self):
        self.students: List[Student] = []
        self.courses: List[Course] = []
        self.enrollments: List[Enrollment] = []
        self._next_student_id = 1
    
    def load_from_dict(self, data: Dict[str, Any]):
        """Load data from dictionary."""
        try:
   
            self.students = [
                Student(student_data['id'], student_data['name'])
                for student_data in data.get('students', [])
            ]
            

            self.courses = [
                Course(course_data['code'], course_data['title'])
                for course_data in data.get('courses', [])
            ]
            

            self.enrollments = [
                Enrollment(
                    enrollment_data['student_id'],
                    enrollment_data['course_code'],
                    enrollment_data.get('grades', [])
                )
                for enrollment_data in data.get('enrollments', [])
            ]
            
            if self.students:
                self._next_student_id = max(s.id for s in self.students) + 1
            else:
                self._next_student_id = 1
                
        except Exception as e:
            raise ValueError(f"Invalid data format: {e}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert current state to dictionary."""
        return {
            "students": [
                {"id": s.id, "name": s.name}
                for s in self.students
            ],
            "courses": [
                {"code": c.code, "title": c.title}
                for c in self.courses
            ],
            "enrollments": [
                {
                    "student_id": e.student_id,
                    "course_code": e.course_code,
                    "grades": e.grades
                }
                for e in self.enrollments
            ]
        }
    
    def add_student(self, name: str) -> int:
        """
        Add a new student to the gradebook.
        
        Args:
            name: Student's name
            
        Returns:
            New student ID
            
        Raises:
            ValueError: If name is invalid
        """
        if not name or not name.strip():
            raise ValueError("Student name cannot be empty")
        
        student_id = self._next_student_id
        student = Student(student_id, name)
        self.students.append(student)
        self._next_student_id += 1
        return student_id
    
    def add_course(self, code: str, title: str):
        """
        Add a new course to the gradebook.
        
        Args:
            code: Course code
            title: Course title
            
        Raises:
            ValueError: If code or title is invalid, or course already exists
        """
        if not code or not code.strip():
            raise ValueError("Course code cannot be empty")
        if not title or not title.strip():
            raise ValueError("Course title cannot be empty")
        
        code = code.strip().upper()
        if any(course.code == code for course in self.courses):
            raise ValueError(f"Course with code {code} already exists")
        
        course = Course(code, title)
        self.courses.append(course)
    
    def enroll(self, student_id: int, course_code: str):
        """
        Enroll a student in a course.
        
        Args:
            student_id: Student ID
            course_code: Course code
            
        Raises:
            ValueError: If student or course doesn't exist, or already enrolled
        """
        student = self._find_student(student_id)
        if not student:
            raise ValueError(f"Student with ID {student_id} not found")
        
        course = self._find_course(course_code)
        if not course:
            raise ValueError(f"Course with code {course_code} not found")
        
        if any(e.student_id == student_id and e.course_code == course_code 
               for e in self.enrollments):
            raise ValueError(f"Student {student_id} is already enrolled in {course_code}")
        
        enrollment = Enrollment(student_id, course_code)
        self.enrollments.append(enrollment)
    
    def add_grade(self, student_id: int, course_code: str, grade: float):
        """
        Add a grade for a student in a course.
        
        Args:
            student_id: Student ID
            course_code: Course code
            grade: Grade value (0-100)
            
        Raises:
            ValueError: If enrollment doesn't exist or grade is invalid
        """
        enrollment = self._find_enrollment(student_id, course_code)
        if not enrollment:
            raise ValueError(f"Student {student_id} is not enrolled in {course_code}")
        
        enrollment.add_grade(grade)
    
    def compute_average(self, student_id: int, course_code: str) -> float:
        """
        Compute average grade for a student in a course.
        
        Args:
            student_id: Student ID
            course_code: Course code
            
        Returns:
            Average grade
            
        Raises:
            ValueError: If enrollment doesn't exist
        """
        enrollment = self._find_enrollment(student_id, course_code)
        if not enrollment:
            raise ValueError(f"Student {student_id} is not enrolled in {course_code}")
        
        return enrollment.get_average()
    
    def compute_gpa(self, student_id: int) -> float:
        """
        Compute GPA for a student (average of all course averages).
        
        Args:
            student_id: Student ID
            
        Returns:
            GPA value
            
        Raises:
            ValueError: If student doesn't exist or has no grades
        """
        if not self._find_student(student_id):
            raise ValueError(f"Student with ID {student_id} not found")
        
        student_enrollments = [
            e for e in self.enrollments 
            if e.student_id == student_id and e.grades
        ]
        
        if not student_enrollments:
            raise ValueError(f"Student {student_id} has no grades")
        
        averages = [e.get_average() for e in student_enrollments]
        return sum(averages) / len(averages)
    
    def list_students(self, sort_by: str = "id") -> List[Student]:
        """List all students, optionally sorted."""
        if sort_by == "name":
            return sorted(self.students, key=lambda s: s.name.lower())
        else:  
            return sorted(self.students, key=lambda s: s.id)
    
    def list_courses(self, sort_by: str = "code") -> List[Course]:
        """List all courses, optionally sorted."""
        if sort_by == "title":
            return sorted(self.courses, key=lambda c: c.title.lower())
        else:  
            return sorted(self.courses, key=lambda c: c.code)
    
    def list_enrollments(self) -> List[Enrollment]:
        """List all enrollments."""
        return self.enrollments
    
    def _find_student(self, student_id: int) -> Optional[Student]:
        """Find student by ID."""
        return next((s for s in self.students if s.id == student_id), None)
    
    def _find_course(self, course_code: str) -> Optional[Course]:
        """Find course by code."""
        return next((c for c in self.courses if c.code == course_code.upper()), None)
    
    def _find_enrollment(self, student_id: int, course_code: str) -> Optional[Enrollment]:
        """Find enrollment by student ID and course code."""
        return next(
            (e for e in self.enrollments 
             if e.student_id == student_id and e.course_code == course_code.upper()),
            None
        )