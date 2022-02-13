#!/usr/bin/env python3

class BookException(ValueError):
    def __init__(self, msg):
        super().__init__(msg)


class Book:
    def __init__(self, **kwargs):
        """
        Constructs Book
        :param kwargs:
        id: unique value for each book
        title: title of the book
        author: author of the book
        genre: genre of the book
        pages: number of pages
        price: price of the book used to buy from the store
        count: number of the books available at the book store
        """
        if 'id' in kwargs: self.id = kwargs['id']
        else: self.id = 0

        if 'title' in kwargs: self.title = kwargs['title']
        else: self.title = ''

        if 'author' in kwargs: self.author = kwargs['author']
        else: self.author = ''

        if 'genre' in kwargs: self.genre = kwargs['genre']
        else: self.genre = ''

        if 'pages' in kwargs: self.pages = kwargs['pages']
        else: self.pages = 0

        if 'price' in kwargs: self.price = kwargs['price']
        else: self.price = 0

        if 'count' in kwargs: self.count = kwargs['count']
        else: self.count = 0

    @property
    def id(self): return self._id
    @property
    def title(self): return self._title
    @property
    def author(self): return self._author
    @property
    def genre(self): return self._genre
    @property
    def pages(self): return self._pages
    @property
    def price(self): return self._price
    @property
    def count(self): return self._count

    @id.setter
    def id(self, value): self._id = value
    @title.setter
    def title(self, value): self._title = value
    @author.setter
    def author(self, value): self._author = value
    @genre.setter
    def genre(self, value): self._genre = value

    @pages.setter
    def pages(self, value):
        if value < 0: raise BookException("Number of pages cannot be a negative value")
        self._pages = value

    @price.setter
    def price(self, value):
        if value < 0: raise BookException("Price cannot be a negative value")
        self._price = value

    @count.setter
    def count(self, value):
        if value < 0: raise BookException("Number of books cannot be a negative value")
        self._count = value


def main():
    Book()


if __name__ == "__main__": main()