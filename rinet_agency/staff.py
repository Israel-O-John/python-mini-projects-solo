from rinet_db_config import get_connection

def main():
    connection = get_connection()
    cursor = connection.cursor()


    try:
        staff = add_staff()
        last_name = staff[0].capitalize()
        first_name = staff[1].capitalize()
        gender = staff[2].capitalize()
        cursor.execute(
            "INSERT INTO staff(last_name, first_name, gender) VALUES(%s, %s, %s)", (last_name, first_name, gender)
        )
        
        connection.commit()
        
    except Exception as err:
        print(f"error: {err}")
    
    
    finally:
        cursor.close()
        connection.close()

def add_staff():
    last_name = input("What's your last name? ").strip().lower()
    first_name = input("What's your first name? ").strip().lower()
    while True:
        gender = input("Gender? ").strip().lower()
        if gender not in ['male', 'female']:
            continue
        break
    return [last_name, first_name, gender]



if __name__ == "__main__":
    main()