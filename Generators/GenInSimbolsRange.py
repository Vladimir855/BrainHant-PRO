import itertools
import sys
import datetime, time
from itertools import combinations_with_replacement,product
import string


if __name__ == '__main__':
    co = 0
    num = 0
    pwdKeys = input("введите слова или символы через ;> ").split(';')
    if len(pwdKeys[0].strip()) == 0: exit(1)

    maxLength = input("Сколько символов в пароле > ")
    if len(maxLength) == 0: exit(1)

    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    w = open(f'out{num}.txt','w', encoding='utf-8')
    for i in range(int(maxLength)):
        pwd = product(pwdKeys, repeat = int(i+1))
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