#!/usr/bin/env python3

import datetime


class User:
    def __init__(self, **kwargs):
        """Attributes 'username' and 'password' and 'creationDate' should be given otherwise they are set by default"""

        if 'username' in kwargs: self.username = kwargs['username']
        else: self.username = ''

        if 'password' in kwargs: self.password = kwargs['password']
        else: self.password = ''

        if 'creationDate' in kwargs: self.creation_date = kwargs['creationDate']
        else: self.creation_date = datetime.datetime.now()

    @property
    def username(self): return self._username
    @property
    def password(self): return self._password
    @property
    def creation_date(self): return self._creation_date

    @username.setter
    def username(self, value): self._username = value

    @password.setter
    def password(self, value): self._password = value

    @creation_date.setter
    def creation_date(self, value): self._creation_date = value


def main():
    a = User(username='aimlessly', password='password')
    print(a.username, a.password, a.creation_date)
    datestring = f'{a.creation_date.year} {a.creation_date.month} {a.creation_date.day} {a.creation_date.hour}' \
                 f' {a.creation_date.minute} {a.creation_date.second}'
    print(datestring)
    print(datetime.datetime.strptime(datestring, '%Y %m %d %H %M %S'))


    b = User(username='test')
    print(b.username, b.password)


if __name__ == "__main__": main()