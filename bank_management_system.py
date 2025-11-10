#to create an account
import os  # (moved up so we can use it for paths)

# --- GitHub-friendly storage (NO logic change) ---
BASE_DIR = os.path.join(os.path.dirname(__file__), "data", "accounts")
os.makedirs(BASE_DIR, exist_ok=True)

def get_account_path(account_number: str) -> str:
    return os.path.join(BASE_DIR, f"{account_number}.txt")
# -------------------------------------------------

def create_account():
    #obtaining account holder name
    name = input('Enter your full name: ').upper()
    
    #checking whether it contains any other chars or not
    namefalse = False
    for i in name:
        if i.isdigit():
            namefalse = True
            break
    
    if namefalse:
        print('NameError: Name should contain alphabets only!')
    else:
        #obtaining mobile number 
        mobile_number = input('Enter your 10-digit mobile number: ')
        
        #checking whether it is valid or not
        if not(mobile_number.isdigit()):
            print('MobileNoError: Mobile number should contain numbers only!')
        elif len(mobile_number)!=10: 
            print('Invalid Mobile number')
        else:
            
            #obtaining aadhar number
            aadhar_number = input('Enter your 12-digit aadhar number: ')
            
            #checking whether it is valid or not
            if not(aadhar_number.isdigit()):
                print('AadharNoError: Aadhar number should contain numbers only!')
            elif len(aadhar_number)!=12:
                print('Invalid Aadhar number')
            
            else:
                #displaying the details
                print('\nCheck your details')
                print('Name:',name.upper(),'\nMobile number:',mobile_number,'\nAadhar number:',aadhar_number)
                
                #asking to do any changes
                correction = input('\nAny changes? (y/n): ')
                if correction == 'y':
                    change = create_account()
                elif correction == 'n':
                    print('Your account has been created succesfully')
                    
                    #generating account number, card number and pin number
                    import random
                    import string
                    account_number = 'VB' + ''.join(random.choices(string.digits, k=8))
                    
                    #balance will be zero untill first deposit
                    balance = '0.00'
                    
                    #displaying account number, card number and pin number
                    print('\nYour account number:',account_number)
                    
                    #adding all the deatils to a list
                    info = [f'account_holder_name: {name}\n',f'mobile_number: {mobile_number}\n',f'aadhar_number: {aadhar_number}\n',f'account_number: {account_number}\n',f'current_balance: {balance}\n']
                                        
                    #creating a textfile with generated account number
                    with open(get_account_path(account_number),'w') as account_file:
                                            
                        #entering the list which contains all the details into the textfile
                        account_file.writelines(info)
            
                else:
                    print('Invalid input')

#to get a debit card
def geta_debit_card():
    #obtaining account number from user
    account_number = input('Enter your account number: ')
    
    #creating file path (portable)
    file_path = get_account_path(account_number)
    
    #checking whether the account exist or not
    if os.path.exists(file_path):
        
        #reading the specified account file
        with open(file_path,'r') as account_file:
            file_info = account_file.readlines()
            
            #checking whether the account has any debit card previously
            CardFound = False
            for line in file_info:
                if 'debit_card_number' in line.strip():
                    CardFound = True
                    break
            if CardFound:
                print('Sorry! Your account already has a debit card')
            else:
                try:
                    #obtaining user's age
                    age = int(input('Enter your age: '))
                    if age>=18:
                        print('You are eligible to get a debit card!')
                
                        #generating cardnumber 
                        import random
                        import string
                        card_number = ''.join(random.choices(string.digits,k=16))

                        #displaying cardnumber and pin
                        print(f'Your Debit Card number: {card_number}\nYou can set a PIN at nearby ATM')
                
                        #adding debit card details to the account file
                        card_info = f'debit_card_number: {card_number}\n'
                
                        with open(file_path,'a') as account_file:
                            account_file.writelines(card_info)
                    else:
                        print('You are not eligible to get a debit card!')
                except ValueError:
                    print('Invalid input')
        
    else:
        print('There is no acconut with this number\nMake sure that you entered a correct account number')
        option = input('Do you want to create an account? (y/n): ')
        if option=='y':
            create_account()
        elif option == 'n':
            print('Thank you :)')
        else:
            print('Invalid Input')
        
#to deposit amount
def deposit():
    #obtaining the account number
    account_number = input('Enter your account number: ')

    #creating file path (portable)
    file_path = get_account_path(account_number)

    #checking whether the account exist or not
    if os.path.exists(file_path):
        with open(file_path,'r') as account_file:
            file_info = account_file.readlines()
            balance = file_info[4][17: ].strip()
            print(f'Currently your account balance is {balance} Rs')
            deposit = float(input('Enter the amount to deposit in your account: '))
            if deposit>0:
                updated_balance = float(balance)+deposit
                print('Your amount has been sucessfully deposited to your account')
                print('Current balance:',updated_balance)
                                
                #updating the balance
                file_info[4]=f'current_balance: {updated_balance}\n'
                with open(file_path,'w') as account_file:
                    account_file.writelines(file_info)
            else:
                print('Error')
                                
    else:
        print('There is no account with this number\nMake sure that you entered a correct account number')
        option = input('Do you want to create an account? (y/n): ')
        if option=='y':
            create_account()
        elif option == 'n':
            print('Thank you :)')
        else:
            print('Invalid Input')
        
#to check balance
def check_balance():
    #obtaining account number
    account_number = input('Enter your account number: ')

    #creating file path (portable)
    file_path = get_account_path(account_number)

    #checking whether the account exists or not
    if os.path.exists(file_path):
        with open(file_path,'r') as account_file:
            file_info = account_file.readlines()
            balance = file_info[4][17: ].strip()
            print(f'Your current balance is {balance} Rs')
                    
    else:
        print('There is no account with this number\nMake sure that you entered a correct account number')
        option = input('Do you want to create an account? (y/n): ')
        if option=='y':
            create_account()
        elif option == 'n':
            print('Thank you :)')
        else:
            print('Invalid Input')

#to withdraw amount       
def withdraw():
    #obtaining account number
    account_number = input('Enter your account number: ')

    #creating file path (portable)
    file_path = get_account_path(account_number)

    #checking whether the account exist or not
    if os.path.exists(file_path):
        try:
            with open(file_path,'r') as account_file:
                file_info = account_file.readlines()
                
                balance = file_info[4][17: ].strip()
        
                #obtaining withdraw amount
                amount = float(input('Enter the amount to withdraw: '))
                if amount<=float(balance):
                    updated_balance = float(balance)-amount
                        
                    file_info[4]=f'current_balance: {updated_balance}\n'
                        
                    with open(file_path,'w') as account_file:
                        account_file.writelines(file_info)
                        
                        print('Transaction Successful')
                        print('Your current balance is',file_info[4][17: ].strip(),'Rs')
                else:
                    print('Insuffucient funds')
                       
        except ValueError:
            print('Invalid Input')
    else:
        print('There is no account with this number\nMake sure that you entered a correct account number')
        option = input('Do you want to create an account? (y/n): ')
        if option=='y':
            create_account()
        elif option == 'n':
            print('Thank you :)')
        else:
            print('Invalid Input')

#Main program
print('\nWelcome to Venu bank\n')
print('1 To create account\n2 To get a debit card\n3 To deposit amount\n4 To check balance\n5 To withdraw amount\n0 To exit\n')
while True:
    option = int(input('Choose an option: '))
    if option==1:
        call = create_account()
        print('\n')
    elif option==2:
        call = geta_debit_card()
        print('\n')
    elif option==3:
        call = deposit()
        print('\n')
    elif option==4:
        call = check_balance()
        print('\n')
    elif option==5:
        call = withdraw()
        print('\n')
    elif option==0:
        print('Thank you :)')
        break
    else:
        print('Invalid option')
        print('\n')
