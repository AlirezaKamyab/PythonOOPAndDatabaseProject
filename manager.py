#!/usr/bin/env python3
import employee
from databaseHelper import DatabaseHelper


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
        creationDate: the time when the account is created
        baseIncome: base salary of the employee
        reward: reward for working extra hour
        penalty: penalty for taking hours off
        extraTime: number of hours which the employee worked extra
        offHours: number of hours which employee took hours off
        store: the store which the person or employee is working at
        """
        employee.Employee.__init__(self, **kwargs)

    def hireEmployee(self, emp):
        found = self.store.searchEmployee(emp.id)
        if found is not None:
            raise employee.EmployeeException("Duplicate Employee found at store with the same id")

        if isinstance(found, Manager): raise employee.EmployeeException("A Store cannot have duplicate employees")

        helper = DatabaseHelper(self.store.databasePath, self.store.EMPLOYEES_TABLE)
        helper.insert(id=emp.id, name=emp.name, lastname=emp.lastname, username=emp.username, password=emp.password,
                      creationDate=emp.creation_date, baseIncome=emp.baseIncome, reward=emp.reward, penalty=emp.penalty,
                      extraTime=emp.extraTime, offHours=emp.offHours)
        helper.close()

        self.store.employees.append(emp)

    def fireEmployee(self, empId):
        helper = DatabaseHelper(self.store.databasePath, self.store.EMPLOYEES_TABLE)
        helper.delete(id=empId)
        helper.close()

        for i in range(len(self.store.employees)):
            if self.store.employees[i].id == empId:
                self.store.employees.pop(i)
                break

    def addBook(self, bk):
        self.store.addBook(bk)

    def removeABook(self, bookId):
        helper = DatabaseHelper(self.store.databasePath, self.store.BOOKS_TABLE)
        helper.delete(id=bookId)
        helper.close()

        helper = DatabaseHelper(self.store.databasePath, self.store.BOOK_INVENTORY_TABLE)
        helper.delete(book_id=bookId)
        helper.close()

        for i in self.store.books:
            if self.store.books[i].id == bookId:
                self.store.books.pop(i)
                break

    def employeeInformation(self, employeeId):
        emp = self.store.searchEmployee(employeeId)
        if emp is None: return f'No employee found with id = {employeeId}'

        return f"#{emp.id} {emp.name} {emp.lastname}\n" \
               f"Username: {emp.username} Password: {emp.password}\n" \
               f"Income: {emp.income()} "



def main():
    pass


if __name__ == "__main__": main()