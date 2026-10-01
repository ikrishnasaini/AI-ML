import random
import json
class Bank:
    def __init__(self):
        self.menu()

    def create_acc(self):
        name = input("Enter your Name :-")
        age = int(input("Enter your age :-"))
        pen_no = input("Enter your PEN NO. :-")
        account_no = random.randint(1000000000,10000000000)
        pin_no = input("Create your PIN :-")
        balance = 0
        new_account ={
            'Name':name,
            'Age':age,
            'PEN NO':pen_no,
            'Account No':account_no,
            'PIN NO':pin_no,
            'Balance':balance
        }
        with open("bank_data.json",'r') as file:
            data = json.load(file)
            
        data.append(new_account)

        with open("bank_data.json",'w') as file:
            json.dump(data,file,indent=4)
            
        print(f'''Your Details
        NAME :- {name},
        Age :- {age},
        PEN NO. :- {pen_no},
        Account NO :- {account_no}
        PIN NO :- {pin_no}
        Balance = {balance}''')

    def deposite(self):
        checking = input("Enter your PEN No :-")
        with open('bank_data.json',"r+") as file:
            json.load(file)
            for ele in file:
                if checking ==  file[ele]:
                    deposite_amount = input("Enter Deposite Amount:-")
                    self.balance = self.balance+deposite_amount
                else:
                    print("your PIN is invaild")    


    def menu(self):
        print('''
        Press 1 to Create a Account .
        Press 2 to Deposite.
        Press 3 to withdrawal.
        Press 4 to change your PIN.
        Press 5 to Exit. ''')
        choice  = input("Enter your choice :-")
        if choice == '1':
            self.create_acc()
        elif choice == '2':
            self.deposite()
        elif choice == '3':
            self.withdrawal()
        elif choice == '4':
            self.change_pin()
        elif choice == '5':
            exit()
        else:
            print("Enter a valid key.")