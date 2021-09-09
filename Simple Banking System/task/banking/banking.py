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
        self.acc_id = 1

    def create_db(self):
        try:
            conn.execute('CREATE TABLE if not exists card ('
                         'id INTEGER PRIMARY KEY AUTOINCREMENT, '
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
        self.card_number = str(bank_id) + str(account_id) + str(self.checksum_define(str(bank_id) + str(account_id)))
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

    def checksum_define(self, card_num):
        _card_num = [int(x) for x in card_num]
        # Luhn algorithm - 1.step - multiply 2
        digits = list(enumerate(_card_num, start=1))
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
        acc_id = cur.execute(f"SELECT id \
                                    FROM card \
                                    WHERE number = {input_card_number} \
                                    and pin = {input_pin_number}").fetchone()

        if acc_id is not None:
            print('\nYou have successfully logged in!\n')
            self.acc_id = acc_id[0]
            self.account_menu()
        else:
            print('\nWrong card number or PIN!\n')
            self.main_menu()

    def get_balance(self, flag="show"):
        balance = cur.execute(f"SELECT balance \
                                           FROM card \
                                           WHERE id = {self.acc_id}").fetchone()[0]
        if flag == "show":
            print("Balance:", balance)
            self.account_menu()
        else:
            return balance

    def add_income(self):
        income_money = int(input("Enter income:\n"))
        cur.execute(f'UPDATE card SET balance = (SELECT balance '
                    f'FROM card WHERE id = {self.acc_id}) + {income_money} '
                    f'WHERE id = {self.acc_id}')
        conn.commit()
        self.account_menu()

    def transfer(self):
        trans_card = int(input("Transfer\nEnter card number:\n"))
        trans_card_check = cur.execute(f"SELECT id FROM card WHERE number = {trans_card}").fetchone()
        if trans_card % 10 != self.checksum_define(str(trans_card // 10)):
            print("Probably you made a mistake in the card number. Please try again!")
            self.account_menu()
        else:
            if trans_card_check is None:
                print("Such a card does not exist.")
                self.account_menu()
            else:
                if trans_card_check[0] != self.acc_id and not None:
                    trans_money = int(input("Enter how much money you want to transfer:\n"))
                    your_balance = self.get_balance(flag="get")
                    if trans_money <= your_balance:
                        cur.execute(f'UPDATE card SET balance = (SELECT balance '
                                    f'FROM card WHERE id = {self.acc_id}) - {trans_money} '
                                    f'WHERE id = {self.acc_id}')
                        cur.execute(f'UPDATE card SET balance = (SELECT balance '
                                    f'FROM card WHERE number = {trans_card}) + {trans_money} '
                                    f'WHERE number = {trans_card}')
                        conn.commit()
                        print("Success!")
                        self.account_menu()
                    else:
                        print("Not enough money!")
                        self.account_menu()
                elif trans_card_check[0] == self.acc_id:
                    print("You can't transfer money to the same account!")
                    self.account_menu()

    def close_account(self):
        cur.execute(f'DELETE FROM card WHERE id = {self.acc_id}')
        conn.commit()
        print("Your account has been deleted\n")
        self.main_menu()

    def account_menu(self):
        print("\n1. Balance\n"
              "2. Add income\n"
              "3. Do transfer\n"
              "4. Close account\n"
              "5. Log out\n"
              "0. Exit\n")
        menu_code = int(input("Input menu number (1, 2, 3, 4, 5, 0):"))
        if menu_code == 1:
            self.get_balance()
        elif menu_code == 2:
            self.add_income()
        elif menu_code == 3:
            self.transfer()
        elif menu_code == 4:
            self.close_account()
        elif menu_code == 5:
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
