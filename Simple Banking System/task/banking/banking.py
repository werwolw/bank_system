# Write your code here
import sys
import random


class BankSystem:
    def __init__(self):
        self.card_number = 0
        self.card_pin = 0
        self.acc_data = {}

    def create_account(self):
        bank_id = 400000
        account_id = random.randint(100000000, 999999999)
        self.card_number = str(bank_id) + str(account_id) + str(self.checksum_define(bank_id, account_id))
        self.card_pin = str(random.randint(0000, 9999)).zfill(4)
        self.acc_data = {self.card_number: {"pin": self.card_pin, "balance": 0}}
        print("\nYour card has been created"
              "Your card number:",
              self.card_number,
              "Your card PIN:",
              self.card_pin, sep='\n')
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
        checksum = 10 - sum_all_digits % 10
        return checksum

    def login_account(self):
        input_card_number = input("Enter your card number:\n")
        input_pin_number = input("Enter your pin:\n")
        # login_data = {input_card_number: {"pin": input_pin_number}}
        if (input_card_number == self.card_number) and (input_pin_number == self.acc_data[self.card_number]["pin"]):
            print("You have successfully logged in!")
            self.account_menu()
        else:
            print("Wrong card number or PIN!")
            self.main_menu()

    def get_balance(self):
        print("Balance:", self.acc_data[self.card_number]["balance"])
        self.account_menu()

    def account_menu(self):
        print("\n1. Balance\n"
              "2. Log out\n"
              "0. Exit\n")
        menu_code = int(input("Input menu number (0, 1, 2):"))
        if menu_code == 1:
            self.get_balance()
        elif menu_code == 2:
            print("You have successfully logged out!")
            self.main_menu()
        elif menu_code == 0:
            print("Bye!")
            sys.exit()

    def main_menu(self):
        print("\n1. Create an account\n"
              "2. Log into account\n"
              "0. Exit\n")
        menu_code = int(input("Input menu number (0, 1, 2):"))
        if menu_code == 1:
            self.create_account()
        elif menu_code == 2:
            self.login_account()
        elif menu_code == 0:
            print("Bye!")
            sys.exit()


if __name__ == "__main__":
    my_bank_sys = BankSystem()
    my_bank_sys.main_menu()

