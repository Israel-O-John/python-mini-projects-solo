from rinet_db_config import get_connection
from datetime import datetime


def main():
    connection = get_connection()
    cursor = connection.cursor()


    try:
        mark = attendance()
        first_name = mark[0].capitalize()
        signin_time = mark[1]
        query = """
            INSERT INTO attendance (staff_id, attendance_date, sign_in_time) SELECT id, CURRENT_DATE, %s
            FROM staff
            WHERE first_name = %s
        """
        cursor.execute(query, (signin_time, first_name))
        connection.commit()
    except Exception as err:
        print(f"error: {err}")
    
    finally:
        cursor.close()
        connection.close()






def attendance():
    first_name = input("What's your first name? ").strip().lower()
    while True:
        sign_in_time_str = input("Sign-in time: HH:MM AM/PM ").strip()
        for time_format in ('%I:%M %p', '%I:%M%p'):
            try:
                valid_time = datetime.strptime(sign_in_time_str, time_format)
                signin_time = valid_time.strftime('%I:%M %p')
                return [first_name, signin_time]
            except ValueError:
                continue
        print("Invalid time format. Please try again.")






if __name__ == "__main__":
    main()