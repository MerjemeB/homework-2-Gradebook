#!/usr/bin/env python3
"""
Seed script to populate the gradebook some sample data
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from gradebook.storage import save_data
from gradebook.service import GradebookService


def create_sample_data():
    """Create sample gradebook data."""
    service = GradebookService()
    

    students = [
        ("Alice Johnson", 1),
        ("Bob Smith", 2), 
        ("Carol Davis", 3)
    ]
    
    for name, expected_id in students:
        student_id = service.add_student(name)
        assert student_id == expected_id, f"Expected ID {expected_id}, got {student_id}"
    

    courses = [
        ("GIT101", "Git & GitHub"),
        ("PY201", "Python Essentials 2"),
        ("PY101", "Python Essentials 1")
    ]
    
    for code, title in courses:
        service.add_course(code, title)
    
 
    enrollments = [
        (1, "GIT101", [85, 90, 88]),
        (1, "PY201", [92, 95, 90]),
        (2, "GIT101", [78, 82, 80]),
        (2, "PY101", [85, 88, 90]),
        (3, "PY201", [90, 92, 94]),
        (3, "PY101", [87, 85, 89])
    ]
    
    for student_id, course_code, grades in enrollments:
        service.enroll(student_id, course_code)
        for grade in grades:
            service.add_grade(student_id, course_code, grade)
    
    return service.to_dict()


if __name__ == '__main__':
    print("Creating sample gradebook data...")
    
    data = create_sample_data()
    success = save_data(data)
    
    if success:
        print("Sample data created successfully!")
        print(f"Created {len(data['students'])} students")
        print(f"Created {len(data['courses'])} courses") 
        print(f"Created {len(data['enrollments'])} enrollments")
        print("Data saved to data/gradebook.json")
    else:
        print("Failed to save sample data")
        sys.exit(1)