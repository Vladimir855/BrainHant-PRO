# #!/usr/bin/python3
# encoding=utf-8
# -*- coding: utf-8 -*-
"""
@author: NonameHUNT
@GitHub: https://github.com/Noname400
@telegram: https://t.me/NonameHunt
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
    parser = ArgumentParser(description='BrainHunt')
    parser.add_argument ('-th', '--threading', action='store', type=int, help='threading', default='1')
    parser.add_argument ('-dbbtc', '--database1', action='store', type=str, help='File BF', default='')
    parser.add_argument ('-dbeth', '--database2', action='store', type=str, help='File BF ETH', default='')
    parser.add_argument ('-dbalt', '--database3', action='store', type=str, help='File BF ALT', default='')
    parser.add_argument ('-in', '--infile', action='store', type=str, help='infile', default='')
    parser.add_argument ('-telegram', '--telegram', action='store_true', help='enable update')
    parser.add_argument ('-id', '--id', action='store', type=int, help='threading', default='0')
    parser.add_argument ('-desc', '--desc', action='store', type=str, help='description', default='local')
    parser.add_argument ('-save', '--save', action='store', type=int, help='save continue sec', default='60')
    parser.add_argument ('-minout', '--minout', action='store_true', help='minimal out console')
    parser.add_argument ('-raw', '--raw', action='store_true', help='input raw')
    return parser.parse_args().threading, parser.parse_args().database1, parser.parse_args().database2, parser.parse_args().database3, \
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
    bfbtc_dir:str = ''
    bfeth_dir:str = ''
    bfalt_dir:str = ''
    cbtc:bool = False
    ceth:bool = False
    calt:bool = False
    bfbtc = BF
    bfeth = BF
    bfalt = BF
    data_local:any
    desc:str = 'local'
    id:int = 0
    save = 30
    minout = False
    raw:bool = False
    th, bfbtc_dir, bfeth_dir, bfalt_dir, in_file, telegram_enable, id, desc, save, minout, raw  = createParser()

    data_local = load_configure('setings.json')
    try:
        local_version_brain:float = data_local['general']['version_brain']
        telegram_token = data_local['telegram']['token']
        telegram_channel_id = data_local['telegram']['id']
        continue_point = data_local['general'][f'continue_point{id}@']
    except:
        print(f'[E] {red}Please Update file configuration!')
        exit(1)
    print('-'*70,end='\n')
    print(f'{green}Thank you very much: @iceland2k14 for his libraries!')

    if bfbtc_dir != '':
        cbtc = True
    if bfeth_dir != '':
        ceth = True
    if bfalt_dir != '':
        calt = True

    if th < 1:
        print('[E] The number of processes must be greater than 0')
        th = 1

    if telegram_enable:
        telegram_enable = send_telegram(f'[I] Version BrainHunt EX: {local_version_brain} ID:{id} desc:{desc} Start programm: {date_str()}', telegram_channel_id, telegram_token)

    print('-'*70,end='\n')
    print(f'[I] Version BrainHunt: {cyan}v{local_version_brain} Classic')
    print(f'[I] Start proogramm: {cyan}{date_str()}')
    print(f'[I] Total kernel of CPU: {cyan}{cpu_count()}')
    print(f'[I] Used kernel: {cyan}{th}')
    print(f'[I] Used file: {cyan}{in_file}')
    print(f'[I] Used ID: {cyan}{id}')
    print(f'[I] Database Bloom Filter BTC: {cyan}{bfbtc_dir}')
    if ceth: print(f'[I] Database Bloom Filter ETH: {cyan}{bfeth_dir}')
    if calt: print(f'[I] Database Bloom Filter ALT: {cyan}{bfalt_dir}')
    if minout: print(f'[I] minimalistic OUT console: {cyan}Enable')
    else: print(f'[I] minimalistic OUT console: {red}Disabled')
    if raw: print(f'[I] Input Raw private key: {green}Enable')
    else: print(f'[I] Input Raw private key: {red}Disabled')
    if telegram_enable: print(f'[I] Send telegram: {green}Enable')
    else: print(f'[I] Send telegram: {red}Disabled')
    print('-'*70,end='\n')
    if cbtc: bfbtc.bit, bfbtc.hash, bfbtc.bf = load_BF(bfbtc_dir)
    if ceth: bfeth.bit, bfeth.hash, bfeth.bf = load_BF(bfeth_dir)
    if calt: bfalt.bit, bfalt.hash, bfalt.bf = load_BF(bfalt_dir)
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
            l.append([line,raw,cbtc,calt,ceth])
            if line_co == list_line:
                total_count += list_line
                line_co = 0
                st = time()
                results = pool.map(bw, l)
                for ii in range(len(results)):
                    for iii in range(len(results[ii])):
                        if results[ii][iii][0] == 'btc':
                            if cbtc:
                                if check_in_bloom(results[ii][iii][3].hex(), bfbtc.bit, bfbtc.hash, bfbtc.bf):# or results[ii][iii][3].hex() == 'bf1c61ac19576d71d4623b185f3bae2a3d4df6bc':
                                    print(f'\nFOUND word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} Algo:{results[ii][iii][4]} ID:{id} desc:{desc} {in_file}\n')
                                    save_file('found',f'FOUND word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} Algo:{results[ii][iii][4]} ID:{id} desc:{desc} {in_file}')
                                    if telegram_enable:
                                        send_telegram(f'FOUND word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} Algo:{results[ii][iii][4]} ID:{id} desc:{desc} {in_file}', telegram_channel_id, telegram_token)
                                co += 4
                            if calt:
                                if check_in_bloom(results[ii][iii][3].hex(), bfalt.bit, bfalt.hash, bfalt.bf):
                                    print(f'\nFOUND word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} Algo:{results[ii][iii][4]} ID:{id} desc:{desc} {in_file}\n')
                                    save_file('found',f'FOUND word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} Algo:{results[ii][iii][4]} ID:{id} desc:{desc} {in_file}')
                                    if telegram_enable:
                                        send_telegram(f'FOUND word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} Algo:{results[ii][iii][4]} ID:{id} desc:{desc} {in_file}', telegram_channel_id, telegram_token)
                                co += 4
                        if results[ii][iii][0] == 'eth':
                            if ceth:
                                if check_in_bloom(results[ii][iii][3], bfeth.bit, bfeth.hash, bfeth.bf):
                                    print(f'\nFOUND ETH:0x{results[ii][iii][3]} word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} Algo:{results[ii][iii][4]} ID:{id} desc:{desc} {in_file}\n')
                                    save_file('found',f'FOUND ETH:0x{results[ii][iii][3]} word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} Algo:{results[ii][iii][4]} ID:{id} desc:{desc} {in_file}')
                                    if telegram_enable:
                                        send_telegram(f'FOUND ETH:0x{results[ii][iii][3]} word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} Algo:{results[ii][iii][4]} ID:{id} desc:{desc} {in_file}', telegram_channel_id, telegram_token)
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
                    save_station(id,total_count)
                    save += save
                co = 0
                results = []
                l = []
    pool.terminate()
    pool.join()
    print ("\nEnd File.")
    save_station(id,-1)