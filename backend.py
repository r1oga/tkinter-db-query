import sqlite3

DB = "books.db"


class Database:
    def connect_then_close(func):
        def inner(self, db=DB, *args, **kwargs):
            conn = sqlite3.connect(db)
            cursor = conn.cursor()
            result = None
            try:
                result = func(self, cursor, *args, **kwargs)
            except Exception as e:
                raise e
            else:
                conn.commit()
            finally:
                conn.close()

            return result

        return inner

    @connect_then_close
    def do(self, cursor, query, args=()):
        cursor.execute(query, args)
        return cursor.fetchall()

    @connect_then_close
    def __init__(self, cursor):
        self.do(
            query="CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, isbn INTEGER)"
        )

    def create_table(self):
        self.do(
            query="CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, isbn INTEGER)"
        )

    def populate_table(self, records):
        for record in records:
            # syntax to avoid sql injection attack
            self.do(query=f"INSERT INTO books VALUES (NULL, ?, ?, ?, ?)", args=record)

    def view_all(self):
        return self.do(query="SELECT * FROM books")

    def delete(self, id):
        self.do(query="DELETE FROM books WHERE id=?", args=(id,))

    def search(self, title="", author="", year="", isbn=""):
        args = [title, author, year, isbn]
        return self.do(
            query="SELECT * FROM books WHERE title=? OR author=? OR year=? OR isbn=?",
            args=args,
        )

    def update(self, id, *args):
        title, author, year, isbn = self.do(
            query="SELECT * FROM books WHERE id=?", args=(id,)
        )[0][1:]
        attrs = [title, author, year, isbn]
        new_attrs = []

        for i, attr in enumerate(attrs):
            try:
                new_attrs.append(args[i])
            except:
                new_attrs.append(attr)

        self.do(
            query="UPDATE books SET title=?, author=?, year=?, isbn=? WHERE id=?",
            args=[*new_attrs, id],
        )


# create_table()
# populate_table([("Li", "r1oga", 2011, 1)])
# delete("retest")
# update(3, "John")
# print(search(author="author2"))
# print(view_all())
