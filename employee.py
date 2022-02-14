#!/usr/bin/env python3
import person
import user
from databaseHelper import DatabaseHelper


class EmployeeException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class Employee(person.Person, user.User):
    PENALTY = 100000
    REWARD = 200000
    MAX_OFF_HOURS = 15
    MAX_EXTRA_HOURS = 15

    def __init__(self, **kwargs):
        """
        Constructs Employee
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

        if 'baseIncome' in kwargs: self.baseIncome = kwargs['baseIncome']
        else: self.baseIncome = 0

        if 'reward' in kwargs: self.reward = kwargs['reward']
        else: self.reward = 0

        if 'penalty' in kwargs: self.penalty = kwargs['penalty']
        else: self.penalty = 0

        if 'extraTime' in kwargs: self.extraTime = kwargs['extraTime']
        else: self.extraTime = 0

        if 'offHours' in kwargs: self.offHours = kwargs['offHours']
        else: self.offHours = 0

        if 'store' in kwargs: self.store = kwargs['store']
        else: self.store = None

        person.Person.__init__(self, **kwargs)
        user.User.__init__(self, **kwargs)

    @property
    def baseIncome(self): return self._baseIncome
    @property
    def reward(self): return self._reward
    @property
    def penalty(self): return self._penalty
    @property
    def extraTime(self): return self._extraTime
    @property
    def offHours(self): return self._offHours
    @property
    def store(self): return self._store

    @baseIncome.setter
    def baseIncome(self, value):
        if value < 0: raise EmployeeException("Base Income cannot be a negative number")
        self._baseIncome = value

    @reward.setter
    def reward(self, value):
        if value < 0: raise EmployeeException("Reward cannot be a negative number")
        self._reward = value

    @penalty.setter
    def penalty(self, value):
        if value < 0: raise EmployeeException("Penalty cannot be a negative number")
        self._penalty = value

    @extraTime.setter
    def extraTime(self, value):
        if value < 0: raise EmployeeException("Extra time cannot be a negative number")
        self._extraTime = value

    @offHours.setter
    def offHours(self, value):
        if value < 0: raise EmployeeException("Off hours cannot be a negative number")
        self._offHours = value

    @store.setter
    def store(self, value): self._store = value

    def leave(self, hours):
        if (hours + self.offHours) * self.PENALTY > self.income():
            raise EmployeeException("Cannot take hours off anymore")

        self.offHours += hours
        if self.offHours >= self.MAX_OFF_HOURS:
            self.penalty = (self.offHours - self.MAX_OFF_HOURS) * self.PENALTY

        self.update_employee_from_database()

    def extraWork(self, hours):
        if self.extraTime + hours > self.MAX_EXTRA_HOURS: raise EmployeeException("Working extra time's limit exceed")

        self.extraTime += hours
        self.reward = self.extraTime * self.REWARD

        self.update_employee_from_database()

    def income(self):
        return self.baseIncome + self.reward - self.penalty

    def customerInfo(self, customerId):
        """
        Searches through Store to find the Customer with specified ID
        :param customerId: Customer with customerId will be searched
        :return: If found, return a string with customer info otherwise "Customer with id {customerId} not found"
        """
        cus = self.store.searchCustomer(customerId)
        if cus is None: return f'Customer with id {customerId} not found'

        return f'#{cus.id} {cus.name} {cus.lastname}\nUsername: {cus.username} Password: {cus.password}\n' \
               f'Credit: {cus.credit}'

    def __str__(self):
        return f"#{self.id} {self.name} {self.lastname}\nUsername: {self.username} Password: {self.password}\n" \
               f"Income {self.income()}"

    def update_employee_from_database(self):
        helper = DatabaseHelper(self.store.databasePath, self.store.EMPLOYEES_TABLE)
        helper.update(id=self.id, name=self.name, lastname=self.lastname, username=self.username,
                      password=self.password, extraTime=self.extraTime, offHours=self.offHours, reward=self.reward,
                      penalty=self.penalty, baseIncome=self.baseIncome)
        helper.close()


def main():
    pass


if __name__ == "__main__": main()