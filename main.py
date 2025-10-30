#!/usr/bin/env python3
"""
Gradebook CLI - Command-line interface for managing students, courses, and grades.
"""
import argparse
import sys
import logging
from gradebook.storage import load_data, save_data, setup_logging
from gradebook.service import GradebookService


def parse_grade(grade_str: str) -> float:
    """
    Parse and validate grade input.
    
    Args:
        grade_str: Grade as string
        
    Returns:
        Parsed grade as float
        
    Raises:
        ValueError: If grade is invalid
    """
    try:
        grade = float(grade_str)
        if grade < 0 or grade > 100:
            raise ValueError("Grade must be between 0 and 100")
        return grade
    except ValueError as e:
        raise ValueError(f"Invalid grade '{grade_str}': must be a number between 0 and 100")


def main():
    """Main CLI entry point."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Load data and initialize service
    try:
        data = load_data()
        service = GradebookService()
        service.load_from_dict(data)
    except Exception as e:
        logger.error(f"Failed to initialize gradebook: {e}")
        print(f"Error: Failed to initialize gradebook: {e}")
        return 1
    
    parser = argparse.ArgumentParser(description="Gradebook CLI")
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    parser_add_student = subparsers.add_parser('add-student', help='Add a new student')
    parser_add_student.add_argument('--name', required=True, help='Student name')
    
    parser_add_course = subparsers.add_parser('add-course', help='Add a new course')
    parser_add_course.add_argument('--code', required=True, help='Course code')
    parser_add_course.add_argument('--title', required=True, help='Course title')
    
    parser_enroll = subparsers.add_parser('enroll', help='Enroll student in course')
    parser_enroll.add_argument('--student-id', type=int, required=True, help='Student ID')
    parser_enroll.add_argument('--course', required=True, help='Course code')
    
    parser_add_grade = subparsers.add_parser('add-grade', help='Add grade for student in course')
    parser_add_grade.add_argument('--student-id', type=int, required=True, help='Student ID')
    parser_add_grade.add_argument('--course', required=True, help='Course code')
    parser_add_grade.add_argument('--grade', required=True, help='Grade (0-100)')
    
    parser_list = subparsers.add_parser('list', help='List students, courses, or enrollments')
    parser_list.add_argument('type', choices=['students', 'courses', 'enrollments'], 
                           help='What to list')
    parser_list.add_argument('--sort', choices=['name', 'code', 'title', 'id'], 
                           help='Sort by field')
    
    parser_avg = subparsers.add_parser('avg', help='Compute average grade for student in course')
    parser_avg.add_argument('--student-id', type=int, required=True, help='Student ID')
    parser_avg.add_argument('--course', required=True, help='Course code')
    
    parser_gpa = subparsers.add_parser('gpa', help='Compute GPA for student')
    parser_gpa.add_argument('--student-id', type=int, required=True, help='Student ID')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    try:
        if args.command == 'add-student':
            student_id = service.add_student(args.name)
            print(f"Added student: ID={student_id}, Name='{args.name}'")
            
        elif args.command == 'add-course':
            service.add_course(args.code, args.title)
            print(f"Added course: Code={args.code.upper()}, Title='{args.title}'")
            
        elif args.command == 'enroll':
            service.enroll(args.student_id, args.course)
            print(f"Enrolled student {args.student_id} in course {args.course.upper()}")
            
        elif args.command == 'add-grade':
            grade = parse_grade(args.grade)
            service.add_grade(args.student_id, args.course, grade)
            print(f"Added grade {grade} for student {args.student_id} in course {args.course.upper()}")
            
        elif args.command == 'list':
            if args.type == 'students':
                students = service.list_students(args.sort or 'id')
                if not students:
                    print("No students found")
                else:
                    print("Students:")
                    for student in students:
                        print(f"  {student}")
                        
            elif args.type == 'courses':
                courses = service.list_courses(args.sort or 'code')
                if not courses:
                    print("No courses found")
                else:
                    print("Courses:")
                    for course in courses:
                        print(f"  {course}")
                        
            elif args.type == 'enrollments':
                enrollments = service.list_enrollments()
                if not enrollments:
                    print("No enrollments found")
                else:
                    print("Enrollments:")
                    for enrollment in enrollments:
                        print(f"  {enrollment}")
            
        elif args.command == 'avg':
            average = service.compute_average(args.student_id, args.course)
            print(f"Average for student {args.student_id} in {args.course.upper()}: {average:.2f}")
            
        elif args.command == 'gpa':
            gpa = service.compute_gpa(args.student_id)
            print(f"GPA for student {args.student_id}: {gpa:.2f}")
        
        # Save data after successful operation
        save_data(service.to_dict())
        
    except ValueError as e:
        logger.error(f"Validation error in {args.command}: {e}")
        print(f"Error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error in {args.command}: {e}")
        print(f"Unexpected error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())