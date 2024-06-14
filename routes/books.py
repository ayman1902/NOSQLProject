from flask import Blueprint, request, jsonify, render_template
from models.mongo_models import add_book, get_all_books, delete_all_books, get_books_count
from models.neo4j_models import sync_book_to_neo4j
from bson import ObjectId  # Add this import

books_bp = Blueprint('books', __name__)

def serialize_book(book):
    """Convert MongoDB book document to JSON-serializable format."""
    serialized_book = {
        "title": book["title"],
        "author": book["author"],
        "co_author": book.get("co_author"),
        "isbn": book["isbn"],
        "image_url": book.get("image_url"),
        "theme": book["theme"]
    }
    if "_id" in book:
        serialized_book["id"] = str(book["_id"])  # Convert ObjectId to string
    return serialized_book

# This route returns JSON data
@books_bp.route('/api/books', methods=['GET'])
def get_books():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        skip = (page - 1) * limit

        books = get_all_books(skip=skip, limit=limit)
        serialized_books = [serialize_book(book) for book in books]

        # Get the total count of books
        total_books = get_books_count()
        total_pages = (total_books + limit - 1) // limit

        return jsonify({
            "books": serialized_books,
            "total_books": total_books,
            "total_pages": total_pages,
            "current_page": page
        })
    except ValueError:
        return jsonify({"message": "Invalid page or limit value"}), 400

# This route adds a new book
@books_bp.route('/api/books', methods=['POST'])
def create_book():
    book_data = request.json
    inserted_id = add_book(book_data)  # Get the inserted ObjectId
    if isinstance(inserted_id, str):
        return jsonify({"message": inserted_id}), 400  # If there's an error message, return it

    book_data["_id"] = str(inserted_id)  # Convert ObjectId to string
    sync_book_to_neo4j(book_data)
    return jsonify({"message": "Book added successfully"}), 201

# This route deletes all books
@books_bp.route('/api/books', methods=['DELETE'])
def delete_books():
    deleted_count = delete_all_books()
    return jsonify({"message": f"Deleted {deleted_count} books"}), 200

# New route to manage books and authors
@books_bp.route('/gerer_books', methods=['GET'])
def manage_books():
    return render_template('gerer_books.html')
