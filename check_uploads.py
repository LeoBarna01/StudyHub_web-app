import os
from app import create_app, db
from app.models import Document

app = create_app()

with app.app_context():
    upload_folder = app.config['UPLOAD_FOLDER']
    print(f"Checking files in folder: {upload_folder}")
    missing_files = []
    all_docs = Document.query.all()
    for doc in all_docs:
        file_path = os.path.join(upload_folder, doc.filename)
        if not os.path.isfile(file_path):
            missing_files.append((doc.id, doc.title, doc.filename))
            print(f"[MISSING] ID: {doc.id} | Title: {doc.title} | File: {doc.filename}")
            # Remove the orphan document from the database
            db.session.delete(doc)
    db.session.commit()
    print(f"\nTotal documents checked: {len(all_docs)}")
    print(f"Missing and removed files: {len(missing_files)}")
    if missing_files:
        print("\nList of removed files/documents:")
        for doc_id, title, filename in missing_files:
            print(f"ID: {doc_id} | Title: {title} | File: {filename}")
    else:
        print("All files are present.")
    
