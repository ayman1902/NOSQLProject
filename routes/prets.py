from flask import Blueprint, request, jsonify, render_template
from models.mongo_models import add_pret, get_all_prets, delete_pret_by_id

prets_bp = Blueprint('prets', __name__)

# Route pour récupérer tous les prêts
@prets_bp.route('/prets', methods=['GET'])
def get_prets():
    try:
        prets = get_all_prets()
        return jsonify(prets), 200
    except Exception as e:
        print(f"Erreur lors de la récupération des prêts: {e}")
        return jsonify({"error": "Erreur lors de la récupération des prêts"}), 500

# Route pour ajouter un nouveau prêt
@prets_bp.route('/prets', methods=['POST'])
def create_pret():
    try:
        pret_data = request.json
        add_pret(pret_data)
        return jsonify({"message": "Pret added successfully"}), 201
    except Exception as e:
        print(f"Erreur lors de l'ajout du prêt: {e}")
        return jsonify({"error": "Erreur lors de l'ajout du prêt"}), 500

# Route pour supprimer un prêt par son identifiant
@prets_bp.route('/prets/<id>', methods=['DELETE'])
def delete_pret(id):
    try:
        deleted_count = delete_pret_by_id(id)
        if deleted_count:
            return jsonify({"message": "Pret deleted successfully"}), 200
        else:
            return jsonify({"message": "Pret not found"}), 404
    except Exception as e:
        print(f"Erreur lors de la suppression du prêt: {e}")
        return jsonify({"error": "Erreur lors de la suppression du prêt"}), 500

# Route pour afficher les prêts sur une page HTML
@prets_bp.route('/prets/html', methods=['GET'])
def get_prets_html():
    try:
        prets = get_all_prets()
        return render_template('prets.html', prets=prets)
    except Exception as e:
        print(f"Erreur lors de l'affichage des prêts: {e}")
        return render_template('error.html', error="Erreur lors de l'affichage des prêts")
