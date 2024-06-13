from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from functools import wraps

from flask_login import login_required
from BDNOSQL import authenticate_user
from routes.books import books_bp
from routes.adherents import adherents_bp
from routes.prets import prets_bp
from models.mongo_models import get_all_adherents, add_adherent, delete_all_adherents, add_pret

app = Flask(__name__)

# Enregistrer les Blueprints
app.register_blueprint(books_bp)
app.register_blueprint(adherents_bp)
app.register_blueprint(prets_bp)
app.secret_key = '2b8e5d4f7e3c8b1a5d2f6e4c7a1b3d2e'

# Route pour la page d'accueil
@app.route('/')
def index():
    print(session.get('logged_in'))
    return render_template('index.html')

# Route pour afficher la page HTML des livres
@app.route('/books')
def books():
    return render_template('books.html')

# Route pour afficher les adhérents
@app.route('/adherents/html')
def adherents_page():
    print(session.get('logged_in'))
    if(session.get('logged_in') == True ):
        return render_template('adherents.html')
    else:
        return redirect(url_for('index'))

# Route pour afficher les prêts
@app.route('/prets/html')
@login_required
def prets():
    return render_template('prets.html')

# Route pour la page de connexion
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    data = request.form
    username = data['username']
    password = data['password']
    if authenticate_user(username, password):
        session['username'] = username
        session['logged_in'] = True  # Set session variable to indicate user is logged in
        flash('Login successful', 'success')
        return redirect(url_for('index'))
    else:
        flash('Invalid credentials', 'danger')
        return redirect(url_for('login_page'))

# Route pour la déconnexion
@app.route('/logout')
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))
# Route pour obtenir tous les adhérents
@app.route('/adherents', methods=['GET'])
def get_adherents():
    adherents = get_all_adherents()
    return jsonify(adherents)

# Route pour ajouter un adhérent
@app.route('/adherents', methods=['POST'])
def create_adherent():
    adherent_data = request.json
    add_adherent(adherent_data)
    return jsonify({"message": "Adherent added successfully"}), 201

# Route pour supprimer tous les adhérents
@app.route('/adherents', methods=['DELETE'])
def delete_all_adherents_route():
    delete_count = delete_all_adherents()
    return jsonify({"deleted_count": delete_count})

# Route pour ajouter un prêt
@app.route('/prets', methods=['POST'])
def create_pret():
    pret_data = request.json
    add_pret(pret_data)
    return jsonify({"message": "Loan added successfully"}), 201

@app.route('/gerer_books', methods=['GET'])
def gerer_books():
    return render_template('gerer_books.html')
if __name__ == '__main__':
    app.run(debug=True)
