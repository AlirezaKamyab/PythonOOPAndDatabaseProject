#!/usr/bin/env python3
import manager
from databaseHelper import DatabaseHelper
import book
import customer
import employee


class BookStoreException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class BookStore:
    BOOKS_TABLE = 'Books'
    CUSTOMERS_TABLE = 'Customers'
    EMPLOYEES_TABLE = 'Employees'
    BOOK_INVENTORY_TABLE = 'Inventories'

    def __init__(self, **kwargs):
        """
        Constructs a book store; Table names are optional to specify; it helps to create a better database
        :param kwargs:
        manager: This is required to construct a shop
        databasePath: locates the database to load data from (optional)
        """

        if 'databasePath' in kwargs: self.databasePath = kwargs['databasePath']
        else: self.databasePath = 'database.db'

        if 'manager' in kwargs: self.manager_store = kwargs['manager']
        else: raise BookStoreException('Manager is missing')

        self._books = []
        self._employees = []
        self._customers = []

        self.__initialize()
        self.loadData()

    @property
    def books(self): return self._books
    @property
    def customers(self): return self._customers
    @property
    def employees(self): return self._employees
    @property
    def databasePath(self): return self._databasePath
    @property
    def manager_store(self): return self._manager_store

    @databasePath.setter
    def databasePath(self, value): self._databasePath = value

    @manager_store.setter
    def manager_store(self, value):
        value.id = 1
        self._manager_store = value

        # Search Database
        helper = DatabaseHelper(self.databasePath, self.EMPLOYEES_TABLE)
        lst = list(helper.searchData(id=1))
        if len(lst) == 0:
            helper.insert(id=1, name=value.name, lastname=value.lastname, username=value.username,
                          password=value.password, creationDate=value.creation_date, baseIncome=value.baseIncome,
                          reward=value.reward, penalty=value.penalty, extraTime=value.extraTime, offHours=value.offHours)
        helper.close()

    def __initialize(self):
        """
        This function tries to create tables which are not yet made inside database.
        If the table is existed, it does not create another table.
        :return:
        Nothing
        """

        books = DatabaseHelper(self.databasePath, self.BOOKS_TABLE)
        books.createTable(
            f"""
            CREATE TABLE {self.BOOKS_TABLE} 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            genre TEXT,
            pages INT,
            price INT,
            count INT);
            """)
        books.close()

        customers = DatabaseHelper(self.databasePath, self.CUSTOMERS_TABLE)
        customers.createTable(
            f"""
            CREATE TABLE {self.CUSTOMERS_TABLE}
            (id INTEGER PRIMARY KEY,
            name TEXT,
            lastname TEXT,
            username TEXT,
            password TEXT,
            creationDate TEXT,
            credit INT);
            """)
        customers.close()

        employees = DatabaseHelper(self.databasePath, self.CUSTOMERS_TABLE)
        employees.createTable(
            f"""
            CREATE TABLE {self.EMPLOYEES_TABLE}
            (id INTEGER PRIMARY KEY,
            name TEXT,
            lastname TEXT,
            username TEXT,
            password TEXT,
            creationDate TEXT,
            baseIncome INT,
            reward INT,
            penalty INT,
            extraTime INT,
            offHours INT);
            """)
        employees.close()

        inventories = DatabaseHelper(self.databasePath, self.BOOK_INVENTORY_TABLE)
        inventories.createTable(
            f"""
            CREATE TABLE {self.BOOK_INVENTORY_TABLE}
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INT,
            customer_id INT,
            completed BOOLEAN);
            """)
        inventories.close()

    def loadData(self):
        """
        Fetches data from database and reloads the lists
        """

        books_table = DatabaseHelper(self.databasePath, self.BOOKS_TABLE)
        self.books.clear()
        for bk in books_table.getData():
            temp = book.Book(**bk)
            self.books.append(temp)
        books_table.close()

        customers_table = DatabaseHelper(self.databasePath, self.CUSTOMERS_TABLE)
        self.customers.clear()
        for cus in customers_table.getData():
            temp = customer.Customer(**cus)
            self.customers.append(temp)
        customers_table.close()

        employees_table = DatabaseHelper(self.databasePath, self.EMPLOYEES_TABLE)
        self.employees.clear()
        for emp in employees_table.getData():
            temp = employee.Employee(**emp)
            if temp.id == 1:
                self.manager_store = temp
                temp = manager.Manager(**emp)
            self.employees.append(temp)
        employees_table.close()

        inventory_table = DatabaseHelper(self.databasePath, self.BOOK_INVENTORY_TABLE)
        for inv in inventory_table.getData():
            book_id = inv['book_id']
            customer_id = inv['customer_id']
            completed = inv['completed']

            cus = self.searchCustomer(customer_id)
            bk = self.searchBook(book_id)
            if cus is None: continue
            if bk is None: continue
            cus.books.append(bk)
            if completed: cus.completed.append(bk)
        inventory_table.close()

    def addBook(self, bk):
        books_table = DatabaseHelper(self.databasePath, self.BOOKS_TABLE)
        bk_id = books_table.insert(title=bk.title, author=bk.author, genre=bk.genre, pages=bk.pages, price=bk.price,
                                   count=bk.count)
        books_table.close()

        bk.id = bk_id
        self.books.append(bk)

    def removeBook(self, bookId):
        books_table = DatabaseHelper(self.databasePath, self.BOOKS_TABLE)
        books_table.delete(id=bookId)
        books_table.close()

        for i in range(len(self.books)):
            if self.books[i].id == bookId:
                self.books.pop(i)
                break

    def searchEmployee(self, employeeId):
        for emp in self.employees:
            if emp.id == employeeId: return emp
        return None

    def searchCustomer(self, customerId):
        for cus in self.customers:
            if cus.id == customerId: return cus
        return None

    def searchBook(self, bookId):
        for bk in self.books:
            if bk.id == bookId: return bk
        return None

    def logAsEmployee(self, username : str, password : str):
        for emp in self.employees:
            if emp.username == username and emp.password == password: return emp
        return None

    def logAsCustomer(self, username : str, password : str):
        for cus in self.customers:
            if cus.username == username and cus.password == password: return cus
        return None

    def registerACustomer(self, cus):
        if self.searchCustomer(cus.id) is not None: raise BookStoreException("Id should be a unique value!")
        self.customers.append(cus)

        customer_table = DatabaseHelper(self.databasePath, self.CUSTOMERS_TABLE)
        customer_table.insert(id=cus.id, name=cus.name, lastname=cus.lastname, username=cus.username,
                              password=cus.password, creationDate=cus.creation_date, credit=cus.credit)
        customer_table.close()

    def __iter__(self):
        self._current = 0
        return self

    def __next__(self):
        if self._current >= len(self.books):
            raise StopIteration

        temp = self.books[self._current]
        self._current += 1
        return temp

    @staticmethod
    def load_manager(databasePath):
        helper = DatabaseHelper(databasePath, BookStore.EMPLOYEES_TABLE)
        lst = list(helper.searchData(id=1))
        if len(lst) == 0: return None
        man = manager.Manager(**lst[0])
        return man


def main():
    pass


if __name__ == "__main__": main()