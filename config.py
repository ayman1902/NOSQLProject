import pymongo
from neo4j import GraphDatabase

# Configuration de MongoDB
MONGO_URI = "mongodb://localhost:27017/"
client = pymongo.MongoClient(MONGO_URI)
mongo_db = client["bibliotheque"]
livres_collection = mongo_db["livres"]
adherents_collection = mongo_db["adherents"]
prets_collection = mongo_db["prets"]
users_collection = mongo_db["users"]

# Configuration de Neo4j
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "password"
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
