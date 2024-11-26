Hotel Management System

Acest proiect este o aplicație web pentru gestionarea rezervărilor de camere într-un hotel, construită cu ajutorul Flask. Aplicația include funcționalități pentru utilizatori obișnuiți, cât și pentru administratori, oferind o experiență completă pentru gestionarea rezervărilor, afișarea recenziilor și generarea rapoartelor.

1.Funcționalități

Pentru utilizatori:
- Rezervarea unei camere: Posibilitatea de a rezerva camere de tip Suite, Deluxe, Single sau Family pentru date specificate.
- Validare avansată: Validarea automată a datelor introduse (nume, e-mail, telefon etc.) pentru a preveni erori.
- Primirea confirmării prin e-mail: O confirmare a rezervării este trimisă prin e-mail.
Pentru administratori:
- Autentificare administrativă: Administratorii se pot autentifica pentru a accesa funcționalități avansate.
- Export rapoarte: Generarea de fișiere CSV cu rezervările realizate într-un anumit interval de timp.
Recenzii:
- Afișarea recenziilor: Recenziile lăsate de utilizatori sunt afișate într-o pagină dedicată.
- Adăugarea de recenzii: Funcționalitate pentru introducerea recenziilor direct în baza de date (manual, pentru testare).

2.Tehnologii utilizate
- Backend: Flask (Python)
- Frontend: HTML, CSS (în template-uri Jinja2)
- Bază de date: SQLite
- API pentru e-mailuri: SendGrid

3.Configurare și utilizare
Configurarea mediului:
- Asigură-te că ai instalat Python (v3.7+).

- Configurarea bazei de date:
Rulează scripturile de creare a tabelelor:
python -c "from create_tables import create_table, create_reviews_table; create_table(); create_reviews_table()"

Opțional adaugă date de test în tabele:
python -c "from create_tables import insert_rooms, insert_customer; insert_rooms(); insert_customer()"

- Pornirea aplicației:
Rulează comanda: python main.py
Accesează aplicația în browser la adresa: http://127.0.0.1:5000/.

4.Structura proiectului
main.py: Punctul de intrare al aplicației.
templates/: Conține fișierele HTML pentru interfața utilizator(+CSS).
home.py: Gestionarea paginii de start.
book.py: Logica pentru rezervarea camerelor.
reviews.py: Gestionarea recenziilor.
admin.py: Funcționalități pentru administratori.
reports.py: Exportul de rapoarte CSV.
classes_and_functions.py: Clase și funcții auxiliare, inclusiv validări și trimiterea de e-mailuri.

5.API
- Recenzii
GET /reviews: Returnează recenziile în format JSON.
