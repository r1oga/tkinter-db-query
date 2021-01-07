import sqlite3

DB = "books.db"


def connect_then_close(func):
    def inner(db=DB, *args, **kwargs):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        result = None
        try:
            result = func(cursor, *args, **kwargs)
        except Exception as e:
            raise e
        else:
            conn.commit()
        finally:
            conn.close()

        return result

    return inner


@connect_then_close
def do(cursor, query, args=()):
    cursor.execute(query, args)
    return cursor.fetchall()


def create_table():
    do(
        query="CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, isbn INTEGER)"
    )


def populate_table(records):
    for record in records:
        # syntax to avoid sql injection attack
        do(query=f"INSERT INTO books VALUES (NULL, ?, ?, ?, ?)", args=record)


def view_all():
    return do(query="SELECT * FROM books")


def delete(id):
    do(query="DELETE FROM books WHERE id=?", args=(id,))


def search(title="", author="", year="", isbn=""):
    args = [title, author, year, isbn]
    return do(
        query="SELECT * FROM books WHERE title=? OR author=? OR year=? OR isbn=?",
        args=args,
    )


def update(id, *args):
    title, author, year, isbn = do(query="SELECT * FROM books WHERE id=?", args=(id,))[
        0
    ][1:]
    attrs = [title, author, year, isbn]
    new_attrs = []

    for i, attr in enumerate(attrs):
        try:
            new_attrs.append(args[i])
        except:
            new_attrs.append(attr)

    do(
        query="UPDATE books SET title=?, author=?, year=?, isbn=? WHERE id=?",
        args=[*new_attrs, id],
    )


# create_table()
# populate_table([("Li", "r1oga", 2011, 1)])
# delete("retest")
# update(3, "John")
# print(search(author="author2"))
# print(view_all())
