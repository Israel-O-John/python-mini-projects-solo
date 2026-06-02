import json
import secrets

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
    },
}


def main():
    
    
    student_a = create_student_basic()

# loop over the student class and modify specific class based on student_a class
    for class_name, class_details in student_classes.items():
        if class_name == student_a["student_class"]:
            student_a["subjects"] = [*class_details["class subjects"]]
            student_a["subjects_details"] = {
                subject: {
                    "test": 0,
                    "assignments": 0,
                    "projects": 0,
                    "exam": 0,
                    "total": 0,
                }
                for subject in student_a["subjects"]
            }
            student_a["subjects_details"] = score_entry(student_a["subjects_details"])
            class_details["students"].append(student_a)
            
    
    print(json.dumps(student_a["subjects_details"], indent=4))
    


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
        "Guardian mail",
        "Date of Birth(YYYY-MM-DD)",
        "Guardian name",
        "student_class",
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




if __name__ == "__main__":
    main()