# #!/usr/bin/python3
# encoding=utf-8
# -*- coding: utf-8 -*-
"""
@author: NonameHUNT
@GitHub: https://github.com/Noname400
@telegram: https://t.me/NonameHunt
"""
version_lib = 'LIB 3.10/14.02.23'

from multiprocessing import Pool, freeze_support, cpu_count
from time import time, sleep
from argparse import ArgumentParser
from signal import SIGINT, SIG_IGN, signal
from codecs import open
from urllib.request import urlopen
from requests import get
from sys import stdin
from os import path, environ, mkdir, system, name, makedirs
from datetime import datetime
import glob, pathlib
from io import TextIOWrapper
from json import loads, dump
from .secp256k1_lib import pubkey_to_h160, scalar_multiplication, point_sequential_increment, point_sequential_decrement, pubkey_to_ETH_address, get_sha256
from .libhunt import LibHUNT, version_LIB
from bitcoin import mul_privkeys, inv, N, random_key
import string, secrets, random
from .patina import HashMap
from colorama import Back, Fore, Style, init
init(autoreset = True)

alphabet = string.ascii_letters + string.digits

class color:
    yellow = Fore.YELLOW+Style.BRIGHT
    red = Fore.RED+Style.BRIGHT
    clear = Style.RESET_ALL
    green = Fore.GREEN+Style.BRIGHT
    blink = Fore.RED+Style.DIM
    cyan = Fore.CYAN+Style.BRIGHT
    back = '\033[1A'
    clear_screen = '\x1b[2J'

def rescan(hash160, pref, _path):
    tmp = False
    _path = _path.replace('\\', '/')
    if _path[-1] != '\\' or path[-1] != '/':
        _path += '/'
    pp = _path+pref+'.rescan'
    print(f'[I] {color.cyan} Enable rescan {pref} {hash160.hex()}')
    if path.exists(pp):
        hm = HashMap.load2(_path+pref+'.rescan')
        tmp = hm.contains_key(hash160.hex())
        del hm
        return tmp
    else: 
        print(f'[W] {color.red}File {_path}{pref}.rescan is missing')
        print(f'[W] {color.red} Mode Recheck Disable')
        return None
        
def load_bf(path, mask):
    bf_list = []
    path = path.replace('\\', '/')
    if path[-1] != '\\' or path[-1] != '/':
        path += '/'
    currentDirectory = pathlib.Path(path)
    for currentFile in currentDirectory.glob(mask):
        bf = LibHUNT(2000, 0.01)
        #print(path+currentFile.name)
        result = bf.load(path+currentFile.name)
        #print(f'Result - {result}')
        if result == None:
            pass
            #print("filter load successfully")
        else:
            #print("Error load the filter")
            exit()
        bf_list.append(bf)
    return bf_list

def cls():
    system('cls' if name=='nt' else 'clear')

def gen_word():
    word = ''.join(secrets.choice(alphabet) for i in range(random.randrange(2,32)))
    return ''.join(word)

def convert_int(num:int):
    dict_suffix = {0:'key', 1:'Kkey', 2:'Mkey', 3:'Gkey', 4:'Tkey', 5:'Pkey', 6:'Ekeys'}
    num *= 1.0
    idx = 0
    for ii in range(len(dict_suffix)-1):
        if int(num/1000) > 0:
            idx += 1
            num /= 1000
    return ('%.2f'%num), dict_suffix[idx]

def send_telegram(text: str, telegram_channel_id, telegram_token):
    try:
        get('https://api.telegram.org/bot{}/sendMessage'.format(telegram_token), params=dict(
        chat_id=telegram_channel_id,
        text=text))
    except:
        print(f'[E] {color.red}Error send telegram. Reconnect.')
        return False
    else: 
        return True

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
        f.write(f'[*] {text} \n')
        f.close()
        
def load_configure(file):
    if path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            try:
                data = loads(f.read())
            except:
                pass
                return None
            else:
                return data
    else: 
        print(f'[W] {color.red}The settings file is missing.')
        exit(1)

def date_str():
    now = datetime.now()
    return now.strftime("%Y/%m/%d/, %H:%M:%S")

def bw(input_list):
    text = input_list[0]
    raw = input_list[1]
    cb = input_list[2]
    ca = input_list[3]
    ce = input_list[4]
    incdec = input_list[5]
    pvk_i = int(text,16)
    pub_raw = scalar_multiplication(pvk_i)
    current_pvk1 = pvk_i + 1
    current_pvk2 = pvk_i - 1
    if incdec > 1:
        res_pub_inc = point_sequential_increment(incdec, pub_raw)
        res_pub_dec = point_sequential_decrement(incdec, pub_raw)
    if raw:
        f1 = []
        if cb or ca:
            f1.append(['btc', text, pvk_i, pubkey_to_h160(0, False, pub_raw), f'BTC/ALT RAW'])
            f1.append(['btc', text, pvk_i, pubkey_to_h160(0, True, pub_raw), f'BTC/ALT RAW'])
            f1.append(['btc', text, pvk_i, pubkey_to_h160(1, True, pub_raw), f'BTC/ALT RAW'])
            if incdec > 1:
                for inc2 in range(incdec):
                    pub2 = res_pub_inc[inc2*65:inc2*65+65]
                    f1.append(['btc', text, current_pvk1+inc2, pubkey_to_h160(0, False, pub2), f'BTC/ALT RAW INC {inc2}'])
                    f1.append(['btc', text, current_pvk1+inc2, pubkey_to_h160(0, True, pub2), f'BTC/ALT RAW INC {inc2}'])
                    f1.append(['btc', text, current_pvk1+inc2, pubkey_to_h160(1, True, pub2), f'BTC/ALT RAW INC {inc2}'])
                for dec2 in range(incdec):
                    pub2 = res_pub_dec[dec2*65:dec2*65+65]
                    f1.append(['btc', text, current_pvk2-dec2, pubkey_to_h160(0, False, pub2), f'BTC/ALT RAW DEC {dec2}'])
                    f1.append(['btc', text, current_pvk2-dec2, pubkey_to_h160(0, True, pub2), f'BTC/ALT RAW DEC {dec2}'])
                    f1.append(['btc', text, current_pvk2-dec2, pubkey_to_h160(1, True, pub2), f'BTC/ALT RAW DEC {dec2}'])
        if ce:
            f1.append(['eth', text, pvk_i, bytes.fromhex(pubkey_to_ETH_address(pub_raw)),'ETH RAW'])
            if incdec > 1:
                res_pub = point_sequential_increment(incdec, pub_raw)
                for inc2 in range(incdec):
                    pub2 = res_pub_inc[inc2*65:inc2*65+65]
                    f1.append(['eth', text, current_pvk1+inc2, bytes.fromhex(pubkey_to_ETH_address(pub2)),f'ETH RAW INC {inc2}'])
                res_pub = point_sequential_decrement(incdec, pub_raw)
                for dec2 in range(incdec):
                    pub2 = res_pub_dec[dec2*65:dec2*65+65]
                    f1.append(['eth', text, current_pvk2-dec2, bytes.fromhex(pubkey_to_ETH_address(pub2)),f'ETH RAW DEC {dec2}'])
        return f1
    else:
        f1 = []
        binary_data = text if isinstance(text, bytes) else bytes(text, 'utf-8')
        hash_sha256 = get_sha256(binary_data).hex()
        pvk_i = int(hash_sha256, 16)
        pub_raw = scalar_multiplication(pvk_i)
        current_pvk1 = pvk_i + 1
        current_pvk2 = pvk_i - 1
        if cb or ca:
            f1.append(['btc', text, hash_sha256, pubkey_to_h160(0, False, pub_raw), 'BTC/ALT'])
            f1.append(['btc', text, hash_sha256, pubkey_to_h160(0, True, pub_raw), 'BTC/ALT'])
            f1.append(['btc', text, hash_sha256, pubkey_to_h160(1, True, pub_raw), 'BTC/ALT'])
            if incdec > 1:
                for inc2 in range(incdec):
                    pub2 = res_pub_inc[inc2*65:inc2*65+65]
                    f1.append(['btc', text, current_pvk1+inc2, pubkey_to_h160(0, False, pub2),f'BTC/ALT INC {inc2}'])
                    f1.append(['btc', text ,current_pvk1+inc2, pubkey_to_h160(0, True, pub2),f'BTC/ALT INC {inc2}'])
                    f1.append(['btc', text, current_pvk1+inc2, pubkey_to_h160(1, True, pub2),f'BTC/ALT INC {inc2}'])
                res_pub = point_sequential_decrement(incdec, pub_raw)
                for dec2 in range(incdec):
                    pub2 = res_pub_dec[dec2*65:dec2*65+65]
                    f1.append(['btc', text, current_pvk2-dec2, pubkey_to_h160(0, False, pub2),f'BTC/ALT DEC {dec2}'])
                    f1.append(['btc', text ,current_pvk2-dec2, pubkey_to_h160(0, True, pub2),f'BTC/ALT DEC {dec2}'])
                    f1.append(['btc', text, current_pvk2-dec2, pubkey_to_h160(1, True, pub2),f'BTC/ALT DEC {dec2}'])
        if ce:
            f1.append(['eth', text, hash_sha256, bytes.fromhex(pubkey_to_ETH_address(pub_raw)), 'ETH'])
            if incdec > 1:
                for inc2 in range(incdec):
                    pub2 = res_pub[inc2*65:inc2*65+65]
                    f1.append(['eth', text, current_pvk1+inc2, bytes.fromhex(pubkey_to_ETH_address(pub2)),f'ETH INC {inc2}'])
                for dec2 in range(incdec):
                    pub2 = res_pub[dec2*65:dec2*65+65]
                    f1.append(['eth', text, current_pvk2-dec2, bytes.fromhex(pubkey_to_ETH_address(pub2)),f'ETH DEC {dec2}'])
        return f1

def bw_seq(input_list):
    try:
        w = input_list[0].hex()
    except:
        w = input_list[0]
    h = input_list[1]
    cb = input_list[2]
    ca = input_list[3]
    ce = input_list[4]
    incdec = input_list[5]
    f1 = []
    pvk = h if isinstance(h, int) else int(h, 16)
    pub_raw = scalar_multiplication(pvk)
    current_pvk1 = pvk + 1
    current_pvk2 = pvk - 1
    if incdec > 1:
        res_pub_inc = point_sequential_increment(incdec, pub_raw)
        res_pub_dec = point_sequential_decrement(incdec, pub_raw)
    if cb or ca:
        f1.append(['btc',w,pvk,pubkey_to_h160(0, False, pub_raw), 'BTC/ALT'])
        f1.append(['btc',w,pvk,pubkey_to_h160(0, True, pub_raw), 'BTC/ALT'])
        f1.append(['btc',w,pvk,pubkey_to_h160(1, True, pub_raw), 'BTC/ALT'])
        if incdec > 1:
            for inc2 in range(incdec):
                pub2 = res_pub_inc[inc2*65:inc2*65+65]
                f1.append(['btc', w, current_pvk1+inc2, pubkey_to_h160(0, False, pub2), f'BTC/ALT INC {inc2}'])
                f1.append(['btc', w, current_pvk1+inc2, pubkey_to_h160(0, True, pub2), f'BTC/ALT INC {inc2}'])
                f1.append(['btc', w, current_pvk1+inc2, pubkey_to_h160(1, True, pub2), f'BTC/ALT INC {inc2}'])
            for dec2 in range(incdec):
                pub2 = res_pub_dec[dec2*65:dec2*65+65]
                f1.append(['btc', w, current_pvk2-dec2, pubkey_to_h160(0, False, pub2), f'BTC/ALT DEC {dec2}'])
                f1.append(['btc', w, current_pvk2-dec2, pubkey_to_h160(0, True, pub2), f'BTC/ALT DEC {dec2}'])
                f1.append(['btc', w, current_pvk2-dec2, pubkey_to_h160(1, True, pub2), f'BTC/ALT DEC {dec2}'])
    if ce:
        f1.append(['eth', w, pvk, bytes.fromhex(pubkey_to_ETH_address(pub_raw)), 'ETH'])
        if incdec > 1:
            for inc2 in range(incdec):
                pub2 = res_pub_inc[inc2*65:inc2*65+65]
                f1.append(['eth', w, current_pvk1+inc2, bytes.fromhex(pubkey_to_ETH_address(pub2)), f'ETH INC {inc2}'])
            for dec2 in range(incdec):
                pub2 = res_pub_dec[dec2*65:dec2*65+65]
                f1.append(['eth', w, current_pvk2-dec2, bytes.fromhex(pubkey_to_ETH_address(pub2)), f'ETH DEC {dec2}'])
    return f1

def gen_hash(input_list):
    text = input_list[0]
    list_line = input_list[1]
    cb = input_list[2]
    ca = input_list[3]
    ce = input_list[4]
    raw1 = input_list[5]
    raw2 = input_list[6]
    dbg = input_list[7]
    div = input_list[8]
    incdec = input_list[9]
    gen = []
    
    if raw1:
        div = div if isinstance(div, int) else int(div, 16)
        div = inv(div, N)
        try:
            pvk = text if isinstance(text, int) else int(text, 16)
        except:
            pvk = random.randrange(2**240, 2**256)
        if dbg: print(f'Debug: {pvk} {div}')
        for _ in range(list_line):
            sha = mul_privkeys(pvk, div)
            if dbg: print(f'Debug: {sha}')
            if sha < 2**200: print(f'\n {sha} < 2**200')
            sha = hex(sha)[2:]
            gen.append([sha, sha, cb, ca, ce, incdec])
            pvk = int(sha, 16)
        return gen
    elif raw2:
        for _ in range(list_line):
            try:
                text = hex(text if isinstance(text, int) else int(text,16))[2:]
            except:
                text = hex(random.randrange(2**240, 2**256))[2:]
            byt = bytes.fromhex(text.zfill(64))
            sha = get_sha256(byt).hex()
            gen.append([sha, sha, cb, ca, ce, incdec])
            text = sha
        return gen
    else:
        for _ in range(list_line):
            text = text if isinstance(text, bytes) else bytes(text, 'utf-8')
            sha = get_sha256(text)
            try:
                gen.append([text.hex(), sha.hex(), cb, ca, ce, incdec])
            except:
                gen.append([text, sha.hex(), cb, ca, ce, incdec])
            text = sha.hex()
        return gen

def save_station(id, conti):
    data_local = load_configure('setings.json')
    if data_local == None: pass
    else:
        data_local['general'][f'continue_point{id}@'] = conti
        with open("setings.json", "w", encoding='utf-8') as write_file:
            dump(data_local, write_file, indent = 4)
            
def save_station_ex(id, conti):
    data_local = load_configure('setings.json')
    if data_local == None: pass
    else:
        data_local['general'][f'continue_point_ex{id}@'] = conti
        with open("setings.json", "w", encoding='utf-8') as write_file:
            dump(data_local, write_file, indent = 4)
            
def save_station_seq(id, hash):
    data_local = load_configure('setings.json')
    if data_local == None: pass
    else:
        data_local['general'][f'continue_point_seq{id}@'] = hash
        with open("setings.json", "w", encoding='utf-8') as write_file:
            dump(data_local, write_file, indent = 4)
            
def save_station_all_bloom(id, conti):
    data_local = load_configure('setings.json')
    if data_local == None: pass
    else:
        data_local['general'][f'continue_point_classic_all_bloom{id}@'] = conti
        with open("setings.json", "w", encoding='utf-8') as write_file:
            dump(data_local, write_file, indent = 4)