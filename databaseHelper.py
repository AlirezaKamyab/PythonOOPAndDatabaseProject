#!/usr/bin/env python3
import sqlite3


class DatabaseHelper:
    def __init__(self, path, tableName):
        self.path = path
        self.tableName = tableName
        self._db = sqlite3.connect(path)
        self._db.row_factory = sqlite3.Row

    @property
    def tableName(self): return self._tableName
    @property
    def path(self): return self._path

    @tableName.setter
    def tableName(self, value): self._tableName = value
    @path.setter
    def path(self, value): self._path = value

    @path.deleter
    def path(self): self.close()

    def createTable(self, query : str):
        try:
            self._db.execute(query)
        except sqlite3.Error:
            pass

    def dropTable(self):
        self._db.cursor().execute(f"""DROP TABLE IF EXISTS {self.tableName}""")

    def insert(self, **kwargs):
        keys = kwargs.keys()
        values = tuple(kwargs.values())
        keyString = ', '.join(keys)
        placeHolders = '?, ' * len(values)
        placeHolders = placeHolders[:-2]
        query = f"""INSERT INTO {self.tableName} ({keyString}) VALUES ({placeHolders});"""
        cur = self._db.cursor()
        cur.execute(query, values)
        return cur.lastrowid

    def update(self, **kwargs):
        id_value = kwargs['id']
        del kwargs['id']

        placeHolders = ''
        keys = tuple(kwargs.keys())
        values = tuple(kwargs.values())
        for i in range(len(kwargs.keys())):
            placeHolders += f"""{keys[i]} = '{values[i]}', """

        placeHolders = placeHolders[:-2]
        query = f"""UPDATE {self.tableName} SET {placeHolders} WHERE id = {id_value};"""
        self._db.cursor().execute(query)

    def delete(self, **kwargs):
        placeHolders = ''
        keys = tuple(kwargs.keys())
        values = tuple(kwargs.values())

        for i in range(len(keys)):
            placeHolders += f"""{keys[i]} = '{values[i]}' AND """

        placeHolders = placeHolders[:-5]

        query = f"""DELETE FROM {self.tableName} WHERE {placeHolders};"""
        print(query)
        self._db.cursor().execute(query)

    def countRows(self):
        cur = self._db.cursor()
        cur.execute(f"""SELECT COUNT(*) FROM {self.tableName};""")
        return cur.fetchone()[0]

    def getData(self):
        cur = self._db.cursor()
        res = cur.execute(f"""SELECT * FROM {self.tableName};""")
        for r in res:
            yield dict(r)

    def searchData(self, **kwargs):
        placeHolders = ''
        keys = tuple(kwargs.keys())
        values = tuple(kwargs.values())

        for i in range(len(keys)):
            placeHolders += f"""{keys[i]} = '{values[i]}' AND """

        placeHolders = placeHolders[:-5]
        query = f"""SELECT * FROM {self.tableName} WHERE {placeHolders};"""
        cur = self._db.cursor()
        cur.execute(query)
        for r in cur:
            yield r

    def commit(self):
        self._db.commit()

    def close(self):
        self._db.commit()
        self._db.close()


def main():
    dh = DatabaseHelper('test.db', 'Books')
    dh.createTable("""CREATE TABLE Books (id INT PRIMARY KEY,
                        title TEXT,
                        author TEXT,
                        pages INT);""")
    # dh.insert(id='2', title='Harry Potter2', author='J.K Rowling', pages=498)
    # dh.delete(id=1, title="Introduction to algorithms", author='Thomas Corman', pages=1325)
    print(dh.countRows())
    print(list(dh.getData()))
    dh.close()


if __name__ == "__main__": main()