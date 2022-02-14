#!/usr/bin/env python3
import person
import user
import bookStore
from databaseHelper import DatabaseHelper


class CustomerException(ValueError):
    def __init__(self, msg):
        super().__init__(msg)


class Customer(person.Person, user.User):
    def __init__(self, **kwargs):
        """
        Use 'balance' attribute to set balance
        Use 'name', 'lastname', 'id' to construct Person
        Use 'username' and 'password' to construct User
        """

        if 'credit' in kwargs: self.credit = kwargs['credit']
        else: self.credit = 0

        if 'store' in kwargs: self.store = kwargs['store']
        else: self.store = None

        self._books = []
        self._completed = []
        person.Person.__init__(self, **kwargs)
        user.User.__init__(self, **kwargs)

    @property
    def books(self): return self._books
    @property
    def completed(self): return self._completed
    @property
    def credit(self): return self._credit
    @property
    def store(self): return self._store

    @credit.setter
    def credit(self, value):
        if value < 0: raise CustomerException("Credit cannot be negative value!")
        self._credit = value

    @store.setter
    def store(self, value): self._store = value

    def buyABook(self, bk):
        if bk.count <= 0: raise CustomerException("Book is out of stock!")
        if bk.price > self.credit: raise CustomerException("Insufficient credit!")

        # Update books table from database
        book_table = DatabaseHelper(self.store.databasePath, self.store.BOOKS_TABLE)
        bk.count -= 1
        book_table.update(id=bk.id, count=bk.count)
        book_table.close()

        # Update Inventory table from database
        inventory_table = DatabaseHelper(self.store.databasePath, self.store.BOOK_INVENTORY_TABLE)
        inventory_table.insert(customer_id=self.id, book_id=bk.id, completed=False)
        inventory_table.close()

        self.credit -= bk.price
        # Update customer table from database
        customer_table = DatabaseHelper(self.store.databasePath, self.store.CUSTOMERS_TABLE)
        customer_table.update(id=self.id, credit=self.credit)
        customer_table.close()

        # add to the list
        self.books.append(bk)

    def setABookAsCompleted(self, bk):
        self.completed.append(bk)

        # Update database
        helper = DatabaseHelper(self.store.databasePath, self.store.BOOK_INVENTORY_TABLE)
        lst = [helper.searchData(book_id=bk.id, customer_id=self.id)]
        data = lst[0]
        data['completed'] = True
        helper.update(**data)
        helper.close()

    def increaseCredit(self, amount):
        if amount < 0: raise CustomerException("Cannot increase a negative value")
        self.credit += amount

        # Update database
        helper = DatabaseHelper(self.store.databasePath, self.store.CUSTOMERS_TABLE)
        helper.update(id=self.id, credit=self.credit)
        helper.close()


def main():
    pass


if __name__ == "__main__": main()