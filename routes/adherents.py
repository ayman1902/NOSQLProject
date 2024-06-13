from flask import Blueprint, request, jsonify, render_template
from models.mongo_models import add_adherent, get_all_adherents, delete_adherent_by_id

adherents_bp = Blueprint('adherents', __name__)

# Route pour récupérer tous les adhérents
@adherents_bp.route('/adherents', methods=['GET'])
def get_adherents():
    adherents = get_all_adherents()
    return jsonify(adherents)

# Route pour ajouter un nouvel adhérent
@adherents_bp.route('/adherents', methods=['POST'])
def create_adherent():
    adherent_data = request.json
    add_adherent(adherent_data)
    return jsonify({"message": "Adherent added successfully"}), 201

# Route pour supprimer un adhérent par son identifiant
@adherents_bp.route('/adherents/<id>', methods=['DELETE'])
def delete_adherent(id):
    deleted_count = delete_adherent_by_id(id)
    if deleted_count:
        return jsonify({"message": "Adherent deleted successfully"}), 200
    else:
        return jsonify({"message": "Adherent not found"}), 404

# Route pour afficher les adhérents sur une page HTML
@adherents_bp.route('/adherents/html', methods=['GET'])
def get_adherents_html():
    adherents = get_all_adherents()
    return render_template('adherents.html', adherents=adherents)


