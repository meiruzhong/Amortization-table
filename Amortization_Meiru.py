# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 21:35:18 2022

@author: Meiru
"""
#load the needed packages
import numpy as np
import pandas as pd
import sys
#define a is_valid functino to check if values are valid
def is_valid(text):
    numbers = '0123456789.'
    for value in text:
        if numbers.find(value) == -1:
            return False
    return True

#input principal and check if it's valid
print('Please enter the following items: ')
principal = input('The amount of the principal: ')
while is_valid(principal) != True:
    print('please enter a valid principal with numbers only!')
    principal = input('The amount of the principal: ')

#input expected payment and check if it's valid
expected_payment = input('The amount of the minimum expected payment: ')
while is_valid(expected_payment) != True:
    print('please enter a valid expected payment with numbers only!')
    expected_payment= input('The amount of the expected payment: ')
    
#input interest rate and check if it's valid
interest_rate = input('The interest rate (ex:0.08 should be entered as 8): ')
while is_valid(interest_rate) != True:
    print('please enter a valid interest with numbers only!')
    interest_rate = input('The interest rate: ')

#input extra payment and check if it's valid
extra_payment = input('The amount of the extra payment: ')
while is_valid(extra_payment) != True:
    print('please enter a valid extra_payment with numbers only!')
    extra_payment = input('The amount of the extra_payment: ')

nmc= 2400
#create the blank lists for all the elements
month = np.zeros(nmc)
beginp = np.zeros(nmc)
payment = np.zeros(nmc)
interest = np.zeros(nmc)
extra_p = np.zeros(nmc)
p_applied = np.zeros(nmc)
end_p = np.zeros(nmc)

#define the first row
month[0] = 1
beginp[0] = float(principal)
payment[0] = float(expected_payment)
interest[0] = float((float(beginp[0]) * float(interest_rate)*0.01 /12))
extra_p[0] = float(extra_payment)
p_applied[0] = float(payment[0]) - float(interest[0]) + float(extra_payment[0])
end_p[0] = float(beginp[0]) - float(p_applied[0])

#use a for loop to create the following figures based on their previous data
#the last row's payment might be different, which depends on the situation
for i in range(1,nmc):
    month[i] = i +1
    beginp[i] = float(end_p[i-1])
    payment[i] = float(expected_payment)
    interest[i] = float(beginp[i]) * float(interest_rate)*0.01 /12
    extra_p[i] = float(extra_payment)
    p_applied[i] = float(payment[i]) - float(interest[i]) + float(extra_p[i])
    end_p[i] = float(beginp[i]) - float(p_applied[i])
    if end_p[i] < p_applied[i]:
        month[i+1] = i +2
        beginp[i+1] = float(end_p[i])
        interest[i+1] = float(beginp[i+1]) * float(interest_rate)*0.01 /12
        payment[i+1] = beginp[i+1] + interest[i+1] - extra_p[i+1]
        extra_p[i+1] = float(extra_payment)
        p_applied[i+1] = float(payment[i+1]) - float(interest[i+1]) + float(extra_p[i+1])
        end_p[i+1] = float(beginp[i+1]) - float(p_applied[i+1])
        break

def is_valid_case(text):
    if end_p[i] > p_applied[i]:
        print('Your input data is out of the range and the maximum repayment period is 200 years.')
        print('Please restart the program and try again!')
        return False

while is_valid_case(end_p) == False:
    sys.exit()
    
#delete useless rows and make dataframe clearer
indexes = np.arange(i+2,nmc)
month = np.delete(month, indexes, axis=0)
beginp = np.delete(beginp, indexes, axis=0)
payment = np.delete(payment, indexes, axis=0)
interest = np.delete(interest, indexes, axis=0)
extra_p = np.delete(extra_p, indexes, axis=0)
p_applied = np.delete(p_applied, indexes, axis=0)
end_p = np.delete(end_p, indexes, axis=0)

#calculate the amounts of total
sum_payemnt = round(payment.sum(),2)
sum_interest = round(interest.sum(),2)
sum_extrap = round(extra_p.sum(),2)
sum_papplied = round(p_applied.sum(),2)


#build a dictionary to concatenate all the elements
schedule = {'Month':month,'Begin P':beginp,'Payment':payment,'Interest':interest,
            'Extra Payment':extra_p,'P Applied':p_applied,'End P':end_p}
#build a total list
total_list = {'Month':'Total','Begin P':'.','Payment':sum_payemnt,'Interest':sum_interest,
            'Extra Payment':sum_extrap,'P Applied':sum_papplied,'End P':'.'}

#convert its type to dataframe
schedule = pd.DataFrame(schedule)
#control the decimals to 2
schedule = schedule.round(decimals=2)
#control the decimals for month lists to 0
schedule['Month'] = schedule['Month'].astype(int)

#convert its type to dataframe
total_list = pd.DataFrame(total_list,index=[0])

#combine the two dataframes 
frame = [schedule,total_list]
fulltable = pd.concat(frame, axis=0, join='outer', sort=False)

# hide the index column and show clear results
print(fulltable.to_string(index=False))
print('You need to pay off the loan in '+ str(round(month[i+1]/12,2))+' years.')






