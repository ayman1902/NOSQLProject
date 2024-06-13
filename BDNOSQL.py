import pymongo
from neo4j import GraphDatabase

# Connexion à MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["bibliotheque"]
livres_collection = db["livres"]
livres_collection.create_index([("isbn", 1)], unique=True)
adherents_collection = db["adherents"]
prets_collection = db["prets"]
users_collection = db["users"]

# Connexion à Neo4J
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

def create_book_author(tx, book_title, author_name):
    tx.run("MERGE (a:Author {name: $author_name}) "
           "MERGE (b:Book {title: $book_title}) "
           "MERGE (a)-[:WROTE]->(b)", author_name=author_name, book_title=book_title)

def add_book_author(book_title, author_name):
    with driver.session() as session:
        session.execute_write(create_book_author, book_title, author_name)

def add_book(book):
    livres_collection.insert_one(book)

def add_adherent(adherent):
    adherents_collection.insert_one(adherent)

def add_pret(pret):
    prets_collection.insert_one(pret)

def add_user(user):
    users_collection.insert_one(user)

def authenticate_user(username, password):
    with driver.session() as session:
        result = session.run("MATCH (u:User {username: $username, password: $password}) RETURN count(u) AS count", username=username, password=password)
        return result.single()["count"] > 0
def add_user(username, password):
    with driver.session() as session:
        session.run("CREATE (:User {username: $username, password: $password})", username=username, password=password)
#add_user("ayman","JS5")
#add_user("lt","nadi")

###################################################################################""""""""""""""""""""""
def sync_book_to_neo4j(book_id):
    book = livres_collection.find_one({"_id": book_id})
    author_name = book["author"]
    book_title = book["title"]
    add_book_author(book_title, author_name)
###########################################################################################~ééééééé
def sync_all_books():
    books = livres_collection.find()
    for book in books:
        sync_book_to_neo4j(book["_id"])

def print_livres_collection():
    livres = livres_collection.find()
    for livre in livres:
        print(livre)

# Exemples de données
def insert_example_data():
    # Effacer les collections existantes
    livres_collection.delete_many({})
    adherents_collection.delete_many({})
    prets_collection.delete_many({})
    users_collection.delete_many({})

    # Insérer les nouvelles données


    adherents_collection.insert_many([
        {
            "_id": "1",
            "name": "Adherent Name 1",
            "email": "adherent1@example.com",
            "phone": "1234567890"
        },
        {
            "_id": "2",
            "name": "Adherent Name 2",
            "email": "adherent2@example.com",
            "phone": "0987654321"
        }
    ])

    prets_collection.insert_many([
        {
            "_id": "1",
            "book_id": "1",
            "adherent_id": "1",
            "date_pret": "2024-01-01",
            "date_retour": "2024-01-15"
        },
        {
            "_id": "2",
            "book_id": "2",
            "adherent_id": "2",
            "date_pret": "2024-02-01",
            "date_retour": "2024-02-15"
        }
    ])

    users_collection.insert_many([
        {
            "_id": "1",
            "username": "user1",
            "password": "password1"
        },
        {
            "_id": "2",
            "username": "user2",
            "password": "password2"
        }
    ])

# Insérer les données d'exemple
insert_example_data()

# Synchroniser les livres avec Neo4J
sync_all_books()

# Imprimer la collection de livres
print("Contenu de la collection 'livres' :")
print_livres_collection()

# Exemple d'authentification d'utilisateur
username = "user1"
password = "password1"
if authenticate_user(username, password):
    print(f"Authentification réussie pour l'utilisateur {username}")
else:
    print(f"Échec de l'authentification pour l'utilisateur {username}")

driver.close()
client.close()
