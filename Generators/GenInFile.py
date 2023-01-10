import itertools
import sys
import datetime, time
from itertools import combinations_with_replacement,product
import string

def load_txt(name):
    data = []
    with open(name, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            data.append(line.strip())
    return data

if __name__ == '__main__':
    co = 0
    num = 0
    
    filename = input("Введите имя файла > ")
    if filename == '': exit(1)
    data = load_txt(f'wordlist/{filename}')
    
    maxLength = input("скольки слов генерировать ? (например указав 5 будут сгенерированы все комбинации от 1 слова до 5) > ")
    if int(maxLength) == 0: exit(1)

    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    w = open(f'out{num}.txt','w', encoding='utf-8')
    pwd = product(data, repeat = int(maxLength))
    for i in pwd:
        co += 1
        password = "".join(i)
        #sys.stdout.write(password)
        #print(password)
        w.write(password+'\n')
        if co == 1000000000:
            w.close()
            co = 0
            num += 1
            w = open(f'out{num}.txt','w', encoding='utf-8')
            print(f'Достигнута точка 1 000 000 000')
            print(f'Новый файл - out{num}.txt')
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    w.close()
