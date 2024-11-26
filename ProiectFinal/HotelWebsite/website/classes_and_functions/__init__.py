import csv
import re
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
import sqlite3

class Check:
    @staticmethod
    def mail_validation(email):
        email_check = re.match(r'^[a-zA-Z0-9._%+-]+@[a-z]+\.[a-z]{2,}$', email)
        return email_check

    @staticmethod
    def phone_validation(phone):
        phone_check = re.match(r'^[0-9]{10}$', phone)
        return phone_check

    @staticmethod
    def name_validation(name):
        name_check = re.match(r'^[a-zA-Z]{3,}$', name)
        return name_check

    @staticmethod
    def surname_validation(surname):
        surname_check = re.match(r'^[a-zA-Z]{3,}$', surname)
        return surname_check


def send_confirmation_email(api_key, from_email, template_id, to_email, last_name, first_name, check_in, check_out,
                            res_id, room_type, final_price):

    sg = SendGridAPIClient(api_key=api_key)

    email_message = Mail(
        from_email=from_email,
        to_emails=to_email,
    )
    email_message.template_id = template_id
    # Prepare dynamic template data
    email_message.dynamic_template_data = {
        'last_name': last_name,
        'first_name': first_name,
        'id_reservation': res_id,
        'check_in': check_in,
        'check_out': check_out,
        'room': room_type,
        'price': str(final_price)
    }

    try:
        response = sg.send(email_message)
        print(f"Email sent successfully! Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")
        if hasattr(e, 'body'):
            print("Response Body:", e.body)


# send_confirmation_email(
#     api_key='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',
#     from_email='rotarubianca42@gmail.com',
#     template_id='d-3eb9e9eb5e694d8c856ec84904ea1f5a',
#     to_email='rotarubianca42@gmail.com',
#     last_name='Bianca',
#     first_name='Bianca',
#     check_in='2024-12-01',
#     check_out='2024-12-05',
#     res_id='12345',
#     room_type='suite',
#     final_price=200.00
# )
def insert_review():
    """Funcție pentru a introduce review-uri în baza de date."""
    name = input("Introduceți numele: ")
    room = input("Introduceți tipul camerei (single, double, suite): ")
    rating = int(input("Introduceți rating-ul (1-5): "))
    description = input("Introduceți o descriere: ")

    db_path = os.path.join(os.path.dirname(__file__), 'Reviews.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO reviews (name, room, rating, description) VALUES (?, ?, ?, ?)",
            (name, room, rating, description)
        )
        conn.commit()
        print("Review-ul a fost adăugat cu succes!")
    except sqlite3.Error as e:
        print(f"Eroare la baza de date: {e}")
    finally:
        conn.close()


def check_if_admin(user, password):
    valid_password = '123456789'
    valid_user = 'admin'
    if user == valid_user and password == valid_password:
        return True
    else:
        return False


# def generate_csv(start_date, end_date):
#     db_path = os.path.join(os.path.dirname(__file__), 'Hotel.db')
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#
#     query = '''
#         SELECT r.reservation_id, c.name, c.surname, c.email, rm.room_number, r.final_price, r.check_in, r.check_out
#         FROM reservations r
#         JOIN customers c ON r.customer_id = c.customer_id
#         JOIN rooms rm ON r.room_id = rm.room_id
#         WHERE r.check_in >= ? AND r.check_out <= ?
#     '''
#     cursor.execute(query, (start_date, end_date))
#     rows = cursor.fetchall()
#
#     output_file = f'reservations_{start_date}_to_{end_date}.csv'
#
#     with open(output_file, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(['Reservation ID', 'Customer Name', 'Customer Surname', 'Email', 'Room Number', 'Final Price', 'Check-In', 'Check-Out'])
#         writer.writerows(rows)
#
#     conn.close()
#
#     print(f"CSV file created: {output_file}")