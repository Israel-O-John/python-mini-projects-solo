import json
import secrets
from tabulate import tabulate
from base_data import student_classes_data as classes_data


student_classes = {}
SCORE_LIMITS = {
    "test": 25,
    "assignments": 10,
    "projects": 15,
    "exam": 40,
}


def main():

    global student_classes
    student_classes = base_file_config()

    users = ["admin", "teacher", "student"]
    menu = (
        input("What's your role in this system? ADMIN | TEACHER | STUDENT:\n")
        .lower()
        .strip()
    )

    # a guard clause against inputs from user not in the users list
    if not menu in users:
        print(f"{menu.capitalize()} not recognised in this system!")

    if menu == "admin":
        while True:
            task = (
            input(
                "What operation do you intend to render? Student Management | Teacher Management | Check database | Exit:\n"
            )
            .lower()
            .strip()
        )
            match task:
                case "check database":
                    # table_formatted_database()
                    print(json.dumps(student_classes, indent=4))
                case "student management":
                    student_management_sys()
                case "teacher management":
                    teacher_management_sys()
                case "exit":
                    break
                case _:
                    print(f"{task} operation not recognised")


    if menu == "teacher":
        while True:
            task = (
            input(
                "What operation do you intend to render? View Students | Edit scores | Exit:\n"
            )
            .lower()
            .strip()
        )
            match task:
                case "view students":
                    view_students()
                case "edit scores":
                    teacher_scores_entry()
                case _:
                    print(f"{task} operation is either not on this system or not within your juristiction")


    if menu == "student":
        print(json.dumps(student_classes, indent=4))
        get_report_card()


def student_management_sys():
    while True:
            task = (
            input(
                "What operation do you intend to render? Add Student | Delete student | Update Student data | Exit:\n"
            )
            .lower()
            .strip()
        )
            match task:
                case "add student":
                    add_student_to_class()
                case "delete student":
                    delete_student()
                case "update student data":
                    update_student_data()
                case "exit":
                    break
                case _:
                    print(f"{task} operation not recognised")


def teacher_management_sys():
    while True:
            task = (
            input(
                "What operation do you intend to render? Add Teacher | Delete Teacher | Update Teacher data | Exit:\n"
            )
            .lower()
            .strip()
        )
            match task:
                case "add teacher":
                    create_teacher()
                case "delete teacher":
                    delete_teacher()
                case "update teacher data":
                    update_teacher_data()
                case "exit":
                    break
                case _:
                    print(f"{task} operation not recognised")
    
    
    
    
    
    
def base_file_config():
    # checking if file exists
    try:
        with open("school_database.json", "r") as database_file:
            student_classes = json.load(database_file)
    except FileNotFoundError:
        student_classes = classes_data
    return student_classes


def save_to_file():
    with open("school_database.json", "w") as database_file:
        json.dump(student_classes, database_file, indent=4)


def find_class_by_condition(condition_func):
    for class_name, class_details in student_classes.items():
        if condition_func(class_name, class_details):
            return class_name, class_details
    return None, None


# Creates a student and add student to specified class
def add_student_to_class(transfer_student=None):
    if transfer_student == None:
        student = create_student_basic()
    else:
        student = transfer_student

    _, class_details = find_class_by_condition(
        lambda name, details: name == student["student class"]
    )

    if class_details:
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
        print(
            f"{student_full_name.capitalize()} has been succesfully added to the system with a student ID of {student_sch_id}"
        )
        save_to_file()


def create_teacher():
    PREFIX = "TEACH-"
    teach_name = input("Full Name: ")
    secure_gen = secrets.SystemRandom()
    random_number = secure_gen.randint(10000, 100000)
    teach_id = f"{PREFIX}{random_number}"

    class_name, class_details = find_class_by_condition(
        lambda name, details: details["teacher"] == ""
    )

    if class_details:
        class_details["teacher"] = teach_name
        class_details["teacher_id"] = teach_id
        print(
            f"{teach_name.capitalize()} is assigned to class {class_name.capitalize()}"
        )
        save_to_file()
    else:
        print("No vacancy! All classes have a teacher")


def delete_teacher():
    print("Delete Teacher")


def update_teacher_data():
    print("Update Teacher Data")

def view_students():
    teacher_id = input("Input your ID: ")

    _, class_details = find_class_by_condition(
        lambda name, details: details["teacher_id"] == teacher_id
    )
    if class_details:
        print(class_details["students"])
        return
    else:
        print(f"{teacher_id} does not match any ID in the system")
        return


def get_report_card():
    student_class = input("Student class: ").lower()
    student_id = input("Input ID: ")

    _, class_details = find_class_by_condition(
        lambda name, details: name == student_class
        and student_id in details["report_cards"].keys()
    )
    if class_details:
        print(class_details["report_cards"][student_id])
    else:
        print("ERROR: Input Valid Class and Student ID")


# gets a student and updates the student scores
def teacher_scores_entry():
    teacher_id = input("What's your ID? ").strip()

    class_name, class_details = find_class_by_condition(
        lambda name, details: details["teacher_id"] == teacher_id
    )


    if class_details:
        student_id = input("Student ID: ").strip()
        student, _, _ = find_student(student_id)

        if student is not None:
            try:
                student["subjects_details"] = score_entry(student["subjects_details"])
                student["teachers_remark"] = input("Your remark on this student: ")
                class_details["report_cards"][student_id] = generate_report_card(
                    student
                )
                save_to_file()
            except Exception as err:
                print(f"An error occurred while entering scores: {err}")
        else:
            print(f"No student found with ID {student_id} in {class_name}")
    else:
        print(f"No class found registered under Teacher ID: {teacher_id}")


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
                    if score < 0 or score > SCORE_LIMITS[criteria]:
                        print(f"{criteria} score is in range of 1 to {SCORE_LIMITS[criteria]}")
                        continue
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

    class_name, class_details = find_class_by_condition(
        lambda name, details: any(
            s["student_id"] == student_id for s in details["students"]
        )
    )

    if class_details:
        for student in class_details["students"]:
            if student["student_id"] == student_id:
                return (student, class_name, class_details)

    return None, None, None


def view_student_details(student_id=None):
    if student_id is None:
        student_id = input("Student ID: ").strip()
    else:
        student_id = str(student_id).strip()

    student, _, _ = find_student(student_id)
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

    student, _, _ = find_student(student_id)
    if student is None:
        print(f"Student with ID:{student_id} does not exist on the system.")
        return

    class_name, class_details = find_class_by_condition(
        lambda name, details: student in details["students"]
    )
    if class_details:
        class_details["students"].remove(student)
        print(
            f"Student with ID:{student_id} in {class_name.capitalize()} has been removed from the system."
        )
        save_to_file()
        return


def update_student_data():
    student, class_name, class_details = find_student()
    if student == None and class_name == None and class_details == None:
        print("Student does not exist on the system")
        return


    changes = input("Edit Info | Change class \n").strip().lower()
    if changes == "edit info":
        change_type_sys = [
            "guardian name",
            "guardian mail",
            "surname",
            "first name",
            "middle name",
        ]
        usr_change = input("what to change? \n").strip().lower()
        if usr_change in change_type_sys:
            change = input(f"Input {usr_change}: ").strip().lower()
            student[usr_change] = change
            save_to_file()
            print(f"{usr_change} update has been effected.")
        else:
            print("Such operation not recognised!")
    elif changes == "change class":
        new_class = input("Transfer to Class: ").strip().lower()
        new_class_name, new_class_details = find_class_by_condition(
            lambda name, details: new_class == name
        )
        if new_class_name == None:
            print("That class does not exist!")
            return
        else:
            class_details["students"].remove(student)
            student["student class"] = new_class_name
            add_student_to_class(student)
            save_to_file()
    else:
        print("ERROR: Choose operation to perform from the listed")


def table_formatted_database():
    return "Love"

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
