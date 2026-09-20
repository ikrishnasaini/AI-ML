'''Problem 3: Write a program that will take user input of cost price and selling price and determines whether its a loss or a profit.'''
cost_price = int(input("Enter Cost price :-"))
sell_price = int(input("Enter sell price :-"))

price = sell_price - cost_price

if price > 0:
    print("It is a profit.")
elif price == 0:
    print("NO Profit No Loss")
else:
    print("It is a Loss")