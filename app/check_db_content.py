import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from app.models import Category, User, Tag

app = create_app()
with app.app_context():
    print('Categorie:', [c.name for c in Category.query.all()])
    print('Tag:', [t.name for t in Tag.query.all()])
    print('Utenti:', [u.email for u in User.query.all()])
