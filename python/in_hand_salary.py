'''Problem 1: 
Write a program that will give you in hand monthly salary after deduction on 
CTC - HRA(10%), DA(5%), PF(3%) and taxes deduction as below: 
> Salary(Lakhs) : Tax(%)
 * Below 5 : 0% 
 * 5-10 : 10% 
 * 10-20 : 20% 
 * aboove 20 : 30%  '''

total_salary = int(input("Enter your total salary :-"))
monthly_salary = 0
HRA = total_salary * 10 / 100
DA = total_salary * 5 /100
PF = total_salary * 3 / 100
CTC = HRA + DA + PF
total_salary = total_salary - CTC

if total_salary < 500000:
    monthly_salary = total_salary / 12
    print(f"you monthly salary {monthly_salary}")
elif total_salary >= 500000 and total_salary < 1000000:
    Tax = total_salary * 10 /100
    total_salary-=Tax
    monthly_salary = total_salary/12
    print(f"you monthly salary {monthly_salary}")
elif total_salary >= 1000000 and total_salary < 2000000 :
    Tax = total_salary * 20 / 100
    total_salary-=Tax
    monthly_salary = total_salary/12
    print(f"you monthly salary {monthly_salary}")
else:
    Tax = total_salary *30 /100
    total_salary-=Tax
    monthly_salary = total_salary/12
    print(f"you monthly salary {monthly_salary}")
    
