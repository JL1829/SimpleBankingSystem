import random
from .luhnAlgo import Luhn
import sqlite3


class BankAccount:
    """
    DocString
    """

    def __init__(self,
                 cardNumber=None,
                 pin=None,
                 balance=0):
        self.ID = None
        self.cardNumber = cardNumber
        self.pin = pin
        self.balance = balance

    def createAccount(self):
        IIN = str(400000)
        self.ID = str(random.randint(000000000, 999999999))
        AccountNumber = IIN + "0" * (9 - len(self.ID)) + self.ID

        self.cardNumber = Luhn().create(accountNumber=AccountNumber)
        tempPIN = str(random.randint(0000, 9999))
        self.pin = "0" * (4 - len(tempPIN)) + tempPIN
        return self.ID, self.cardNumber, self.pin

    def __repr__(self):
        return f"Bank Account ID: {self.ID}\n" \
               f"Bank Account number: {self.cardNumber}\n" \
               f"Pin Number: {self.pin}\n" \
               f"Balance: {self.balance}"


class Menu:
    """
    Show the main menu of the Banking System
    """

    def __init__(self):
        self._choice = '0'

    def __repr__(self):
        return f"Current choice: {self._choice}"

    def __eq__(self, other):
        return True if self._choice == other else False

    @staticmethod
    def _show_main_menu():
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')

    @staticmethod
    def _show_account_menu():
        print("1. Balance")
        print('2. Add income')
        print('3. Do transfer')
        print('4. Close account')
        print('5. Log out')
        print('0. Exit')

    def show_and_get_choice(self):
        if self._choice.startswith('2'):
            self._show_account_menu()
            self._choice = f'{self._choice[0]}.{input()}'
        else:
            self._show_main_menu()
            self._choice = input()

    def back_to_main(self):
        self._choice = '0'


class Database:
    """
    SQLite Database Operation object

    --------
    Method:

    * add(self, account): add new account to database
    * get(self, cardNumber): get the account details from database by it's cardNumber
    * close(self, number): DELETE the cardNumber record in database
    * updateBalance(self, number, balance): UPDATE the account balance in database
    """

    def __init__(self):
        self.conn = sqlite3.connect('card.s3db')
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS card
                (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)
            """)
        except sqlite3.OperationalError:
            pass

    def add(self, account):
        self.cursor.execute(
            f"INSERT INTO card VALUES ({account.ID}, {account.cardNumber}, \
            {account.pin}, {account.balance})")
        self.conn.commit()

    def get(self, cardNumber):
        acc = self.cursor.execute(
            f"SELECT * FROM card WHERE number={cardNumber}").fetchone()
        if acc:
            account = BankAccount()
            account.ID, account.cardNumber, account.pin, account.balance = acc
            return account
        return None

    def close(self, number):
        self.cursor.execute(f"DELETE FROM card WHERE number = {number}")
        self.conn.commit()

    def updateBalance(self, number, balance):
        self.cursor.execute(
            f"UPDATE card SET balance = {balance} WHERE number = {number}")
        self.conn.commit()


class BankingSystem:
    """
    Simple Banking System
    """

    def __init__(self):
        self.menu = Menu()
        self.db = Database()
        self.current_account = None

    def createAccount(self):
        account = BankAccount()
        account.createAccount()
        self.db.add(account=account)
        print('\nYour card has been created')
        print('Your card number:')
        print(f'{account.cardNumber}')
        print('Your card PIN:')
        print(f'{account.pin}\n')

    def login(self):
        print("\nEnter your card number:")
        number = input()
        print('Enter your PIN:')
        pin = input()
        account = self.db.get(cardNumber=number)
        if account:
            if account.pin == pin:
                print('\nYou have successfully logged in!\n')
                self.current_account = account
                return
        print('\nWrong card number or PIN!\n')
        self.menu.back_to_main()

    def showBalance(self):
        print(f"\nBalance: {self.current_account.balance}\n")

    def addIncome(self):
        print('\nEnter income:')
        income = int(input())
        self.current_account.balance += income
        self.db.updateBalance(
            number=self.current_account.cardNumber,
            balance=self.current_account.balance)
        print('Income was added!\n')

    def transfer(self):
        print('\nTransfer\nEnter card number:')
        number = input()
        if Luhn().validate(number):
            account = self.db.get(cardNumber=number)
            if account:
                print("Enter how much money you want to transfer:")
                transfer = int(input())
                if self.current_account.balance >= transfer:
                    self.db.updateBalance(
                        number=number, balance=account.balance + transfer)
                    print(
                        f'>>> num: {self.current_account.cardNumber} bal: {self.current_account.balance}')
                    self.current_account.balance -= transfer
                    self.db.updateBalance(
                        self.current_account.cardNumber,
                        self.current_account.balance)
                    print(
                        f'>>> num: {self.current_account.cardNumber} bal: {self.current_account.balance}')
                    print('Success!\n')
                else:
                    print('Not enough money!\n')
            else:
                print('Such a card does not exist.\n')
        else:
            print('Probably you made mistake in the card number. Please try again!\n')

    def closeAccount(self):
        self.db.close(self.current_account.cardNumber)
        print('\nThe account has been closed!\n')

    def logOut(self):
        print('\nYou have successfully logged out!\n')
        self.menu.back_to_main()

    def main(self):
        while True:
            self.menu.show_and_get_choice()
            if self.menu == '1':
                self.createAccount()
            elif self.menu == '2':
                self.login()
            elif self.menu == '2.1':
                self.showBalance()
            elif self.menu == '2.2':
                self.addIncome()
            elif self.menu == '2.3':
                self.transfer()
            elif self.menu == '2.4':
                self.closeAccount()
            elif self.menu == '2.5':
                self.logOut()
            else:
                print('\nBye!')
                break
