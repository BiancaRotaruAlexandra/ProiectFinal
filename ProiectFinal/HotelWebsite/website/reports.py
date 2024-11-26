from flask import Blueprint, request, render_template, redirect, url_for, flash
import sqlite3
import csv
import os

reports = Blueprint('reports', __name__)


def get_db_path():
    return os.path.join(os.path.dirname(__file__), 'Hotel.db')


# Route for exporting reservations
@reports.route('/export_reservations', methods=['GET', 'POST'])
def export_reservations():
    if request.method == 'POST':

        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if not start_date or not end_date:
            flash('Both start date and end date are required.', category='error')

        try:
            db_path = get_db_path()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Query reservations between the specified dates
            query = """
                SELECT r.reservation_id, c.name, c.surname, c.email, rm.room_number, r.check_in, r.check_out, r.final_price
                FROM reservations r
                JOIN rooms rm ON rm.room_id = r.room_id
                JOIN customers c ON c.customer_id = r.customer_id 
                WHERE r.check_in >= ? AND r.check_out <= ?
            """
            cursor.execute(query, (start_date, end_date))
            rows = cursor.fetchall()
            conn.close()

            # Save results to CSV
            csv_path = os.path.join(os.path.dirname(__file__), f'reservations_{start_date}_to_{end_date}.csv')
            with open(csv_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Reservation ID', 'Name', 'Surname', 'Email', 'Room Number', 'Check-in', 'Check-out', 'Price'])
                writer.writerows(rows)

            flash(f'Reservations exported successfully to {csv_path}.', category='success')
        except Exception as e:
            flash(f'An error occurred: {e}', category='error')
    return render_template('export_reservations.html')
