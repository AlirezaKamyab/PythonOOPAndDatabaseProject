#!/usr/bin/env python3

class PersonException(ValueError):
    def __init__(self, msg):
        super().__init__(msg)


class Person:
    def __init__(self, **kwargs):
        """Attributes 'name', 'lastname' and 'id' should be given otherwise they are set by default"""

        if 'id' in kwargs: self.id = kwargs['id']
        else: self.id = 0

        if 'name' in kwargs: self.name = kwargs['name']
        else: self.name = ''

        if 'lastname' in kwargs: self.lastname = kwargs['lastname']
        else: self.lastname = ''

    @property
    def id(self): return self._id
    @property
    def name(self): return self._name
    @property
    def lastname(self): return self._lastname

    @id.setter
    def id(self, value):
        if value < 0: raise PersonException("Id cannot be a negative value")
        self._id = value

    @name.setter
    def name(self, value): self._name = value

    @lastname.setter
    def lastname(self, value): self._lastname = value

    def __str__(self):
        return f'#{self.id} {self.name} {self.lastname}'


def main():
    a = Person(name='Alireza', lastname='Kamyab', id=65)
    b = Person(id=66)
    c = Person(lastname='Test')
    print(a)
    print(b)
    print(c)


if __name__ == "__main__": main()