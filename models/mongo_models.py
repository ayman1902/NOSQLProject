from config import livres_collection, adherents_collection, prets_collection, users_collection
from bson.objectid import ObjectId


def add_book(book):
    # Check if the book with the same title and author already exists
    if livres_collection.find_one({"title": book.get("title"), "author": book.get("author")}):
        return "Book with the same title and author already exists."

    result = livres_collection.insert_one(book)
    return result.inserted_id


def add_adherent(adherent):
    result = adherents_collection.insert_one(adherent)
    return result.inserted_id


def add_pret(pret):
    result = prets_collection.insert_one(pret)
    return result.inserted_id


def add_user(user):
    result = users_collection.insert_one(user)
    return result.inserted_id


def authenticate_user(username, password):
    user = users_collection.find_one({"username": username, "password": password})
    return user is not None


def get_all_books():
    return list(livres_collection.find())


def get_all_adherents():
    return list(adherents_collection.find({}, {'_id': 0}))


def get_all_prets():
    prets = list(prets_collection.find())
    for pret in prets:
        pret['_id'] = str(pret['_id'])  # Convert ObjectId to string for JSON
    return prets


def delete_all_books():
    result = livres_collection.delete_many({})
    return result.deleted_count


def delete_adherent_by_id(adherent_id):
    result = adherents_collection.delete_one({"_id": ObjectId(adherent_id)})
    return result.deleted_count


def delete_pret_by_id(pret_id):
    result = prets_collection.delete_one({"_id": ObjectId(pret_id)})
    return result.deleted_count


def delete_all_adherents():
    adherents_collection.delete_many({})
