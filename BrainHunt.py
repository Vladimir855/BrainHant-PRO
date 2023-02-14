# #!/usr/bin/python3
# encoding=utf-8
# -*- coding: utf-8 -*-
"""
@author: NonameHUNT
@GitHub: https://github.com/Noname400
@telegram: https://t.me/NonameHunt
"""
version = 'BrainHunt Classic 3.27/14.02.23'
from lib.function import *

def init_worker():
    signal(SIGINT, SIG_IGN)

def createParser():
    parser = ArgumentParser(description='BrainHunt')
    parser.add_argument ('-th', '--threading', action='store', type=int, help='threading', default='1')
    parser.add_argument ('-dbdir', '--database_dir', action='store', type=str, help='DIR BF', default='')
    parser.add_argument ('-rescandir', '--database_rescan', action='store', type=str, help='DIR rescan', default='')
    parser.add_argument ('-in', '--infile', action='store', type=str, help='infile', default='')
    parser.add_argument ('-telegram', '--telegram', action='store_true', help='enable telegram')
    parser.add_argument ('-id', '--id', action='store', type=int, help='id for save', default='0')
    parser.add_argument ('-desc', '--desc', action='store', type=str, help='description', default='local')
    parser.add_argument ('-save', '--save', action='store', type=int, help='save continue sec', default='60')
    parser.add_argument ('-minout', '--minout', action='store_true', help='minimal out console')
    parser.add_argument ('-raw', '--raw', action='store_true', help='input raw')
    parser.add_argument ('-incdec', '--incdec', action='store', type=int, help='IncDec', default='1')

    return parser.parse_args().threading, parser.parse_args().database_dir, parser.parse_args().infile, parser.parse_args().telegram, parser.parse_args().id, parser.parse_args().desc, \
        parser.parse_args().save, parser.parse_args().minout, parser.parse_args().raw, parser.parse_args().incdec, parser.parse_args().database_dir
        
if __name__ == "__main__":
    freeze_support()
    cls()
    telegram_token:str = ''
    telegram_channel_id:str = ''
    telegram_enable:bool = False
    continue_point:int = -1
    th:int = 1
    in_file = ''
    bf_dir:str = ''
    crescan:bool = False
    rescan_dir:str = ''
    list_btc = []
    list_eth = []
    list_alt = []
    cbtc:bool = False
    ceth:bool = False
    calt:bool = False
    data_local:any
    desc:str = 'local'
    id:int = 0
    save = 30
    minout = False
    raw:bool = False
    incdec:int = 1
    th, bf_dir, in_file, telegram_enable, id, desc, save, minout, raw, incdec, rescan_dir  = createParser()

    data_local = load_configure('setings.json')
    try:
        telegram_token = data_local['telegram']['token']
        telegram_channel_id = data_local['telegram']['id']
        continue_point = data_local['general'][f'continue_point{id}@']
    except:
        print(f'[E] {color.red}Please Update file configuration!')
        exit(1)
    print('-'*70,end='\n')
    print(f'{color.green}Thank you very much: @iceland2k14 for his libraries!')

    if th < 1:
        print('[E] The number of processes must be greater than 0')
        th = 1

    if telegram_enable:
        telegram_enable = send_telegram(f'[I] Version:{version} ID:{id} desc:{desc} Start programm: {date_str()}', telegram_channel_id, telegram_token)

    if rescan_dir != '':
        crescan = True

    print('-'*70,end='\n')
    print(f'[I] Version: {color.cyan}{version}')
    print(f'[I] Version LIB: {color.cyan}{version_LIB}')
    print(f'[I] Start proogramm: {color.cyan}{date_str()}')
    print(f'[I] Total kernel of CPU: {color.cyan}{cpu_count()}')
    print(f'[I] Used kernel: {color.cyan}{th}')
    print(f'[I] Used file: {color.cyan}{in_file}')
    print(f'[I] Used ID: {color.cyan}{id}')
    print(f'[I] Directory Bloom Filter: {color.cyan}{bf_dir}')
    if crescan: print(f'[I] Directory Rescan: {color.cyan}{rescan_dir}')
    else: print(f'[I] Rescan: {color.red}Disabled')
    if incdec > 1:
        print(f'[I] IncDEc: {color.cyan}Enable')
        print(f'[I] IncDEc: {color.cyan}{incdec}')
    if minout: print(f'[I] minimalistic OUT console: {color.cyan}Enable')
    else: print(f'[I] minimalistic OUT console: {color.red}Disabled')
    if raw: print(f'[I] Input Raw private key: {color.green}Enable')
    else: print(f'[I] Input Raw private key: {color.red}Disabled')
    if telegram_enable: print(f'[I] Send telegram: {color.green}Enable')
    else: print(f'[I] Send telegram: {color.red}Disabled')

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
    line_co = 0
    step_print = 0
    co = 0
    l = []
    file = ''
    # if raw:
    #     if incdec > 1:
    #         list_line = int(10000/10)
    #     else: list_line = 10000
    # else:
    #     if incdec > 1:
    #         list_line = int(5000/10)
    #     else: list_line = 5000
    list_line = 100 * th
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
            l.append([line,raw,cbtc,calt,ceth,incdec])
            if line_co == list_line:
                total_count += list_line
                line_co = 0
                st = time()
                results = pool.map(bw, l)
                for map_res in results:
                    for res in map_res:
                        if type(res[3]) != bytes:
                            print('NOT BYTES')
                        if res[0] == 'btc' and cbtc:
                            for BF in list_btc:
                                if BF.check(res[3]):
                                    if crescan:
                                        rez = rescan(res[3], 'btc', rescan_dir)
                                        if rez == None: crescan = False
                                        elif rez == True:
                                            print(f'\n{color.green}[F True] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}\n')
                                            save_file('found',f'[F True] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}')
                                            if telegram_enable:
                                                send_telegram(f'[F True] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}', telegram_channel_id, telegram_token)
                                        else:
                                            print(f'\n{color.green}[F False] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}\n')
                                            save_file('found-false',f'[F False] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}')
                                    else:
                                        print(f'\n{color.green}[F] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}\n')
                                        save_file('found',f'[F] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}')
                                        if telegram_enable:
                                            send_telegram(f'[F] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}', telegram_channel_id, telegram_token) 
                                co += 1
                        if res[0] == 'alt' and calt:    
                            for check in list_alt:
                                if BF.check(res[3]):
                                    if crescan:
                                        rez = rescan(res[3], 'alt', rescan_dir)
                                        if rez == None: crescan = False
                                        elif rez == True:
                                            print(f'\n{color.green}[F True] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}\n')
                                            save_file('found',f'[F True] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}')
                                            if telegram_enable:
                                                send_telegram(f'[F True] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}', telegram_channel_id, telegram_token)
                                        else:
                                            print(f'\n{color.green}[F False] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}\n')
                                            save_file('found-false',f'[F False] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}')
                                    else:
                                        print(f'\n{color.green}[F] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}\n')
                                        save_file('found',f'[F] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}')
                                        if telegram_enable:
                                            send_telegram(f'[F] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}', telegram_channel_id, telegram_token) 
                                co += 1
                                    
                        if res[0] == 'eth' and ceth:
                            for check in list_eth:
                                if BF.check(res[3]):
                                    if crescan:
                                        rez = rescan(res[3], 'eth', rescan_dir)
                                        if rez == None: crescan = False
                                        elif rez == True:
                                            print(f'\n{color.green}[F True] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}\n')
                                            save_file('found',f'[F True] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}')
                                            if telegram_enable:
                                                send_telegram(f'[F True] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}', telegram_channel_id, telegram_token)
                                        else:
                                            print(f'\n{color.green}[F false] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}\n')
                                            save_file('found-false',f'[F false] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}')
                                    else:
                                        print(f'\n{color.green}[F] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}\n')
                                        save_file('found',f'[F] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}')
                                        if telegram_enable:
                                            send_telegram(f'[F] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}', telegram_channel_id, telegram_token)
                                co += 1
                try:
                    speed_float, speed_hash = convert_int(co/(time()-st))
                except:
                    speed_float, speed_hash = convert_int(co/1)
                step_print +=1
                if step_print > 20:
                    if raw:
                        try:
                            ww = hex(res[1])
                        except:
                            ww = str(res[1])
                    else:
                        ww = str(res[1])
                    if minout:
                        print(' '*110,end='\r')
                        print(f'{color.yellow}Total time: {time()-total_st:.2f}, Total Hash: {total_count}, Speed:{speed_float} {speed_hash} ID:{id} word:{ww[:10]}... desc:{desc}',end='\r')
                    else:
                        print(' '*110,end='\r')
                        print(f'{color.yellow}Total time: {time()-total_st:.2f}, Total Hash: {total_count}, Speed:{speed_float} {speed_hash} ID:{id} word:{res[1]} desc:{desc}',end='\r')
                    step_print = 0
                if (int(time()-total_st)) >= save:
                    save_station(id,total_count)
                    save += save
                co = 0
                results = []
                l = []
        else:
            results = pool.map(bw, l)
            for map_res in results:
                for res in map_res:
                    if type(res[3]) != bytes:
                        print('NOT BYTES')
                        if res[0] == 'btc' and cbtc:
                            for BF in list_btc:
                                if BF.check(res[3]):
                                    if crescan:
                                        rez = rescan(res[3], 'btc', rescan_dir)
                                        if rez == None: crescan = False
                                        elif rez == True:
                                            print(f'\n{color.green}[F True] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}\n')
                                            save_file('found',f'[F True] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}')
                                            if telegram_enable:
                                                send_telegram(f'[F True] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}', telegram_channel_id, telegram_token)
                                        else:
                                            print(f'\n{color.green}[F False] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}\n')
                                            save_file('found-false',f'[F False] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}')
                                    else:
                                        print(f'\n{color.green}[F] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}\n')
                                        save_file('found',f'[F] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}')
                                        if telegram_enable:
                                            send_telegram(f'[F] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}', telegram_channel_id, telegram_token) 

                        if res[0] == 'alt' and calt:    
                            for check in list_alt:
                                if BF.check(res[3]):
                                    if crescan:
                                        rez = rescan(res[3], 'alt', rescan_dir)
                                        if rez == None: crescan = False
                                        elif rez == True:
                                            print(f'\n{color.green}[F True] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}\n')
                                            save_file('found',f'[F True] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}')
                                            if telegram_enable:
                                                send_telegram(f'[F True] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}', telegram_channel_id, telegram_token)
                                        else:
                                            print(f'\n{color.green}[F False] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}\n')
                                            save_file('found-false',f'[F False] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}')
                                    else:
                                        print(f'\n{color.green}[F] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}\n')
                                        save_file('found',f'[F] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}')
                                        if telegram_enable:
                                            send_telegram(f'[F] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}', telegram_channel_id, telegram_token) 
                                   
                        if res[0] == 'eth' and ceth:
                            for check in list_eth:
                                if BF.check(res[3]):
                                    if crescan:
                                        rez = rescan(res[3], 'eth', rescan_dir)
                                        if rez == None: crescan = False
                                        elif rez == True:
                                            print(f'\n{color.green}[F True] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}\n')
                                            save_file('found',f'[F True] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}')
                                            if telegram_enable:
                                                send_telegram(f'[F True] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}', telegram_channel_id, telegram_token)
                                        else:
                                            print(f'\n{color.green}[F false] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}\n')
                                            save_file('found-false',f'[F false] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}')
                                    else:
                                        print(f'\n{color.green}[F] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}\n')
                                        save_file('found',f'[F] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}')
                                        if telegram_enable:
                                            send_telegram(f'[F] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc} {in_file}', telegram_channel_id, telegram_token)
    pool.terminate()
    pool.join()
    print ("\nEnd File.")
    save_station(id,-1)