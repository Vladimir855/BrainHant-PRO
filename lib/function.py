# #!/usr/bin/python3
# encoding=utf-8
# -*- coding: utf-8 -*-
"""
@author: NonameHUNT
@GitHub: https://github.com/Noname400
@telegram: https://t.me/NonameHunt
"""
version_lib = 'LIB 3.1/16.01.23'

from multiprocessing import Pool, freeze_support, cpu_count
from time import time, sleep
from argparse import ArgumentParser
from signal import SIGINT, SIG_IGN, signal
from codecs import open
from urllib.request import urlopen
from requests import get
from sys import stdin
from os import path, environ, mkdir
from datetime import datetime
from Crypto.Hash import keccak
import glob, pathlib
from io import TextIOWrapper
from json import loads, dump
from .secp256k1_lib import privatekey_to_ETH_address, pubkey_to_h160, scalar_multiplication, pubkey_to_ETH_address, get_sha256, read_bloom_file, check_in_bloom, point_sequential_increment, point_sequential_decrement
from bitcoin import mul_privkeys, inv, N, random_key
import string, secrets, random
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

class BF():
    def __init__(self, file_bf) -> None:
        if path.exists(file_bf):
            self.bit, self.hash, self.bf = read_bloom_file(file_bf)
        else:
            print(f'[E] File bloomfilter: {file_bf} not found.')
            exit(1)

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
        f = open(file,'a')
        f = open(file, 'a', encoding='utf-8', errors='ignore')
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
        print(f'[W] {color.red}The settings file is missing. Download from server.')
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
    if raw:
        pvk_i = int(text,16)
        pub_raw = scalar_multiplication(pvk_i)
        current_pvk1 = pvk_i + 1
        current_pvk2 = pvk_i - 1
        f1 = []
        if cb or ca:
            f1.append(['btc', text, pvk_i, pubkey_to_h160(0, False, pub_raw),'BTC/ALT RAW'])
            f1.append(['btc', text ,pvk_i, pubkey_to_h160(0, True, pub_raw),'BTC/ALT RAW'])
            f1.append(['btc', text, pvk_i, pubkey_to_h160(1, True, pub_raw),'BTC/ALT RAW'])
            if incdec > 1:
                res_pub = point_sequential_increment(incdec, pub_raw)
                for dec2 in range(incdec):
                    pub2 = res_pub[dec2*65:dec2*65+65]
                    f1.append(['btc', text, current_pvk1+dec2, pubkey_to_h160(0, False, pub2),'BTC/ALT RAW INC'])
                    f1.append(['btc', text ,current_pvk1+dec2, pubkey_to_h160(0, True, pub2),'BTC/ALT RAW INC'])
                    f1.append(['btc', text, current_pvk1+dec2, pubkey_to_h160(1, True, pub2),'BTC/ALT RAW INC'])
                res_pub = point_sequential_decrement(incdec, pub_raw)
                for dec2 in range(incdec):
                    pub2 = res_pub[dec2*65:dec2*65+65]
                    f1.append(['btc', text, current_pvk2-dec2, pubkey_to_h160(0, False, pub2),'BTC/ALT RAW DEC'])
                    f1.append(['btc', text ,current_pvk2-dec2, pubkey_to_h160(0, True, pub2),'BTC/ALT RAW DEC'])
                    f1.append(['btc', text, current_pvk2-dec2, pubkey_to_h160(1, True, pub2),'BTC/ALT RAW DEC'])
        if ce:
            f1.append(['eth', text, pvk_i, pubkey_to_ETH_address(pub_raw)[2:],'ETH RAW'])
            if incdec > 1:
                res_pub = point_sequential_increment(incdec, pub_raw)
                for dec2 in range(incdec):
                    pub2 = res_pub[dec2*65:dec2*65+65]
                    f1.append(['eth', text, current_pvk1+dec2, pubkey_to_ETH_address(pub2)[2:],'ETH RAW INC'])
                res_pub = point_sequential_decrement(incdec, pub_raw)
                for dec2 in range(incdec):
                    pub2 = res_pub[dec2*65:dec2*65+65]
                    f1.append(['eth', text, current_pvk2-dec2, pubkey_to_ETH_address(pub2)[2:],'ETH RAW DEC'])
        return f1
    else:
        f1 = []
        if cb or ca:
            binary_data = text if isinstance(text, bytes) else bytes(text, 'utf-8')
            hash_sha256 = get_sha256(binary_data).hex()
            pvk_i = int(hash_sha256,16)
            pub_sha256 = scalar_multiplication(pvk_i)
            current_pvk1 = pvk_i + 1
            current_pvk2 = pvk_i - 1
            f1.append(['btc', text, hash_sha256, pubkey_to_h160(0, False, pub_sha256),'BTC/ALT'])
            f1.append(['btc', text, hash_sha256, pubkey_to_h160(0, True, pub_sha256),'BTC/ALT'])
            f1.append(['btc', text, hash_sha256, pubkey_to_h160(1, True, pub_sha256),'BTC/ALT'])
            if incdec > 1:
                res_pub = point_sequential_increment(incdec,pub_sha256)
                for dec2 in range(incdec):
                    pub2 = res_pub[dec2*65:dec2*65+65]
                    f1.append(['btc', text, current_pvk1+dec2, pubkey_to_h160(0, False, res_pub),'BTC/ALT INC'])
                    f1.append(['btc', text ,current_pvk1+dec2, pubkey_to_h160(0, True, res_pub),'BTC/ALT INC'])
                    f1.append(['btc', text, current_pvk1+dec2, pubkey_to_h160(1, True, res_pub),'BTC/ALT INC'])
                res_pub = point_sequential_decrement(incdec,pub_sha256)
                for dec2 in range(incdec):
                    pub2 = res_pub[dec2*65:dec2*65+65]
                    f1.append(['btc', text, current_pvk2-dec2, pubkey_to_h160(0, False, res_pub),'BTC/ALT DEC'])
                    f1.append(['btc', text ,current_pvk2-dec2, pubkey_to_h160(0, True, res_pub),'BTC/ALT DEC'])
                    f1.append(['btc', text, current_pvk2-dec2, pubkey_to_h160(1, True, res_pub),'BTC/ALT DEC'])
        if ce:
            k = keccak.new(digest_bits=256)
            k.update(binary_data)
            hash_keccak_256 = k.hexdigest()
            pvk_i = int(hash_keccak_256,16)
            pub_keccak_256 = scalar_multiplication(pvk_i)
            current_pvk1 = pvk_i + 1
            current_pvk2 = pvk_i - 1
            f1.append(['eth',text,hash_keccak_256,pubkey_to_ETH_address(pub_keccak_256)[2:],'ETH'])
            if incdec > 1:
                res_pub = point_sequential_increment(incdec, pub_keccak_256)
                for dec2 in range(incdec):
                    pub2 = res_pub[dec2*65:dec2*65+65]
                    f1.append(['eth', text, current_pvk1+dec2, pubkey_to_ETH_address(pub2)[2:],'ETH INC'])
                res_pub = point_sequential_decrement(incdec,pub_keccak_256)
                for dec2 in range(incdec):
                    pub2 = res_pub[dec2*65:dec2*65+65]
                    f1.append(['eth', text, current_pvk2-dec2, pubkey_to_ETH_address(pub2)[2:],'ETH DEC'])
        return f1

def bw_seq(text):
    try:
        w = text[0].hex()
    except:
        w = text[0]
    h = text[1]
    cb = text[2]
    ca = text[3]
    ce = text[4]
    incdec = text[5]
    f1 = []
    pvk = h if isinstance(h, int) else int(h, 16)
    pub = scalar_multiplication(pvk)
    current_pvk1 = pvk + 1
    current_pvk2 = pvk - 1
    if cb or ca:
        f1.append(['btc',w,pvk,pubkey_to_h160(0, False, pub), 'BTC/ALT'])
        f1.append(['btc',w,pvk,pubkey_to_h160(0, True, pub), 'BTC/ALT'])
        f1.append(['btc',w,pvk,pubkey_to_h160(1, True, pub), 'BTC/ALT'])
        f1.append(['btc',w,pvk,pubkey_to_h160(2, True, pub), 'BTC/ALT'])
        if incdec > 1:
            res_pub = point_sequential_increment(incdec, pub)
            for dec2 in range(incdec):
                pub2 = res_pub[dec2*65:dec2*65+65]
                f1.append(['btc', w, current_pvk1+dec2, pubkey_to_h160(0, False, res_pub),'BTC/ALT INC'])
                f1.append(['btc', w, current_pvk1+dec2, pubkey_to_h160(0, True, res_pub),'BTC/ALT INC'])
                f1.append(['btc', w, current_pvk1+dec2, pubkey_to_h160(1, True, res_pub),'BTC/ALT INC'])
            res_pub = point_sequential_decrement(incdec, pub)
            for dec2 in range(incdec):
                pub2 = res_pub[dec2*65:dec2*65+65]
                f1.append(['btc', w, current_pvk2-dec2, pubkey_to_h160(0, False, res_pub),'BTC/ALT DEC'])
                f1.append(['btc', w, current_pvk2-dec2, pubkey_to_h160(0, True, res_pub),'BTC/ALT DEC'])
                f1.append(['btc', w, current_pvk2-dec2, pubkey_to_h160(1, True, res_pub),'BTC/ALT DEC'])
    if ce:
        f1.append(['eth', w, pvk, pubkey_to_ETH_address(pub)[2:], 'ETH'])
        if incdec > 1:
            res_pub = point_sequential_increment(incdec, pub)
            for dec2 in range(incdec):
                pub2 = res_pub[dec2*65:dec2*65+65]
                f1.append(['eth', w, current_pvk1+dec2, pubkey_to_ETH_address(pub2)[2:],'ETH INC'])
            res_pub = point_sequential_decrement(incdec, pub)
            for dec2 in range(incdec):
                pub2 = res_pub[dec2*65:dec2*65+65]
                f1.append(['eth', w, current_pvk2-dec2, pubkey_to_ETH_address(pub2)[2:],'ETH DEC'])
    return f1

def text2sha256(string):
    binary_data = string if isinstance(string, bytes) else bytes(string, 'utf-8')
    res = get_sha256(binary_data)
    return res

def text2keccak(string):
    binary_data = string if isinstance(string, bytes) else bytes(string, 'utf-8')
    k = keccak.new(digest_bits=256)
    k.update(binary_data)
    res = k.digest()
    return res

def gen_hash(text):
    text_sha = text[0]
    text_kecc = text[0]
    list_line = text[1]
    cb = text[2]
    ca = text[3]
    ce = text[4]
    raw1 = text[5]
    raw2 = text[6]
    dbg = text[7]
    div = text[8]
    incdec = text[9]
    gen = []
    
    if raw1:
        div = div if isinstance(div, int) else int(div,16)
        div = inv(div,N)
        try:
            pvk = text_sha if isinstance(text_sha, int) else int(text_sha,16)
        except:
            pvk = random.randrange(2**240,2**256)
        if dbg: print(f'Debug: {pvk} {div}')
        for _ in range(list_line):
            sha = mul_privkeys(pvk,div)
            if dbg: print(f'Debug: {sha}')
            if sha < 2**200: print(f'\n {sha} < 2**200')
            sha = hex(sha)[2:]
            gen.append([sha, sha, cb, ca, ce, incdec])
            pvk = int(sha,16)
        return gen
    elif raw2:
        for _ in range(list_line):
            try:
                text_sha = hex(text_sha if isinstance(text_sha, int) else int(text_sha,16))[2:]
            except:
                text_sha = hex(random.randrange(2**240,2**256))[2:]
            byt = bytes.fromhex(text_sha.zfill(64))
            sha = get_sha256(byt).hex()
            gen.append([sha, sha, cb, ca, ce, incdec])
            text_sha = sha
        return gen
    else:
        for _ in range(list_line):
            sha = text2sha256(text_sha)
            try:
                gen.append([text_sha.hex(), sha.hex(), cb, ca, ce, incdec])
            except:
                gen.append([text_sha, sha.hex(), cb, ca, ce, incdec])
            text_sha = sha.hex()
            
        for _ in range(list_line):
            kecc = text2keccak(text_kecc)
            try:
                gen.append([text_kecc.hex(), kecc.hex(), cb, ca, ce, incdec])
            except:
                gen.append([text_kecc, kecc.hex(), cb, ca, ce, incdec])
            text_kecc = kecc.hex()
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
