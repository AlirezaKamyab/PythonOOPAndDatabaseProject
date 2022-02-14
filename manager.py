#!/usr/bin/env python3
import employee


class Manager(employee.Employee):
    def __init__(self, **kwargs):
        """
        Constructs Manager
        :param kwargs:
        id: a unique number for each employee
        name: name of the employee
        lastname: lastname of the employee
        username: username credential
        password: pass code credential
        baseIncome: base salary of the employee
        reward: reward for working extra hour
        penalty: penalty for taking hours off
        extraTime: number of hours which the employee worked extra
        offHours: number of hours which employee took hours off
        store: the store which the person or employee is working at
        """
        employee.Employee.__init__(self, **kwargs)

    def hireEmployee(self, emp):
        raise NotImplemented

    def fireEmployee(self, emp):
        raise NotImplemented

    def addBook(self, book):
        raise NotImplemented

    def removeABook(self, bookId):
        raise NotImplemented

    def employeeInformation(self, employeeId):
        raise NotImplemented


def main():
    pass


if __name__ == "__main__": main()