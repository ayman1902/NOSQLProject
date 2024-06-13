from config import driver

def create_book_author(tx, book_title, author_name):
    tx.run("MERGE (a:Author {name: $author_name}) "
           "MERGE (b:Book {title: $book_title}) "
           "MERGE (a)-[:WROTE]->(b)", author_name=author_name, book_title=book_title)

def add_book_author(book_title, author_name):
    with driver.session() as session:
        session.execute_write(create_book_author, book_title, author_name)

def sync_book_to_neo4j(book):
    author_name = book["author"]
    book_title = book["title"]
    add_book_author(book_title, author_name)
