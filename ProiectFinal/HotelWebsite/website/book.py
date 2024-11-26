from flask import Blueprint, render_template, request, flash
import sqlite3
import os
from datetime import datetime
from .classes_and_functions import Check, send_confirmation_email

book = Blueprint('book', __name__)


@book.route('/book-now', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        date1 = request.form.get('date1')
        date2 = request.form.get('date2')
        room = request.form.get('room-name')
        phone = request.form.get('phone')
        email = request.form.get('email')

        valid_name = Check.name_validation(firstName)
        valid_surname = Check.surname_validation(lastName)
        valid_mail = Check.mail_validation(email)
        valid_phone = Check.phone_validation(phone)
        valid_room = room.lower()
        room_list = ['suite', 'deluxe', 'single', 'family']

        errors = []
        if not valid_mail:
            errors.append("Invalid email")
        if not valid_name:
            errors.append("Invalid first name")
        if not valid_surname:
            errors.append("Invalid last name")
        if not valid_phone:
            errors.append("Invalid phone number")
        if valid_room not in room_list:
            errors.append("Invalid room, please enter Suite, Deluxe, Single or Family")

        if len(errors) == 0:
            try:
                db_path = os.path.join(os.path.dirname(__file__), 'Hotel.db')
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                cursor.execute('''SELECT email FROM customers WHERE email = ?''', (email,))
                existing_customer = cursor.fetchone()
                print(existing_customer)
                print(existing_customer[0])

                if existing_customer is None:
                    cursor.execute('INSERT INTO customers (name, surname, email, phone) VALUES (?, ?, ?, ?)',
                                   (firstName, lastName, email, phone))
                    customer_id = cursor.lastrowid
                else:
                    cursor.execute('''SELECT customer_id FROM customers WHERE email = ?''', (existing_customer[0],))
                    customer = cursor.fetchone()
                    customer_id = customer[0]

                cursor.execute('''
                SELECT DISTINCT r.room_id
                FROM rooms AS r
                WHERE LOWER(r.room_type) = LOWER(?)
                  AND NOT EXISTS (
                    SELECT 1 
                    FROM reservations AS res
                    WHERE r.room_id = res.room_id
                      AND NOT (
                        res.check_out <= ? OR 
                        res.check_in >= ?
                      )
                  )
                ''', (room, date1, date2))

                available_room = cursor.fetchone()
                if available_room is None:
                    flash('No available rooms for the selected dates.', category='error')
                else:
                    room_id = available_room[0]

                    cursor.execute('''
                                            SELECT price FROM rooms
                                            WHERE LOWER(room_type) = LOWER(?)
                                        ''', (room,))
                    pret = cursor.fetchone()
                    room_price = pret[0]
                    checkin = datetime.strptime(date1, '%Y-%m-%d')
                    checkout = datetime.strptime(date2, '%Y-%m-%d')
                    days_difference = (checkout - checkin).days
                    # print(days_difference)

                    final_price = int(room_price) * int(days_difference)

                    cursor.execute('''
                                        INSERT INTO reservations (check_in, check_out, customer_id, room_id, final_price)
                                        VALUES (?, ?, ?, ?, ?)
                                    ''', (date1, date2, customer_id, room_id, final_price))
                    res_id = cursor.lastrowid

                    conn.commit()
                    send_confirmation_email('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',
                                            'rotarubianca42@gmail.com', 'd-3eb9e9eb5e694d8c856ec84904ea1f5a',
                                            email, lastName, firstName, date1, date2, res_id, room, final_price)
                    flash('Booking successful!', 'success')

            except sqlite3.Error as e:
                flash(f'Error occurred: {e}', 'error')
            finally:
                conn.close()
        else:
            for error in errors:
                flash(error, category='error')

    return render_template('book-now.html')
