#!/usr/bin/env python3
import bookStore
import manager
import book
import employee
import customer
import os


def main():
    man = bookStore.BookStore.load_manager('database.db')
    if man is None:
        man = manager.Manager(id=1, name="Alireza", lastname='Kamyab', username='aimlessly', password=123456789,
                              baseIncome=10000000)
    store = bookStore.BookStore(manager=man)

    while True:
        os.system('cls')
        print("        Main Menu")
        print("---------------------------")
        print("1- Log as Employee")
        print("2- Log as Customer")
        print("3- Registration")
        print("0- Quit")
        inp = input(">> ")

        if inp == '1':
            os.system('cls')
            username = input('Username >> ')
            password = input('Password >> ')
            emp = store.logAsEmployee(username, password)
            if emp is None:
                print("Invalid credentials!")
                os.system('pause')
            else: employee_menu(emp, store)
        elif inp == '2':
            os.system('cls')
            username = input("Username >> ")
            password = input ("Password >> ")
            cus = store.logAsCustomer(username, password)

            if cus is None:
                print("Invalid credentials!")
                os.system('pause')
            else: customer_menu(cus, store)
        elif inp == '3':
            registration_form(store)
        elif inp == '0':
            break
        else:
            print("Invalid Input")
            os.system("pause")


def registration_form(store):
    os.system('cls')
    try:
        id_number = int(input("ID >> "))
        name = input("Name >> ")
        lastname = input("Lastname >> ")
        username = input("Username >> ")
        password = input("Password >> ")
        credit = int(input("Credit >> "))

        cus = customer.Customer(id=id_number, name=name, lastname=lastname, username=username, password=password,
                                credit=credit)
        store.registerACustomer(cus)
        print("Registration was Successful")
    except Exception as ex:
        print(ex)

    os.system('pause')


def customer_menu(cus, store):
    while True:
        cus.store = store
        os.system('cls')
        print(f"{cus.username} ({cus.name} {cus.lastname}) (Credit: {cus.credit})")
        print(f"_________________________")
        print("1- My books")
        print("2- Mark as completed")
        print("3- Increase credit")
        print("4- Buy a Book")
        print("0- Logout")
        inp = input(">> ")

        if inp == '1':
            os.system('cls')
            print("      My Books")
            print("-----------------------")
            for bk in cus.books:
                print(bk)
            print()
            os.system('pause')
        elif inp == '2':
            os.system('cls')
            try:
                print("      Completed Books")
                print("---------------------------")
                for bk in cus.completed:
                    print(bk)
                print()

                id_number = int(input("BOOK ID >> "))
                bk = store.searchBook(id_number)
                if bk is not None:
                    cus.setABookAsCompleted(bk)
                print()
            except Exception as ex:
                print(ex)
            os.system('pause')
        elif inp == '3':
            os.system('cls')
            try:
                amount = int(input("Amount >> "))
                cus.increaseCredit(amount)
                print(f"Your credit is now {cus.credit}")
            except Exception as ex:
                print(ex)
            print()
            os.system('pause')
        elif inp == '4':
            os.system('cls')
            try:
                print("     Available Books")
                print("----------------------------")
                for bk in store:
                    print(bk)
                print()
                id_number = int(input("BOOK ID >> "))
                found = store.searchBook(id_number)
                if found is None:
                    print("Book not found!")
                else: cus.buyABook(found)
            except Exception as ex:
                print(ex)
            print()
            os.system('pause')
        elif inp == '5':
            os.system('cls')
            try:
                print("          Books")
                print("----------------------------")
                for bk in store:
                    print(bk)
            except Exception as ex:
                print(ex)
            os.system('pause')
        elif inp == '0':
            break
        else:
            print("Invalid Input!")
            os.system("pause")


def create_employee():
    os.system('cls')
    try:
        id_number = int(input("ID >> "))
        name = input("Name >> ")
        lastname = input("Lastname >> ")
        username = input("Username >> ")
        password = input("Password >> ")
        baseIncome = int(input("Base Income >> "))

        emp = employee.Employee(id=id_number, name=name, lastname=lastname, username=username, password=password,
                                baseIncome=baseIncome)
        return emp
    except Exception as ex:
        print(ex)

    os.system('pause')


def create_book():
    os.system('cls')
    try:
        title = input("Title >> ")
        author = input("Author >> ")
        genre = input("Genre >> ")
        pages = int(input("Pages >> "))
        price = int(input("Price >> "))
        count = int(input("Count >> "))

        bk = book.Book(title=title, author=author, genre=genre, pages=pages, price=price, count=count)
        return bk
    except Exception as ex:
        print(ex)


def employee_menu(emp, store):
    emp.store = store
    isManager = isinstance(emp, manager.Manager)

    while True:
        os.system('cls')
        print(f"{emp.username}")
        print("------------------------")
        print("1- Leave")
        print("2- Extra Work")
        print("3- Customer Info")
        print("4- Personal Info")
        print("5- Print Books")

        if isManager:
            print("6- Hire Employee")
            print("7- Fire Employee")
            print("8- Add Book")
            print("9- Remove Book")
            print("10- Employee Info")
        print("0- Logout")
        inp = input(">> ")

        if inp == '1':
            os.system('cls')
            try:
                hours = int(input("Hours >> "))
                emp.leave(hours)
                print(f"Hours took off {emp.offHours} and penalty is {emp.penalty}")
            except Exception as ex:
                print(ex)
            os.system('pause')
        elif inp == '2':
            os.system('cls')
            try:
                hours = int(input("Hours >> "))
                emp.extraWork(hours)
                print(f"Hours worked extra {emp.extraTime} and reward is {emp.reward}")
            except Exception as ex:
                print(ex)
            os.system('pause')
        elif inp == '3':
            os.system('cls')
            try:
                cus_id = int(input("Customer ID >> "))
                print(emp.customerInfo(cus_id))
            except Exception as ex:
                print(ex)
            os.system('pause')
        elif inp == '4':
            os.system('cls')
            print("     Personal Info")
            print("--------------------------")
            print(emp)
            os.system('pause')
        elif inp == '5':
            os.system('cls')
            try:
                print("          Books")
                print("----------------------------")
                for bk in store:
                    print(bk)
            except Exception as ex:
                print(ex)
            os.system('pause')
        elif inp == '6' and isManager:
            os.system('cls')
            try:
                cm = create_employee()
                emp.hireEmployee(cm)
                print("Operation was Successful")
            except Exception as ex:
                print(ex)
            os.system('pause')
        elif inp == '7' and isManager:
            os.system('cls')
            try:
                id_number = int(input("Employee ID >> "))
                emp.fireEmployee(id_number)
            except Exception as ex:
                print(ex)
            os.system('pause')
        elif inp == '8' and isManager:
            os.system('cls')
            try:
                bk = create_book()
                emp.addBook(bk)
                print("Operation was Successful")
            except Exception as ex:
                print(ex)
            os.system('pause')
        elif inp == '9' and isManager:
            os.system('cls')
            try:
                id_number = int(input("Book ID >> "))
                emp.removeABook(id_number)
                print("Operation was Successful")
            except Exception as ex:
                print(ex)
            os.system('pause')
        elif inp == '10' and isManager:
            os.system('cls')
            try:
                id_number = int(input("Employee ID >> "))
                print(emp.employeeInformation(id_number))
            except Exception as ex:
                print(ex)
            os.system('pause')
        elif inp == '0':
            break
        else:
            print("Invalid Input!")
            os.system('pause')


if __name__ == "__main__": main()