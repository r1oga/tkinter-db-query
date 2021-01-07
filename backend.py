import sqlite3

DB = "books.db"


class Database:
    def do_then_commit(func):
        def inner(self, *args, **kwargs):
            result = None
            try:
                result = func(self, *args, **kwargs)
            except Exception as e:
                raise e
            else:
                self.conn.commit()

            return result

        return inner

    @do_then_commit
    def do(self, query, args=()):
        self.cursor.execute(query, args)
        return self.cursor.fetchall()

    def __init__(self, db):
        self.db = db
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, isbn INTEGER)"
            )
        except Exception as e:
            raise e
        else:
            self.conn.commit()

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

    # called when the script is exited
    def __del__(self):
        self.conn.close()


# create_table()
# populate_table([("Li", "r1oga", 2011, 1)])
# delete("retest")
# update(3, "John")
# print(search(author="author2"))
# print(view_all())
