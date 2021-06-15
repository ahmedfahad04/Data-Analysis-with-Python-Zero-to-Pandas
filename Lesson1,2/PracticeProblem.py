from urllib.request import urlretrieve as urr 
import os
import pprint as p
import math

# os.makedirs('data2')

url1 = 'https://gist.githubusercontent.com/aakashns/257f6e6c8719c17d0e498ea287d1a386/raw/7def9ef4234ddf0bc82f855ad67dac8b971852ef/loans1.txt'
url2 = 'https://gist.githubusercontent.com/aakashns/257f6e6c8719c17d0e498ea287d1a386/raw/7def9ef4234ddf0bc82f855ad67dac8b971852ef/loans2.txt'
url3 = 'https://gist.githubusercontent.com/aakashns/257f6e6c8719c17d0e498ea287d1a386/raw/7def9ef4234ddf0bc82f855ad67dac8b971852ef/loans3.txt'

# download those files
urr(url1, './data2/loan1.txt')
urr(url2, './data2/loan2.txt')
urr(url3, './data2/loan3.txt')

def loan_emi(amount, duration, rate, down_payment=0):
    """Calculates the equal montly installment (EMI) for a loan.
    
    Arguments:
        amount - Total amount to be spent (loan + down payment)
        duration - Duration of the loan (in months)
        rate - Rate of interest (monthly)
        down_payment (optional) - Optional intial payment (deducted from amount)
    """
    loan_amount = amount - down_payment
    try:
        emi = loan_amount * rate * ((1+rate)**duration) / (((1+rate)**duration)-1)
    except ZeroDivisionError:
        emi = loan_amount / duration
    emi = math.ceil(emi)
    
    return emi

def compute_emis(data):
    emis = []
    for i in range(len(data['amount'])):
        val = (loan_emi(data['amount'][i], data['duration'][i], data['rate'][i]/12, data['down_payment'][i]))
        emis.append(val)

    data['emis'] = emis

def parse_headers(header_line):
    return header_line.strip().split(",")

def parse_data(value):
    line = value.strip().split(',')
    
    result = []
    for item in line:
        if item == '':
            result.append(0.0)
        else:
            result.append(float(item))
            
    return result

def read_csv_columnar(fName):
    file = open(fName).readlines()
    result = {}
  
    amount = []
    duration = []
    rate = []
    down_payment = []
    lines = []
    
    headers = parse_headers(file[0])
    
    for line in file[1:]:
        value = parse_data(line)
        
        lines.append(value)
        amount.append(value[0])
        duration.append(value[1])
        rate.append(value[2])
        down_payment.append(value[3])
        
    result[headers[0]] = amount
    result[headers[1]] = duration
    result[headers[2]] = rate
    result[headers[3]] = down_payment
    
    return result

def write_csv_columnar(data, path):

    with open(path,'w') as f:
        
        if len(data) == 0:
            return
        
        headers = list(data.keys())
        f.write(", ".join(headers) + "\n")

        for i in range(len(data['amount'])):
            item = ''
            for row in data.values(): # 5 rows
                item += str(row[i])+","

            f.write(item.rstrip(",")+"\n")

# data = read_csv_columnar('./data2/loan1.txt')
# compute_emis(data)
# write_csv_columnar(data, './data2/emis3.csv')


for i in range(1,4):
    filename = './data2/loan{}.txt'.format(i)
    print(filename)

    data = read_csv_columnar(filename)
    compute_emis(data)
    write_csv_columnar(data, './data2/emis{}.csv'.format(i)) 