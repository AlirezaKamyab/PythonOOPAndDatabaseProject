#!/usr/bin/env python3

class BookStoreException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class BookStore:
    def __init__(self, **kwargs):
        if 'manager' in kwargs: self.manager = kwargs['manager']
        else: raise BookStoreException('Manager is missing')

        if 'databasePath' in kwargs: self.databasePath = kwargs['databasePath']
        else: self.databasePath = 'database.db'

        self._books = []
        self._employees = []
        self._customers = []

    @property
    def books(self): return self._books
    @property
    def customers(self): return self._customers
    @property
    def employees(self): return self._employees

    def addBook(self, book):
        raise NotImplemented

    def removeBook(self, bookId):
        raise NotImplemented

    def searchEmployee(self, employeeId):
        for emp in self.employees:
            if emp.id == employeeId: return emp
        return None

    def searchCustomer(self, customerId):
        for cus in self.customers:
            if cus.id == customerId: return cus
        return None

    def searchBook(self, bookId):
        for book in self.books:
            if book.id == bookId: return book
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
        # update database
        raise NotImplemented
    

def main():
    pass


if __name__ == "__main__": main()