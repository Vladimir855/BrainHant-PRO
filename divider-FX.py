# #!/usr/bin/python3
# encoding=utf-8
# -*- coding: utf-8 -*-
"""
@author: NonameHUNT
@GitHub: https://github.com/Noname400
@telegram: https://t.me/NonameHunt
"""
import bitcoin
import random, math
from decimal import Decimal
from lib.secp256k1_lib import pubkey_to_ETH_address, hash_to_address, pubkey_to_h160, scalar_multiplication, point_sequential_increment, point_sequential_decrement
from lib.hunt_lib import LibHUNT, version_LIB
from lib.function import *
from time import time
from random import randint
from sys import argv
from os import system, path, name, mkdir
from secrets import token_hex
import glob, pathlib
from colorama import Back, Fore, Style, init
init(autoreset = True)

version = 'Divider 2.3 / 13.03.23'

def init_worker():
    signal(SIGINT, SIG_IGN)

def createParser():
    parser = ArgumentParser(description='Divider-FX')
    parser.add_argument ('-dbdir', '--database_dir', action='store', type=str, help='File BF', default='')
    parser.add_argument ('-start', '--start',        action='store', type=str, help='start range', default='')
    parser.add_argument ('-end',   '--end',          action='store', type=str, help='end range', default='')
    parser.add_argument ('-group', '--group',        action='store', type=int, help='group size', default='50000')
    parser.add_argument ('-startdiv', '--startdiv',  action='store', type=int, help='start divide', default='1000')
    parser.add_argument ('-incdiv', '--incdiv',      action='store', type=int, help='step divider', default='100')
    parser.add_argument ('-inccycle', '--inccycle',  action='store', type=int, help='count cycle', default='100')
    parser.add_argument ('-divcicle', '--divcicle',  action='store', type=int, help='input raw', default='100000')

    return parser.parse_args().database_dir, parser.parse_args().start, parser.parse_args().end, parser.parse_args().group, parser.parse_args().startdiv, \
        parser.parse_args().incdiv, parser.parse_args().inccycle, parser.parse_args().divcicle
        

if __name__ == "__main__":
    freeze_support()
    cls()
    bf_dir, start, end, groud_size, start_div, inc_div, inc_cycle, div_cicle  = createParser()

    list_btc:list = []
    list_eth:list = []
    list_alt:list = []
    cbtc:bool = False
    ceth:bool = False
    calt:bool = False
    fff = start_div # Начальный делитель Аналог 1.00
    fff1 = inc_div # Прирощение делителя Аналог 0.01
    group_size = groud_size # Сколько проверять в + и в -
    begin_key = randint(int(start,16), int(end,16))
    cycle1 = inc_cycle # Количество циклов на прирощение делителя
    cycle2 = div_cicle # Количество циклов деления (чем меньше делитель тем больше циклов надо)
    l = []
    counter = 0
    total = 0
    plus = 0
    print('-'*70,end='\n')
    mask = "btc*.bin"
    list_btc = load_bf(bf_dir, mask)
    if len(list_btc) != 0:
        cbtc = True
    mask = "alt*.bin"
    list_alt = load_bf(bf_dir, mask)
    if len(list_alt) != 0:
        calt = True
    mask = "eth*.bin"
    list_eth = load_bf(bf_dir, mask)
    if len(list_eth) != 0:
        ceth = True
    if len(list_btc) + len(list_eth) + len(list_alt) == 0:
        print(f'{color.red}bloom filters not found in folder {bf_dir}')
        exit(0)
    print(f'[I] {color.green}Bloomfilter loaded...')
    print('-'*70,end='\n')
    if cbtc: 
        print(f'[I] Bloom Work:{color.cyan}BTC')
    if calt: 
        print(f'[I] Bloom Work:{color.cyan}ALT')
    if ceth: 
        print(f'[I] Bloom Work:{color.cyan}ETH')
    print('-'*70,end='\n')
    list_btc.extend(list_alt)
    list_alt = []
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
                        for BF in list_btc:
                            if BF.check(hash160) or BF.check(hash160_u) or BF.check(hash160_3):
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
                        for BF in list_alt:
                            if BF.check(hash160) or BF.check(hash160_u) or BF.check(hash160_3):
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
                            if BF.check(eth):
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
                        for BF in list_btc:
                            if BF.check(hash160) or BF.check(hash160_u) or BF.check(hash160_3):
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
                        for BF in list_alt:
                            if BF.check(hash160) or BF.check(hash160_u) or BF.check(hash160_3):
                                if hash160.hex() not in l or hash160_3.hex() not in l or hash160_u.hex() not in l:
                                    print(f'[F increment] global:{n} F:{fff} {hex(current_pvk2 - t)} {hash160.hex()} {hash160_u.hex()} {hash160_3.hex()}')
                                    save_file('found',f'[F increment] global:{n} F:{fff} {hex(current_pvk2 - t)} {hash160.hex()} {hash160_u.hex()} {hash160_3.hex()}\n')
                                    l.append(hash160.hex())
                                    l.append(hash160_u.hex())
                                    l.append(hash160_3.hex())
                        counter += 1
                    if ceth:
                        eth = pubkey_to_ETH_address(pub)[2:]
                        for BF in list_eth:
                            if BF.check(eth):
                                if eth not in l:
                                    print(f'[F increment] global:{n} F:{fff} {hex(current_pvk2 - t)} {eth} ')
                                    save_file('found',f'[F increment] global:{n} F:{fff} {hex(current_pvk2 - t)} {eth}\n')
                                    l.append(eth)
                        counter += 1
                total += 1
                print(f'[+] Total Keys Checked : {total}  F:{fff:.2f} PVK:{hex(n)[:12]}... [ Speed : {counter/(time() - st):.2f} Keys/s ] ', end='\r')
                counter = 0
        plus += 1