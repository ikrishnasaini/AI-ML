'''Problem 7 - Reverse a given integer number.'''
# num = int(input("Enter you number :-"))
# rev = str(num)
# rev = rev[-1::-1]
# print(rev)

num = int(input("Enter Number :-"))
rev = 0
while num > 0:
    d = num % 10
    rev = rev * 10 + d 
    num = num // 10
print(rev)