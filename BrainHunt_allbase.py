# #!/usr/bin/python3
# encoding=utf-8
# -*- coding: utf-8 -*-
"""
@author: Noname400
@GitHub https://github.com/Noname400
"""

from lib.function import *

yellow = Fore.YELLOW+Style.BRIGHT
red = Fore.RED+Style.BRIGHT
clear = Style.RESET_ALL
green = Fore.GREEN+Style.BRIGHT
blink = Fore.RED+Style.DIM
cyan = Fore.CYAN+Style.BRIGHT
back = '\033[1A'
clear_screen = '\x1b[2J'

def init_worker():
    signal(SIGINT, SIG_IGN)

def createParser():
    parser = ArgumentParser(description='BrainHunt Classic All Bloom')
    parser.add_argument ('-th', '--threading', action='store', type=int, help='threading', default='1')
    parser.add_argument ('-db', '--database', action='store', type=str, help='File BF', default='')
    parser.add_argument ('-in', '--infile', action='store', type=str, help='infile', default='')
    parser.add_argument ('-telegram', '--telegram', action='store_true', help='enable update')
    parser.add_argument ('-id', '--id', action='store', type=int, help='threading', default='0')
    parser.add_argument ('-desc', '--desc', action='store', type=str, help='description', default='local')
    parser.add_argument ('-save', '--save', action='store', type=int, help='save continue sec', default='60')
    parser.add_argument ('-minout', '--minout', action='store_true', help='minimal out console')
    parser.add_argument ('-raw', '--raw', action='store_true', help='input raw')
    return parser.parse_args().threading, parser.parse_args().database, \
        parser.parse_args().infile, parser.parse_args().telegram, parser.parse_args().id, parser.parse_args().desc, parser.parse_args().save, parser.parse_args().minout, parser.parse_args().raw
        
if __name__ == "__main__":
    freeze_support()
    print(clear_screen)
    local_version_brain:float = 0.0
    telegram_token:str = ''
    telegram_channel_id:str = ''
    telegram_enable:bool = False
    continue_point:int = -1
    th:int = 1
    in_file = ''
    cbtc:bool = False
    ceth:bool = False
    calt:bool = False
    bf0 = BF
    bf1 = BF
    bf2 = BF
    bf3 = BF
    bf4 = BF
    bf5 = BF
    bf6 = BF
    bf7 = BF
    bf8 = BF
    bf9 = BF
    bf10 = BF
    bf11 = BF
    bf12 = BF
    bf13 = BF
    bf14 = BF
    bf15 = BF
    bf16 = BF
    bf17 = BF
    bfeth0 = BF
    bfeth1 = BF
    bfeth2 = BF
    bfeth3 = BF
    bfalt0 = BF
    data_local:any
    desc:str = 'local'
    id:int = 0
    save = 30
    minout = False
    raw:bool = False
    th, dbdir, in_file, telegram_enable, id, desc, save, minout, raw  = createParser()

    data_local = load_configure('setings.json')
    try:
        local_version_brain:float = data_local['general']['version_brain_btc_all_bloom']
        telegram_token = data_local['telegram']['token']
        telegram_channel_id = data_local['telegram']['id']
        continue_point = data_local['general'][f'continue_point_classic_all_bloom{id}@']
    except:
        print(f'[E] {red}Please Update file configuration!')
        exit(1)
        
    print('-'*70,end='\n')
    print(f'{green}Thank you very much: @iceland2k14 for his libraries!')

    if th < 1:
        print('[E] The number of processes must be greater than 0')
        th = 1

    if telegram_enable:
        telegram_enable = send_telegram(f'[I] Version BrainHunt Classic All bloom: {local_version_brain} ID:{id} desc:{desc} Start programm: {date_str()}', telegram_channel_id, telegram_token)

    print('-'*70,end='\n')
    print(f'[I] Version BrainHunt: {cyan}v{local_version_brain} Classic ALL BLOOM')
    print(f'[I] Start proogramm: {cyan}{date_str()}')
    print(f'[I] Total kernel of CPU: {cyan}{cpu_count()}')
    print(f'[I] Used kernel: {cyan}{th}')
    print(f'[I] Used file: {cyan}{in_file}')
    print(f'[I] Used ID: {cyan}{id}')
    print(f'[I] Database Bloom Filter: {cyan}{dbdir}')
    if minout: print(f'[I] minimalistic OUT console: {cyan}Enable')
    else: print(f'[I] minimalistic OUT console: {red}Disabled')
    if raw: print(f'[I] Input Raw private key: {green}Enable')
    else: print(f'[I] Input Raw private key: {red}Disabled')
    if telegram_enable: print(f'[I] Send telegram: {green}Enable')
    else: print(f'[I] Send telegram: {red}Disabled')
    print('-'*70,end='\n')
    cbtc = True # Включить если BTC
    bf0.bit, bf0.hash, bf0.bf  = load_BF(dbdir+'BTCFull00.bf')
    bf1.bit, bf1.hash, bf1.bf = load_BF(dbdir+'BTCFull01.bf')
    bf2.bit, bf2.hash, bf2.bf = load_BF(dbdir+'BTCFull02.bf')
    bf3.bit, bf3.hash, bf3.bf = load_BF(dbdir+'BTCFull03.bf')
    bf4.bit, bf4.hash, bf4.bf = load_BF(dbdir+'BTCFull04.bf')
    bf5.bit, bf5.hash, bf5.bf = load_BF(dbdir+'BTCFull05.bf')
    bf6.bit, bf6.hash, bf6.bf = load_BF(dbdir+'BTCFull06.bf')
    bf7.bit, bf7.hash, bf7.bf = load_BF(dbdir+'BTCFull07.bf')
    bf8.bit, bf8.hash, bf8.bf = load_BF(dbdir+'BTCFull08.bf')
    bf9.bit, bf9.hash, bf9.bf = load_BF(dbdir+'BTCFull09.bf')
    bf10.bit, bf10.hash, bf10.bf = load_BF(dbdir+'BTCFull10.bf')
    bf11.bit, bf11.hash, bf11.bf = load_BF(dbdir+'BTCFull11.bf')
    bf12.bit, bf12.hash, bf12.bf = load_BF(dbdir+'BTCFull12.bf')
    bf13.bit, bf13.hash, bf13.bf = load_BF(dbdir+'BTCFull13.bf')
    bf14.bit, bf14.hash, bf14.bf = load_BF(dbdir+'BTCFull14.bf')
    bf15.bit, bf15.hash, bf15.bf = load_BF(dbdir+'BTCFull15.bf')
    bf16.bit, bf16.hash, bf16.bf = load_BF(dbdir+'BTCFull16.bf')
    bf17.bit, bf17.hash, bf17.bf = load_BF(dbdir+'BTCFull17.bf')
    catt = True # Включить если ALT
    bfeth0.bit, bfeth0.hash, bfeth0.bf = load_BF(dbdir+'ETHFull00.bf')
    bfeth1.bit, bfeth1.hash, bfeth1.bf = load_BF(dbdir+'ETHFull01.bf')
    bfeth2.bit, bfeth2.hash, bfeth2.bf = load_BF(dbdir+'ETHFull02.bf')
    bfeth3.bit, bfeth3.hash, bfeth3.bf = load_BF(dbdir+'ETHFull03.bf')
    ceth = True # Включить если ETH
    bfalt0.bit, bfalt0.hash, bfalt0.bf = load_BF(dbdir+'ALTFull00.bf')
    print(f'{green}Bloomfilter loaded...')
    print('-'*70,end='\n')
    line_co = 0
    step_print = 0
    co = 0
    l = []
    file = ''
    list_line = 100
    total_count = 0
    total_st = time()
    station = continue_point
    if station >= 0: 
        print(f'[I] Found file continuation, rewind to position...')
        t = True
    else: t = False
    pool = Pool(th, init_worker)
    with open(in_file, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            line = line.strip()
            line_co += 1
            if t:
                if line_co < station: 
                    continue
                else: 
                    total_count += station
                    line_co = 0
                    station = -1
                    t = False
            l.append([line, raw, cbtc, calt, ceth])
            if line_co == list_line:
                total_count += list_line
                line_co = 0
                st = time()
                results = pool.map(bw, l)
                for ii in range(len(results)):
                    for iii in range(len(results[ii])):
                        if results[ii][iii][0] == 'btc':
                            if cbtc:
                                if check_in_bloom(results[ii][iii][3].hex(), bf0.bit, bf0.hash, bf0.bf) or check_in_bloom(results[ii][iii][3].hex(), bf1.bit, bf1.hash, bf1.bf) or check_in_bloom(results[ii][iii][3].hex(), bf2.bit, bf2.hash, bf2.bf) or \
                                    check_in_bloom(results[ii][iii][3].hex(), bf3.bit, bf3.hash, bf3.bf) or check_in_bloom(results[ii][iii][3].hex(), bf4.bit, bf4.hash, bf4.bf) or check_in_bloom(results[ii][iii][3].hex(), bf5.bit, bf5.hash, bf5.bf) or \
                                    check_in_bloom(results[ii][iii][3].hex(), bf6.bit, bf6.hash, bf6.bf) or check_in_bloom(results[ii][iii][3].hex(), bf7.bit, bf7.hash, bf7.bf) or check_in_bloom(results[ii][iii][3].hex(), bf8.bit, bf8.hash, bf8.bf) or \
                                    check_in_bloom(results[ii][iii][3].hex(), bf9.bit, bf9.hash, bf9.bf) or check_in_bloom(results[ii][iii][3].hex(), bf10.bit, bf10.hash, bf10.bf) or check_in_bloom(results[ii][iii][3].hex(), bf11.bit, bf11.hash, bf11.bf) or \
                                    check_in_bloom(results[ii][iii][3].hex(), bf12.bit, bf12.hash, bf12.bf) or check_in_bloom(results[ii][iii][3].hex(), bf13.bit, bf13.hash, bf13.bf) or check_in_bloom(results[ii][iii][3].hex(), bf14.bit, bf14.hash, bf14.bf) or \
                                    check_in_bloom(results[ii][iii][3].hex(), bf15.bit, bf15.hash, bf15.bf) or check_in_bloom(results[ii][iii][3].hex(), bf16.bit, bf16.hash, bf16.bf) or check_in_bloom(results[ii][iii][3].hex(), bf17.bit, bf17.hash, bf17.bf):
                                    print(f'\nFOUND word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} Algo:{results[ii][iii][4]} ID:{id} desc:{desc} {in_file}\n')
                                    save_file('found',f'FOUND;word:{results[ii][iii][1]};PVK:{(results[ii][iii][2])};Algo:{results[ii][iii][4]};ID:{id};desc:{desc};{in_file}')
                                    if telegram_enable:
                                        send_telegram(f'FOUND word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} Algo:{results[ii][iii][4]} ID:{id} desc:{desc} {in_file}', telegram_channel_id, telegram_token)
                                co += 4
                            if calt:
                                if check_in_bloom(results[ii][iii][3].hex(), bfeth0.bit, bfeth0.hash, bfeth0.bf) or check_in_bloom(results[ii][iii][3].hex(), bfeth1.bit, bfeth1.hash, bfeth1.bf) or \
                                    check_in_bloom(results[ii][iii][3].hex(), bfeth2.bit, bfeth2.hash, bfeth2.bf)  or check_in_bloom(results[ii][iii][3].hex(), bfeth3.bit, bfeth3.hash, bfeth3.bf):
                                    print(f'\nFOUND word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} Algo:{results[ii][iii][4]} ID:{id} desc:{desc}\n')
                                    save_file('found',f'FOUND;word:{results[ii][iii][1]};PVK:{(results[ii][iii][2])};Algo:{results[ii][iii][4]};ID:{id};desc:{desc}')
                                    if telegram_enable:
                                        send_telegram(f'FOUND word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} Algo:{results[ii][iii][4]} ID:{id} desc:{desc}', telegram_channel_id, telegram_token)
                                co += 4
                        if results[ii][iii][0] == 'eth':
                            if ceth:
                                if check_in_bloom(results[ii][iii][3], bfalt0.bit, bfalt0.hash, bfalt0.bf):
                                    print(f'\nFOUND ETH:0x{results[ii][iii][3]} word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} Algo:{results[ii][iii][4]} ID:{id} desc:{desc}\n')
                                    save_file('found',f'FOUND;ETH:0x{results[ii][iii][3]};word:{results[ii][iii][1]};PVK:{(results[ii][iii][2])};Algo:{results[ii][iii][4]};ID:{id};desc:{desc}')
                                    if telegram_enable:
                                        send_telegram(f'FOUND ETH:0x{results[ii][iii][3]} word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} Algo:{results[ii][iii][4]} ID:{id} desc:{desc}', telegram_channel_id, telegram_token)
                                co += 1
                if step_print >= 20:
                    try:
                        speed_float, speed_hash = convert_int(co/(time()-st))
                    except:
                        speed_float, speed_hash = 0.0 , 'Key'
                    step_print +=1
                    if raw:
                        try:
                            ww = hex(results[ii][iii][1])
                        except:
                            ww = str(results[ii][iii][1])
                    else:
                        ww = str(results[ii][iii][1])
                    if minout:
                        print(' '*110,end='\r')
                        print(f'{yellow}Total time: {time()-total_st:.2f}, Total Hash: {total_count}, Speed:{speed_float} {speed_hash} ID:{id} word:{ww[:10]}... desc:{desc}',end='\r')
                    else:
                        print(' '*110,end='\r')
                        print(f'{yellow}Total time: {time()-total_st:.2f}, Total Hash: {total_count}, Speed:{speed_float} {speed_hash} ID:{id} word:{results[ii][iii][1]} desc:{desc}',end='\r')
                    step_print = 0
                else: step_print += 1
                if (int(time()-total_st)) >= save:
                    save_station_all_bloom(id,total_count)
                    save += save
                co = 0
                results = []
                l = []
    pool.terminate()
    pool.join()
    print ("\nEnd File.")
    save_station_all_bloom(id,-1)