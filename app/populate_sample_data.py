
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import db, create_app
from app.models import Category, User, Tag

def populate():
    app = create_app()
    with app.app_context():
        # Categorie di esempio
        db.session.add_all([
            Category(name="Matematica"),
            Category(name="Fisica"),
            Category(name="Informatica"),
            Category(name="Chimica"),
            Category(name="Biologia")
        ])

        # Tag di esempio
        db.session.add_all([
            Tag(name="Appunti"),
            Tag(name="Esercizi"),
            Tag(name="Teoria"),
            Tag(name="Esame"),
            Tag(name="Dispensa")
        ])

        # Utente di esempio
        u = User(first_name="Mario", last_name="Rossi", email="mario.rossi@example.com")
        u.set_password("password123")
        db.session.add(u)

        db.session.commit()
        print("Dati di esempio inseriti con successo.")

if __name__ == "__main__":
    populate()
