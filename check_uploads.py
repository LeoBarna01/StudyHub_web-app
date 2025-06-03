import os
from app import create_app, db
from app.models import Document

app = create_app()

with app.app_context():
    upload_folder = app.config['UPLOAD_FOLDER']
    print(f"Controllo file nella cartella: {upload_folder}")
    missing_files = []
    all_docs = Document.query.all()
    for doc in all_docs:
        file_path = os.path.join(upload_folder, doc.filename)
        if not os.path.isfile(file_path):
            missing_files.append((doc.id, doc.title, doc.filename))
            print(f"[MANCANTE] ID: {doc.id} | Titolo: {doc.title} | File: {doc.filename}")
            # Rimuovo il documento orfano dal database
            db.session.delete(doc)
    db.session.commit()
    print(f"\nTotale documenti controllati: {len(all_docs)}")
    print(f"File mancanti e rimossi: {len(missing_files)}")
    if missing_files:
        print("\nElenco file/documenti rimossi:")
        for doc_id, title, filename in missing_files:
            print(f"ID: {doc_id} | Titolo: {title} | File: {filename}")
    else:
        print("Tutti i file sono presenti.") 