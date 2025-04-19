from flask import Flask, render_template, request, redirect, url_for
from firebase_config import db
from backend import encrypt, decrypt
import uuid

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    note = request.form['note']
    password = request.form['password'] or 'default-key'
    encrypted_note = encrypt(note, password).decode()
    note_id = str(uuid.uuid4())

    db.collection('notes').document(note_id).set({
        'data': encrypted_note
    })

    return render_template('index.html', link=url_for('view_note', note_id=note_id, _external=True))

@app.route('/note/<note_id>', methods=['GET', 'POST'])
def view_note(note_id):
    doc_ref = db.collection('notes').document(note_id)
    doc = doc_ref.get()

    if not doc.exists:
        return render_template('not_found.html')

    if request.method == 'POST':
        password = request.form['password'] or 'default-key'
        try:
            decrypted_note = decrypt(doc.to_dict()['data'], password)
            doc_ref.delete()  # Auto-delete after viewing
            return render_template('view_note.html', note=decrypted_note)
        except:
            return render_template('view_note.html', error="Incorrect password", show_password=True)

    return render_template('view_note.html', show_password=True)
if __name__ == '__main__':
    app.run(debug=True)
