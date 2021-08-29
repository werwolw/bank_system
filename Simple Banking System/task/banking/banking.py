# Write your code here
import string
import sys
import sqlite3
import random

bank_id = 400000
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

class BankSystem:
    def __init__(self):
        self.card_number = 0
        self.card_pin = 0


    def create_db(self):
        try:
            conn.execute('CREATE TABLE if not exists card ('
                                'id INTEGER, '
                                'number TEXT,'
                                'pin TEXT, '
                                'balance INTEGER DEFAULT 0'
                                ');')
            conn.commit()
            # cur.close()
        except sqlite3.OperationalError as OE:
            print(OE)
            cur.close()

    def create_account(self):
        account_id = ''.join(random.sample(string.digits, 9))
        self.card_number = str(bank_id) + str(account_id) + str(self.checksum_define(bank_id, account_id))
        self.card_pin = "".join(random.sample(string.digits, 4))
        cur.execute(f'INSERT INTO card (number, pin) VALUES({self.card_number}, {self.card_pin})')
        conn.commit()
        print("\nYour card has been created\n"
              "Your card number:",
              self.card_number,
              "Your card PIN:",
              self.card_pin, sep='\n')
        # cur.close()
        self.main_menu()

    def checksum_define(self, _bid, acc_id):
        card_num = (str(_bid) + str(acc_id))
        card_num = [int(x) for x in card_num]
        # Luhn algorithm - 1.step - multiply 2
        digits = list(enumerate(card_num, start=1))
        card_digit_multiply = [int(elem) * 2 if index % 2 != 0 else int(elem) for index, elem in digits]
        # 2.step - subtract 9
        card_digit_subtract = [elem - 9 if elem > 9 else elem for elem in card_digit_multiply]
        # 3.step - sum all digit
        sum_all_digits = sum(card_digit_subtract)
        # 4.step - define checksum digit
        if sum_all_digits % 10 == 0:
            return 0
        else:
            return 10 - sum_all_digits % 10

    def login_account(self):
        input_card_number = input("Enter your card number:\n")
        input_pin_number = input("Enter your pin:\n")
        cur.execute(f"SELECT number, pin \
                            FROM card \
                            WHERE number = {input_card_number} and pin = {input_pin_number}")

        if cur.fetchone() is not None:
            print('\nYou have successfully logged in!\n')
            self.account_menu()
        else:
            print('\nWrong card number or PIN!\n')
            self.account_menu()

    def get_balance(self):
        print("Balance:", 0)
        self.account_menu()

    def account_menu(self):
        print("\n1. Balance\n"
              "2. Log out\n"
              "0. Exit\n")
        menu_code = int(input("Input menu number (1, 2, 0):"))
        if menu_code == 1:
            self.get_balance()
        elif menu_code == 2:
            print("You have successfully logged out!")
            self.main_menu()
        elif menu_code == 0:
            print("Bye!")
            conn.close()
            sys.exit()

    def main_menu(self):
        print("\n1. Create an account\n"
              "2. Log into account\n"
              "0. Exit\n")
        menu_code = int(input("Input menu number (1, 2, 0):"))
        if menu_code == 1:
            self.create_account()
        elif menu_code == 2:
            self.login_account()
        elif menu_code == 0:
            print("Bye!")
            conn.close()
            sys.exit()


if __name__ == "__main__":
    my_bank_sys = BankSystem()
    my_bank_sys.create_db()
    my_bank_sys.main_menu()
