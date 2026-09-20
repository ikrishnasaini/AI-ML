'''Problem 2: Write a program that take a user input of three angles and will find out whether it can form a triangle or not.'''
print("Enter three triangle value")
a = int(input("Enter first value :- "))
b = int(input("Enter second value :- "))
c = int(input("Enter third value :- "))

triangle = a+b+c

if triangle == 180:
    print("It is a triangle.")
else:
    print("It is not a triangle.")