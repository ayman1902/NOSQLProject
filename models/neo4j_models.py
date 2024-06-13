from config import driver


def create_book_author_theme(tx, book_title, author_name, co_author_name, theme):
    tx.run("MERGE (a:Author {name: $author_name}) "
           "MERGE (b:Book {title: $book_title}) "
           "MERGE (c:Theme {name: $theme}) "
           "MERGE (a)-[:WROTE]->(b) "
           "MERGE (b)-[:BELONGS_TO]->(c)",
           author_name=author_name, book_title=book_title, theme=theme)

    if co_author_name:
        tx.run("MERGE (co_a:Author {name: $co_author_name}) "
               "MERGE (b:Book {title: $book_title}) "
               "MERGE (co_a)-[:CO_WROTE]->(b)",
               co_author_name=co_author_name, book_title=book_title)


def add_book_author_theme(book_title, author_name, co_author_name, theme):
    with driver.session() as session:
        session.execute_write(create_book_author_theme, book_title, author_name, co_author_name, theme)


def sync_book_to_neo4j(book):
    author_name = book["author"]
    co_author_name = book.get("co_author")
    book_title = book["title"]
    theme = book["theme"]
    add_book_author_theme(book_title, author_name, co_author_name, theme)
