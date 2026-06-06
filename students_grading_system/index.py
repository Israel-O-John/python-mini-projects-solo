import json
import secrets
from tabulate import tabulate

student_classes = {
    "primary 1": {
        "total attendance": 4,
        "total projects": 5,
        "teacher": "",
        "teacher_id": "",
        "class subjects": [
            "English studies",
            "Mathematics",
        ],
        "students": [],
        "report_cards": {},
    },
    "primary 2": {
        "total attendance": 5,
        "total projects": 2,
        "teacher": "",
        "teacher_id": "",
        "class subjects": [
            "English studies",
            "Mathematics",

        ],
        "students": [],
        "report_cards": {},
    },
    "primary 3": {
        "total attendance": 9,
        "total projects": 4,
        "teacher": "",
        "teacher_id": "",
        "class subjects": [
            "English studies",
            "Mathematics",

        ],
        "students": [],
        "report_cards": {},
    },
    "primary 4": {
        "total attendance": 20,
        "total projects": 5,
        "teacher": "",
        "teacher_id": "",
        "class subjects": [
            "English studies",
            "Mathematics",
        ],
        "students": [],
        "report_cards": {},
    },
    "primary 5": {
        "total attendance": 30,
        "total projects": 4,
        "teacher": "",
        "teacher_id": "",
        "class subjects": [
            "English studies",
            "Mathematics",
        ],
        "students": [],
        "report_cards": {},
    },
    "primary 6": {
        "total attendance": 60,
        "total projects": 3,
        "teacher": "",
        "teacher_id": "",
        "class subjects": [
            "English studies",
            "Mathematics",
        ],
        "students": [],
        "report_cards": {},
    },
}


def main():
    users = ["admin", "teacher", "student"]
    menu = input("What's your role in this system? ADMIN | TEACHER | STUDENT:\n").lower().strip()

    # a guard clause against inputs from user not in the users list
    if not menu in users:
        print(f"{menu.capitalize()} not recognised in this system!")


    if menu == "admin":
        task = input("What operation do you intend to render? Add Student | Add Teacher | Check database:\n").lower().strip()
        if task == "add teacher":
            print("~~~~ Adding Teacher ~~~~")
            create_teacher()
        elif task == "add student":
            print("~~~~ Adding Student ~~~~")
            
            """
            for testing purpose
            for _ in range(2):
                add_student_to_class()
            student_1 = find_student()
            student_2 = find_student()
            print(student_1, student_2)
            """
            
            add_student_to_class()
            add_student_to_class()
            
            # student_1 = find_student()
            # print(json.dumps(student_1, indent=4))
            
            # student_1 = view_student_details()
            # print(student_1)
            
            
            print(json.dumps(student_classes, indent=4))
            delete_student()
            print(json.dumps(student_classes, indent=4))
        elif task == "check database":
            print(json.dumps(student_classes, indent=4))
        else:
            print(f"{task} operation not recognised!")


    if menu == "teacher":
        task = input("What operation do you intend to render? View Students | Edit scores:\n").lower().strip()
        if task == "view students":
            view_students()
        elif task == "edit scores":
            teacher_scores_entry()
        else:
            print(f"{task} operation is either not on this system or not within your juristiction")


    if menu == "student":
        print(json.dumps(student_classes, indent=4))
        get_report_card()





# Creates a student and add student to specified class
def add_student_to_class():
    student = create_student_basic()
    for class_name, class_details in student_classes.items():
        if class_name == student["student class"]:
            student["subjects"] = [*class_details["class subjects"]]
            student["subjects_details"] = {
                subject: {
                    "test": 0,
                    "assignments": 0,
                    "projects": 0,
                    "exam": 0,
                    "total": 0,
                }
                for subject in student["subjects"]
            }
            class_details["students"].append(student)
            
            student_full_name = f"{student["surname"]} {student["first name"]}"
            student_sch_id = f"{student["student_id"]}"
            print(f"{student_full_name.capitalize()} has been succesfully added to the system with a student ID of {student_sch_id}")


def create_teacher():
    PREFIX = "TEACH-"
    teach_name = input("Full Name: ")
    secure_gen = secrets.SystemRandom()
    random_number = secure_gen.randint(10000, 100000)
    teach_id = f"{PREFIX}{random_number}"
    
    assigned = False
    for classes_names, classes_details in student_classes.items():
        if classes_details["teacher"] == "":
            classes_details["teacher"] = teach_name
            classes_details["teacher_id"] = teach_id
            print(f"{teach_name.capitalize()} is assigned to class {classes_names.capitalize()}")
            assigned = True
            break

        
    if not assigned:
        print("No vacancy! All classes have a teacher")


def view_students():
    teacher_id = input("Input your ID: ")
    for classes_names, classes_details in student_classes.items():
        if classes_details["teacher_id"] == teacher_id:
            print(classes_details["students"])
            return
        else:
            print(f"{teacher_id} does not match any ID in the system")
            return


def get_report_card():
    student_class = input("Student class: ").lower()
    student_id = input("Input ID: ")
    
    for classes_names, classes_details in student_classes.items():
        if classes_names == student_class and student_id in classes_details["report_cards"].keys():
            print(classes_details["report_cards"][student_id])
        else:
            print("ERROR: Input Valid Class and Student ID")


# gets a student and updates the student scores
def teacher_scores_entry():
    teacher_id = input("What's your ID? ")
    for class_name, class_details in student_classes.items():
        if "teacher_id" not in class_details or "students" not in class_details:
            continue

        if class_details["teacher_id"] == teacher_id:
            student_id = input("Student ID: ")
            # student = next((student for student in class_details["students"] if student.get("student_id") == student_id), None)
            student = find_student(student_id)
        
            if student is not None:
                try:
                    student["subjects_details"] = score_entry(student["subjects_details"])
                    student["teachers_remark"] = input("Your remark on this student: ")
                    class_details["report_cards"][student_id] = generate_report_card(student)
                    break
                except Exception as err:
                    print(f"An error occurred while entering scores: {err}")
            else:
                print(f"No student found with ID {student_id} in {class_name}")



# Asks for students basic info and assigns student an id
def create_student_basic():
    # generate random id
    PREFIX = "STU-"
    secure_gen = secrets.SystemRandom()
    random_number = secure_gen.randint(10000, 100000)

    # basic info to ask student to provide
    basic_question = [
        "Surname",
        "First Name",
        "Middle name",
        "Date of Birth(YYYY-MM-DD)",
        "Student class",
        "Guardian name",
        "Guardian mail",
    ]
    basic_info = {
        info.lower(): input(f"What's your {info}? ").lower() for info in basic_question
    }

    # merges the basic info with additional key and value pair
    basic_info |= {"student_id": f"{PREFIX}{random_number}"}

    # returns a dict of student info
    return basic_info

    # create a student a



def score_entry(subjects_details):
    for subject_name, assessments in subjects_details.items():
        print(f"\n Entering scores for {subject_name}")

        for criteria in assessments.keys():
            if criteria == "total":
                continue

            while True:
                raw_score = input(f"Enter {criteria} score: ")
                try:
                    score = float(raw_score)
                    assessments[criteria] = score
                    break
                except ValueError:
                    print("Invalid input")

        assessments["total"] = (
            assessments["test"]
            + assessments["assignments"]
            + assessments["projects"]
            + assessments["exam"]
        )
        
        assessments["grade"] = student_grade(assessments["total"])
    return subjects_details


def student_grade(score):
    if not 0 <= score <= 100:
        return "Invalid score"
    if score >= 75:
        return "A1"
    elif score >= 70:
        return "B2" 
    elif score >= 65:
        return "B3" 
    elif score >= 60:
        return "C4" 
    elif score >= 55:
        return "C5" 
    elif score >= 50:
        return "C6" 
    elif score >= 45:
        return "D7" 
    elif score >= 40:
        return "E8" 
    else:
        return "F9" 


def find_student(student_id=None):
    # this is, so the func can be called both with an ID passed as a parameter or not passed
    if student_id is None:
        student_id = input("Student ID: ").strip()
    else:
        student_id = str(student_id).strip()
    
    
    for class_name, class_details in student_classes.items():
        student = next((s for s in class_details["students"] if s["student_id"] == student_id), None)
        
        if student:
            return student
        
    return None



def view_student_details(student_id=None):
    if student_id is None:
        student_id = input("Student ID: ").strip()
    else:
        student_id = str(student_id).strip()
    

    student = find_student(student_id)
    if student is None:
        return f"Student with ID:{student_id} does not exist on the system"
    
    student_full_name = f"{student['surname'].capitalize()} {student['first name'].capitalize()} {student['middle name'].capitalize()}"
    
    return f"""
Name: {student_full_name}
ID: {student["student_id"]}
Class: {student["student class"].capitalize()}
Date of Birth: {student["date of birth(yyyy-mm-dd)"]}
Guardian Name: {student["guardian name"].capitalize()}
Guardian Mail: {student["guardian mail"]}
Subjects: {student["subjects"]}
"""


def delete_student(student_id=None):
    if student_id is None:
        student_id = input("Student ID: ").strip()
    else:
        student_id = str(student_id).strip()

    student = find_student(student_id)
    if student is None:
        print(f"Student with ID:{student_id} does not exist on the system.")
        return
    
    for class_name, class_details in student_classes.items():
        if student in class_details["students"]:
            class_details["students"].remove(student)
            print(f"Student with ID:{student_id} in {class_name.capitalize()} has been removed from the system.")
            return




def generate_report_card(student):
    headers = ["Subject", "Test", "Assignments", "Projects", "Exam", "Total", "Grade"]
    table_data = []
    
    
    for subject, details in student["subjects_details"].items():
        row = [
            subject.title(),
            details.get("test", 0.0),
            details.get("assignments", 0.0),
            details.get("projects", 0.0),
            details.get("exam", 0.0),
            details.get("total", 0.0),
            details.get("grade", "N/A"),
        ]
        table_data.append(row)
    
    score_table = tabulate(table_data, headers=headers)
    
    
    
    return f"""
    ~~~~~ OFFOR COMPREHENSIVE PRIMARY SCHOOL ~~~~~
            ADDRESS: PO BOX 63922
            
    NAME:  {student["surname"].capitalize()} {student["first name"].capitalize()} {student["middle name"].capitalize()}
    CLASS: {student["student_class"].title()}
    ID:    {student["student_id"]}
    
{score_table}

~~~~~ Teacher's remark: {student["teacher_remark"]} ~~~~~~
    """

if __name__ == "__main__":
    main()