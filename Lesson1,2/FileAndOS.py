import os
from urllib.request import urlretrieve as urr

# try:
#     os.makedirs('./data')
#     print("Directory created successfully")
# except:
#     print("Directory creation failed")


# url = 'https://gist.githubusercontent.com/aakashns/257f6e6c8719c17d0e498ea287d1a386/raw/7def9ef4234ddf0bc82f855ad67dac8b971852ef/loans1.txt'

# try:
#     urr(url, './data/loan.txt')
#     print("File created successfully")
# except:
#     print("File creation failed")

store = dict()

with open('./data/loan.txt') as f:
    file = f.readlines()
    

    result = {}
    
    def create_dict(values, headers):
        for val, head in zip(values, headers):
            result[head] = val

        return result

    headers = file[0].strip().split(',')
    for lines in file[1:]:
        line = lines.rstrip('\n').split(',')
        create_dict(line, headers)
    

    print(result)


