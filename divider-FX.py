import bitcoin
import random, math
from decimal import Decimal
from lib.secp256k1_lib import pubkey_to_ETH_address, hash_to_address, pubkey_to_h160, scalar_multiplication, point_sequential_increment, point_sequential_decrement, read_bloom_file, check_in_bloom
from time import time
from random import randint
from sys import argv
from os import system, path, name, mkdir
from secrets import token_hex
import glob, pathlib
from colorama import Back, Fore, Style, init
init(autoreset = True)

class color:
    yellow = Fore.YELLOW+Style.BRIGHT
    red = Fore.RED+Style.BRIGHT
    clear = Style.RESET_ALL
    green = Fore.GREEN+Style.BRIGHT
    blink = Fore.RED+Style.DIM
    cyan = Fore.CYAN+Style.BRIGHT
    back = '\033[1A'
    clear_screen = '\x1b[2J'

version = '1.2'

def cls():
    system('cls' if name=='nt' else 'clear')

class BF():
    def __init__(self, file_bf) -> None:
        if path.exists(file_bf):
            self.bit, self.hash, self.bf = read_bloom_file(file_bf)
        else:
            print(f'[E] File bloomfilter: {file_bf} not found.')
            exit(1)

def save_file(infile, text):
    if path.exists('log'):
        file = f'log/{infile}.log'
        f = open(file, 'a', encoding='utf-8', errors='ignore')
        f.write(f'[*] {text} \n')
        f.close()
    else:
        mkdir('log')
        file = f'log/{infile}.log'
        f = open(file, 'a', encoding='utf-8', errors='ignore')
        f.close()
    
def convert_int(num:int):
    dict_suffix = {0:'key', 1:'Kkey', 2:'Mkey', 3:'Gkey', 4:'Tkey', 5:'Pkey', 6:'Ekeys'}
    num *= 2.0
    idx = 0
    for ii in range(len(dict_suffix)-1):
        if int(num/1000) > 0:
            idx += 1
            num /= 1000
    return ('%.2f'%num), dict_suffix[idx]

def seq(dir):
    list_btc:list = []
    list_eth:list = []
    list_alt:list = []
    cbtc:bool = False
    ceth:bool = False
    calt:bool = False
    fff = 1000 # Начальный делитель Аналог 1.00
    fff1 = 100 # Прирощение делителя Аналог 0.01
    group_size = 50000 # Сколько проверять в + и в -
    begin_key = randint(2**255,2**256)
    cycle1 = 100 # Количество циклов на прирощение делителя
    cycle2 = 100000 # Количество циклов деления (чем меньше делитель тем больше циклов надо)
    l = []
    counter = 0
    total = 0
    plus = 0
    print('-'*70,end='\n')
    currentDirectory = pathlib.Path(dir)
    currentPattern = "btc*.bin"
    for currentFile in currentDirectory.glob(currentPattern):  
        #print(currentFile)
        list_btc.append(BF(currentFile))
        cbtc = True
    currentPattern = "eth*.bin"
    for currentFile in currentDirectory.glob(currentPattern):  
        #print(currentFile)
        list_eth.append(BF(currentFile))
        ceth = True
    currentPattern = "alt*.bin"
    for currentFile in currentDirectory.glob(currentPattern):
        #print(currentFile)
        list_alt.append(BF(currentFile))
        calt = True
    if len(list_btc) + len(list_eth) + len(list_alt) == 0:
        print(f'{color.red}bloom filters not found in folder {dir}')
        exit(0)
    print(f'[I] {color.green}Bloomfilter loaded...')
    print('-'*70,end='\n')

    while True:
        for _ in range(cycle1):
            counter = 0
            total = 0
            n = begin_key-plus # randint(2**255,2**256)
            print(f'[I] Version: {version}')
            print(f'[I] PVK:{hex(n)}')
            fff = fff + fff1
            print('\n')
            for _ in range(cycle2):
                st = time()
                counter = 0
                a1, tmp = divmod(n, fff)
                n = n - a1
                #print(f'[I] PVK:{hex(n)}')
                # n = math.floor(n / fff)
                #n = int(n / fff)
                if n < fff: 
                    break
                P = scalar_multiplication(n)
                current_pvk1 = n + 1
                current_pvk2 = n - 1
                Pv = point_sequential_increment(group_size, P)
                for t in range(group_size):
                    pub = Pv[t*65:t*65+65]
                    if cbtc:
                        hash160 = pubkey_to_h160(0,True,pub)
                        hash160_u = pubkey_to_h160(0,False,pub)
                        hash160_3 = pubkey_to_h160(1,True,pub)
                        for check in list_btc:
                            if check_in_bloom(hash160.hex(), check.bit, check.hash, check.bf) or check_in_bloom(hash160_u.hex(), check.bit, check.hash, check.bf) or check_in_bloom(hash160_3.hex(), check.bit, check.hash, check.bf):
                                if hash160.hex() not in l or hash160_3.hex() not in l or hash160_u.hex() not in l:
                                    print(f'[F increment] global:{n} F:{fff} {hex(current_pvk1 + t)} {hash160.hex()} {hash160_u.hex()} {hash160_3.hex()}')
                                    save_file('found',f'[F increment] global:{n} F:{fff} {hex(current_pvk1 + t)} {hash160.hex()} {hash160_u.hex()} {hash160_3.hex()}\n')
                                    l.append(hash160.hex())
                                    l.append(hash160_u.hex())
                                    l.append(hash160_3.hex())
                            counter += 1
                    if calt:
                        hash160 = pubkey_to_h160(0,True,pub)
                        hash160_u = pubkey_to_h160(0,False,pub)
                        hash160_3 = pubkey_to_h160(1,True,pub)
                        for check in list_btc:
                            if check_in_bloom(hash160.hex(), check.bit, check.hash, check.bf) or check_in_bloom(hash160_u.hex(), check.bit, check.hash, check.bf) or check_in_bloom(hash160_3.hex(), check.bit, check.hash, check.bf):
                                if hash160.hex() not in l or hash160_3.hex() not in l or hash160_u.hex() not in l:
                                    print(f'[F increment] global:{n} F:{fff} {hex(current_pvk1 + t)} {hash160.hex()} {hash160_u.hex()} {hash160_3.hex()}')
                                    save_file('found',f'[F increment] global:{n} F:{fff} {hex(current_pvk1 + t)} {hash160.hex()} {hash160_u.hex()} {hash160_3.hex()}\n')
                                    l.append(hash160.hex())
                                    l.append(hash160_u.hex())
                                    l.append(hash160_3.hex())
                            counter += 1
                    if ceth:
                        eth = pubkey_to_ETH_address(pub)[2:]
                        for check in list_eth:
                            if check_in_bloom(eth, check.bit, check.hash, check.bf):
                                if eth not in l:
                                    print(f'[F increment] global:{n} F:{fff} {hex(current_pvk1 + t)} {eth} ')
                                    save_file('found',f'[F increment] global:{n} F:{fff} {hex(current_pvk1 + t)} {eth}\n')
                                    l.append(eth)
                            counter += 1

                total += 1

                Pv = point_sequential_decrement(group_size, P)
                for t in range(group_size):
                    pub = Pv[t*65:t*65+65]
                    if cbtc:
                        hash160 = pubkey_to_h160(0,True,pub)
                        hash160_u = pubkey_to_h160(0,False,pub)
                        hash160_3 = pubkey_to_h160(1,True,pub)
                        for check in list_btc:
                            if check_in_bloom(hash160.hex(), check.bit, check.hash, check.bf) or check_in_bloom(hash160_u.hex(), check.bit, check.hash, check.bf) or check_in_bloom(hash160_3.hex(), check.bit, check.hash, check.bf):
                                if hash160.hex() not in l or hash160_3.hex() not in l or hash160_u.hex() not in l:
                                    print(f'[F increment] global:{n} F:{fff} {hex(current_pvk2 - t)} {hash160.hex()} {hash160_u.hex()} {hash160_3.hex()}')
                                    save_file('found',f'[F increment] global:{n} F:{fff} {hex(current_pvk2 - t)} {hash160.hex()} {hash160_u.hex()} {hash160_3.hex()}\n')
                                    l.append(hash160.hex())
                                    l.append(hash160_u.hex())
                                    l.append(hash160_3.hex())
                        counter += 1
                    if calt:
                        hash160 = pubkey_to_h160(0,True,pub)
                        hash160_u = pubkey_to_h160(0,False,pub)
                        hash160_3 = pubkey_to_h160(1,True,pub)
                        for check in list_btc:
                            if check_in_bloom(hash160.hex(), check.bit, check.hash, check.bf) or check_in_bloom(hash160_u.hex(), check.bit, check.hash, check.bf) or check_in_bloom(hash160_3.hex(), check.bit, check.hash, check.bf):
                                if hash160.hex() not in l or hash160_3.hex() not in l or hash160_u.hex() not in l:
                                    print(f'[F increment] global:{n} F:{fff} {hex(current_pvk2 - t)} {hash160.hex()} {hash160_u.hex()} {hash160_3.hex()}')
                                    save_file('found',f'[F increment] global:{n} F:{fff} {hex(current_pvk2 - t)} {hash160.hex()} {hash160_u.hex()} {hash160_3.hex()}\n')
                                    l.append(hash160.hex())
                                    l.append(hash160_u.hex())
                                    l.append(hash160_3.hex())
                            counter += 1
                    if ceth:
                        eth = pubkey_to_ETH_address(pub)[2:]
                        for check in list_eth:
                            if check_in_bloom(eth, check.bit, check.hash, check.bf):
                                if eth not in l:
                                    print(f'[F increment] global:{n} F:{fff} {hex(current_pvk2 - t)} {eth} ')
                                    save_file('found',f'[F increment] global:{n} F:{fff} {hex(current_pvk2 - t)} {eth}\n')
                                    l.append(eth)
                        counter += 1
                total += 1
                print(f'[+] Total Keys Checked : {total}  F:{fff:.2f} PVK:{hex(n)[:12]}... [ Speed : {counter/(time() - st):.2f} Keys/s ] ', end='\r')
                counter = 0
        plus += 1
if __name__ == "__main__":  
    cls()
    bf_dir = argv[1]
    # file_in = argv[1]
    # file_out = argv[2]
    # if len (argv) < 3:
    #     print ("[E] Error. Too few options.")
    #     exit(1)

    # if len (argv) > 3:
    #     print ("[E] Error. Too many parameters.")
    #     exit(1)
    seq(bf_dir)