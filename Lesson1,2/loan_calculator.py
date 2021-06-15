import pprint as p
import math

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

def parse_header(header_line):
    return header_line.strip().split(",")

def parse_value(line):
    line = line.strip().split(",")
    values = []

    for item in line:
        if item == "":
            values.append(0.0)
        else:
            values.append(float(item))

    return values

def create_item_dict(header, value):
    item_dict = {}

    for h,v in zip(header,value):
        item_dict[h] = v

    return item_dict

def read_csv(fileName):
    file = open(fileName).readlines()
    result = []
    header = parse_header(file[0])

    for line in file[1:]:
        line = parse_value(line)
        result.append(create_item_dict(header, line))

    p.pprint(result)
    return result

def compute_emis(data):
    
    for line in data:
        amount = line['amount']
        duration = line['duration']
        rate = line['rate']/12
        down_payment = line['down_payment']

        line['emi'] = loan_emi(amount, duration, rate, down_payment)

def write_csv(items, path):
    # Open the file in write mode
    with open(path, 'w') as f:
        # Return if there's nothing to write
        if len(items) == 0:
            return
        
        # Write the headers in the first line
        headers = list(items[0].keys())
        f.write(','.join(headers) + '\n')
        
        # Write one item per line
        for item in items:
        
            values = []
            for header in headers:
                values.append(str(item.get(header, "")))

            f.write(','.join(values) + "\n")


for i in range(1,4):
    filename = './data/loan{}.txt'.format(i)
    print(filename)

    data = read_csv(filename)
    compute_emis(data)
    write_csv(data, './data/emis{}.csv'.format(i))

