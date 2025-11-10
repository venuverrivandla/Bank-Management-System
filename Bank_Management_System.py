#!/usr/bin/env python3
import os
from decimal import Decimal, InvalidOperation
import random
import string

# ---------- Storage ----------
BASE_DIR = os.path.join(os.path.dirname(__file__), "data", "accounts")
os.makedirs(BASE_DIR, exist_ok=True)

def account_path(acct_no: str) -> str:
    return os.path.join(BASE_DIR, f"{acct_no}.txt")

def parse_kv(lines):
    """Convert key: value lines -> dict"""
    data = {}
    for ln in lines:
        if ": " in ln:
            k, v = ln.strip().split(": ", 1)
            data[k.strip()] = v.strip()
    return data

def serialize_kv(d):
    """Convert dict -> key: value lines (stable order)"""
    order = [
        "account_holder_name",
        "mobile_number",
        "aadhar_number",
        "account_number",
        "current_balance",
        "debit_card_number",  # optional
    ]
    lines = []
    for k in order:
        if k in d:
            lines.append(f"{k}: {d[k]}\n")
    # include any extra keys deterministically
    for k in sorted(set(d.keys()) - set(order)):
        lines.append(f"{k}: {d[k]}\n")
    return lines

def load_account(acct_no):
    p = account_path(acct_no)
    if not os.path.exists(p):
        return None
    with open(p, "r") as f:
        return parse_kv(f.readlines())

def save_account(d):
    p = account_path(d["account_number"])
    with open(p, "w") as f:
        f.writelines(serialize_kv(d))

# ---------- Validation ----------
def valid_name(name: str) -> bool:
    return name.replace(" ", "").isalpha()

def valid_mobile(mob: str) -> bool:
    return mob.isdigit() and len(mob) == 10

def valid_aadhar(a: str) -> bool:
    return a.isdigit() and len(a) == 12

def read_amount(prompt: str) -> Decimal | None:
    raw = input(prompt).strip()
    try:
        amt = Decimal(raw)
        if amt <= 0:
            print("Amount must be > 0")
            return None
        return amt.quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        print("Invalid amount")
        return None

# ---------- Features ----------
def create_account():
    name = input("Enter your full name: ").strip()
    if not valid_name(name):
        print("NameError: Name should contain alphabets only!")
        return

    mobile = input("Enter your 10-digit mobile number: ").strip()
    if not valid_mobile(mobile):
        print("Invalid Mobile number")
        return

    aadhar = input("Enter your 12-digit Aadhar number: ").strip()
    if not valid_aadhar(aadhar):
        print("Invalid Aadhar number")
        return

    print("\nCheck your details")
    print(f"Name: {name.upper()}\nMobile number: {mobile}\nAadhar number: {aadhar}")
    if input("\nAny changes? (y/n): ").strip().lower() == "y":
        return create_account()

    acct_no = "VB" + "".join(random.choices(string.digits, k=8))
    data = {
        "account_holder_name": name.upper(),
        "mobile_number": mobile,
        "aadhar_number": aadhar,
        "account_number": acct_no,
        "current_balance": "0.00",
    }
    save_account(data)
    print("\nYour account has been created successfully")
    print("Your account number:", acct_no)

def geta_debit_card():
    acct_no = input("Enter your account number: ").strip()
    data = load_account(acct_no)
    if not data:
        print("No account with this number.")
        if input('Create an account? (y/n): ').strip().lower() == "y":
            create_account()
        return

    if "debit_card_number" in data:
        print("Sorry! Your account already has a debit card")
        return

    try:
        age = int(input("Enter your age: ").strip())
    except ValueError:
        print("Invalid input")
        return

    if age < 18:
        print("You are not eligible to get a debit card!")
        return

    card_number = "".join(random.choices(string.digits, k=16))
    data["debit_card_number"] = card_number
    save_account(data)
    print(f"Your Debit Card number: {card_number}\nSet a PIN at a nearby ATM.")

def deposit():
    acct_no = input("Enter your account number: ").strip()
    data = load_account(acct_no)
    if not data:
        print("No account with this number.")
        if input('Create an account? (y/n): ').strip().lower() == "y":
            create_account()
        return

    bal = Decimal(data.get("current_balance", "0.00"))
    print(f"Current balance: ₹{bal}")

    amt = read_amount("Enter the amount to deposit: ")
    if amt is None:
        return

    bal = (bal + amt).quantize(Decimal("0.01"))
    data["current_balance"] = f"{bal}"
    save_account(data)
    print("Deposit successful.")
    print(f"Current balance: ₹{bal}")

def check_balance():
    acct_no = input("Enter your account number: ").strip()
    data = load_account(acct_no)
    if not data:
        print("No account with this number.")
        if input('Create an account? (y/n): ').strip().lower() == "y":
            create_account()
        return

    bal = Decimal(data.get("current_balance", "0.00")).quantize(Decimal("0.01"))
    print(f"Your current balance is ₹{bal}")

def withdraw():
    acct_no = input("Enter your account number: ").strip()
    data = load_account(acct_no)
    if not data:
        print("No account with this number.")
        if input('Create an account? (y/n): ').strip().lower() == "y":
            create_account()
        return

    bal = Decimal(data.get("current_balance", "0.00")).quantize(Decimal("0.01"))
    print(f"Current balance: ₹{bal}")

    amt = read_amount("Enter the amount to withdraw: ")
    if amt is None:
        return

    if amt > bal:
        print("Insufficient funds")
        return

    bal = (bal - amt).quantize(Decimal("0.01"))
    data["current_balance"] = f"{bal}"
    save_account(data)
    print("Transaction successful.")
    print(f"Your current balance is ₹{bal}")

# ---------- Main ----------
def main():
    print("\nWelcome to Venu Bank\n")
    print("1 Create account\n2 Get a debit card\n3 Deposit amount\n4 Check balance\n5 Withdraw amount\n0 Exit\n")
    while True:
        try:
            option = int(input("Choose an option: ").strip())
        except ValueError:
            print("Invalid option\n")
            continue

        if option == 1:
            create_account()
        elif option == 2:
            geta_debit_card()
        elif option == 3:
            deposit()
        elif option == 4:
            check_balance()
        elif option == 5:
            withdraw()
        elif option == 0:
            print("Thank you :)")
            break
        else:
            print("Invalid option")
        print()

if __name__ == "__main__":
    main()
