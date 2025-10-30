"""
Unit tests for GradebookService.
"""
import unittest
import tempfile
import json
import os
from gradebook.service import GradebookService


class TestGradebookService(unittest.TestCase):
    """Test cases for GradebookService."""
    
    def setUp(self):
        """Set up a fresh service instance for each test."""
        self.service = GradebookService()
    
    def test_add_student_success(self):
        """Test adding a student successfully."""
        student_id = self.service.add_student("John Doe")
        self.assertEqual(student_id, 1)
        self.assertEqual(len(self.service.students), 1)
        self.assertEqual(self.service.students[0].name, "John Doe")
        self.assertEqual(self.service.students[0].id, 1)
    
    def test_add_student_invalid_name(self):
        """Test adding a student with invalid name."""
        with self.assertRaises(ValueError):
            self.service.add_student("")
        with self.assertRaises(ValueError):
            self.service.add_student("   ")
    
    def test_add_course_success(self):
        """Test adding a course successfully."""
        self.service.add_course("CS101", "Introduction to Computer Science")
        self.assertEqual(len(self.service.courses), 1)
        self.assertEqual(self.service.courses[0].code, "CS101")
        self.assertEqual(self.service.courses[0].title, "Introduction to Computer Science")
    
    def test_add_course_duplicate(self):
        """Test adding a duplicate course."""
        self.service.add_course("CS101", "Introduction to Computer Science")
        with self.assertRaises(ValueError):
            self.service.add_course("CS101", "Another Course")
    
    def test_enroll_and_add_grade_success(self):
        """Test enrolling a student and adding grades."""
        # Setup
        student_id = self.service.add_student("Jane Smith")
        self.service.add_course("MATH101", "Calculus I")
        
        # Enroll
        self.service.enroll(student_id, "MATH101")
        
        # Add grade
        self.service.add_grade(student_id, "MATH101", 85.5)
        
        # Verify
        enrollment = self.service._find_enrollment(student_id, "MATH101")
        self.assertIsNotNone(enrollment)
        self.assertEqual(len(enrollment.grades), 1)
        self.assertEqual(enrollment.grades[0], 85.5)
    
    def test_compute_average_success(self):
        """Test computing average grade."""

        student_id = self.service.add_student("Alice Johnson")
        self.service.add_course("PHY101", "Physics I")
        self.service.enroll(student_id, "PHY101")
        

        self.service.add_grade(student_id, "PHY101", 80)
        self.service.add_grade(student_id, "PHY101", 90)
        
   
        average = self.service.compute_average(student_id, "PHY101")
        self.assertEqual(average, 85.0)
    
    def test_compute_average_no_grades(self):
        """Test computing average with no grades."""
        student_id = self.service.add_student("Bob Brown")
        self.service.add_course("CHEM101", "Chemistry I")
        self.service.enroll(student_id, "CHEM101")
        
        average = self.service.compute_average(student_id, "CHEM101")
        self.assertEqual(average, 0.0)
    
    def test_compute_gpa_success(self):
        """Test computing GPA with multiple courses."""
        student_id = self.service.add_student("Charlie Wilson")
        
      
        self.service.add_course("CS101", "CS Intro")
        self.service.add_course("MATH101", "Calculus")
        self.service.enroll(student_id, "CS101")
        self.service.enroll(student_id, "MATH101")
        

        self.service.add_grade(student_id, "CS101", 80)  
        self.service.add_grade(student_id, "CS101", 80)
        self.service.add_grade(student_id, "MATH101", 90)  
        
        gpa = self.service.compute_gpa(student_id)
        self.assertEqual(gpa, 85.0)
    
    def test_compute_gpa_no_grades(self):
        """Test computing GPA when student has no grades."""
        student_id = self.service.add_student("Diana Prince")
        
        with self.assertRaises(ValueError):
            self.service.compute_gpa(student_id)


if __name__ == '__main__':
    unittest.main()