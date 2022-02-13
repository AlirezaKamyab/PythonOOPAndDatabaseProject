#!/usr/bin/env python3
import person
import user


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

    @credit.setter
    def credit(self, value):
        if value < 0: raise CustomerException("Credit cannot be negative value!")
        self._credit = value

    def buyABook(self, book):
        raise NotImplemented

    def setABookAsCompleted(self, book):
        self.completed.append(book)

    def increaseCredit(self, amount):
        if amount < 0: raise CustomerException("Cannot increase a negative value")
        self.credit += amount


def main():
    pass


if __name__ == "__main__": main()