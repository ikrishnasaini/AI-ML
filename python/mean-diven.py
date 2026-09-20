'''Problem 4: Write a menu-driven program 
1. cm to ft 
2. km to miles 
3. USD to INR 
4. exit'''

def cm_to_ft():
    cm = int(input("Enter Centimeter :-"))
    ft = cm/30.48
    print(f"Feet :- {ft}")
def km_to_miles():
    km = int(input("Enter Kilomiters:-"))
    miles = km*0.621371
    print(f"Miles :- {miles}")
def USD_to_INR():
    usd = int(input("Enter USD :-"))
    inr = usd*94.48
    print(f"INR :- {inr}")

print("Pess 1 to calculate cm to ft.")
print("Press 2 to calculate km to miles.")
print("Press 3 to calculate USD to INR.")
print("Press 4 to exit.")
exit = False
while exit == False:
    choice = int(input("Enter your choice:-"))
    if choice == 1:
        cm_to_ft()
    elif choice == 2:
        km_to_miles()
    elif choice == 3:
        USD_to_INR()
    elif choice == 4:
        exit = True
    else:
        print("Press only 1 , 2 , 3 , 4 .")        