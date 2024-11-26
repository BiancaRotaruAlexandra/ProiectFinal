from flask import Blueprint, request, jsonify
import sqlite3
import os

reviews = Blueprint('reviews', __name__)


@reviews.route("/reviews", methods=['GET'])
def get_reviews():
    db_path = os.path.join(os.path.dirname(__file__), 'Reviews.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reviews")
    reviews_db = cursor.fetchall()
    conn.close()

    reviews_list = []
    for row in reviews_db:
        review = {
            "review_id": row[0],
            "name": row[1],
            "room": row[2],
            "rating": row[3],
            "description": row[4],
        }
        reviews_list.append(review)
    return jsonify(reviews_list)


def insert_review():
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
