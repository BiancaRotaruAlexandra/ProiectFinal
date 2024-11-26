from flask import Blueprint, render_template, request, flash, redirect, url_for
from .classes_and_functions import check_if_admin


administrator = Blueprint('administrator', __name__)


@administrator.route('/administrator', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        user = request.form.get('username')

        check = check_if_admin(user, password)
        if check:
            return redirect(url_for('reports.export_reservations'))
        else:
            flash("Invalid username or password", category='error')
    return render_template('admin.html')
