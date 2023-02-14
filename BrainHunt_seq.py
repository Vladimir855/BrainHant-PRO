# #!/usr/bin/python3
# encoding=utf-8
# -*- coding: utf-8 -*-
"""
@author: NonameHUNT
@GitHub: https://github.com/Noname400
@telegram: https://t.me/NonameHunt
"""
version = 'BrainHunt SEQ 3.17/14.02.23'
from lib.function import *

def init_worker():
    signal(SIGINT, SIG_IGN)
    
def createParser():
    parser = ArgumentParser(description='BrainHunt SEQ')
    parser.add_argument ('-th', '--threading', action='store', type=int, help='threading', default='1')
    parser.add_argument ('-dbdir', '--database_dir', action='store', type=str, help='DIR BF', default='')
    parser.add_argument ('-rescandir', '--database_rescan', action='store', type=str, help='DIR rescan', default='')
    parser.add_argument ('-telegram', '--telegram', action='store_true', help='enable telegram')
    parser.add_argument ('-id', '--id', action='store', type=int, help='id from save', default='0')
    parser.add_argument ('-desc', '--desc', action='store', type=str, help='description', default='local')
    parser.add_argument ('-save', '--save', action='store', type=int, help='save continue sec', default='-1')
    parser.add_argument ('-minout', '--minout', action='store_true', help='minimal out console')
    parser.add_argument ('-wordstop', '--wordstop', action='store', type=int, help='word stop', default=-1)
    parser.add_argument ('-word', '--word', action='store', type=str, help='word', default='')
    parser.add_argument ('-raw1', '--raw1', action='store_true', help='RAW1 divider')
    parser.add_argument ('-raw2', '--raw2', action='store_true', help='RAW2 Hasher')
    parser.add_argument ('-dbg', '--dbg', action='store_true', help='Debug')
    parser.add_argument ('-div', '--div', action='store', type=int, help='divider', default=-1)
    parser.add_argument ('-incdec', '--incdec', action='store', type=int, help='IncDec', default='1')

    return parser.parse_args().threading, parser.parse_args().database_dir, parser.parse_args().database_rescan,\
        parser.parse_args().telegram, parser.parse_args().id, parser.parse_args().desc, parser.parse_args().save, \
        parser.parse_args().minout, parser.parse_args().wordstop, parser.parse_args().word, parser.parse_args().raw1, parser.parse_args().raw2, parser.parse_args().dbg, parser.parse_args().div, parser.parse_args().incdec

if __name__ == "__main__":
    freeze_support()
    cls()
    telegram_token:str = ''
    telegram_channel_id:str = ''
    telegram_enable:bool = False
    continue_point_seq:str = ''
    th:int = 1
    bf_dir:str = ''
    crescan:bool = False
    rescan_dir:str = ''
    list_btc:list = []
    list_eth:list = []
    list_alt:list = []
    cbtc:bool = False
    ceth:bool = False
    calt:bool = False
    data_local:any
    desc:str = 'local'
    id:int = 0
    save = -1
    minout = False
    words_iter:int = 0
    word = ''
    rnd_word = False
    incdec:int = 1
    th, bf_dir, rescan_dir, telegram_enable, id, desc, save, minout, words_iter, word, raw1, raw2, dbg, div, incdec  = createParser()

    data_local = load_configure('setings.json')
    try:
        telegram_token = data_local['telegram']['token']
        telegram_channel_id = data_local['telegram']['id']
        continue_point_seq = data_local['general'][f'continue_point_seq{id}@']
    except:
        print(f'[E] {color.red}Please Update file configuration!')
        exit(1)

    if raw1 == raw2: raw2=False
    if raw1:
        if div == -1: div = random.randrange(2,2**32)
        if word == '': word = random_key()
    if raw2:
        if word == '': word = random_key()
        
    if word == '?':
        word = gen_word()
        raw1 = False
        raw2 = False
        rnd_word = True

    print('-'*70,end='\n')
    print(f'{color.green}Thank you very much: @iceland2k14 for his libraries!')

    if th < 1:
        print('[E] The number of processes must be greater than 0')
        th = 1

    if telegram_enable:
        telegram_enable = send_telegram(f'[I] Version: {version} ID:{id} desc:{desc} Start programm: {date_str()}', telegram_channel_id, telegram_token)

    if rescan_dir != '':
        crescan = True

    print('-'*70,end='\n')
    print(f'[I] Version: {color.cyan}{version}')
    print(f'[I] Version LIB: {color.cyan}{version_lib}')
    print(f'[I] Start proogramm: {color.cyan}{date_str()}')
    print(f'[I] Total kernel of CPU: {color.cyan}{cpu_count()}')
    print(f'[I] Used kernel: {color.cyan}{th}')
    print(f'[I] Description: {color.cyan}{desc}')
    print(f'[I] Used ID: {color.cyan}{id}')
    print(f'[I] iterate word: {color.cyan}{words_iter}')
    print(f'[I] Save continuation time: {color.cyan}{save}/sec')
    print(f'[I] Input DATA: {color.cyan}{word}')
    print(f'[I] Directory Bloom Filter: {color.cyan}{bf_dir}')
    if crescan: print(f'[I] Directory Rescan: {color.cyan}{rescan_dir}')
    else: print(f'[I] Rescan: {color.red}Disabled')
    if incdec > 1:
        print(f'[I] IncDEc: {color.cyan}Enable')
        print(f'[I] IncDEc: {color.cyan}{incdec}')
    if minout: print(f'[I] minimalistic OUT console: {color.cyan}Enable')
    else: print(f'[I] minimalistic OUT console: {color.red}Disabled')
    if rnd_word: 
        print(f'[I] Mode Random generate word: {color.cyan}Enable')
    else: print(f'[I] Mode Random generate word: {color.red}Disabled')
    if raw1: 
        print(f'[I] Mode RAW-1 divider: {color.cyan}Enable')
        print(f'[I] Divider: {color.cyan}{div}')
    else: print(f'[I] Mode RAW-1: {color.red}Disabled')
    if raw2: print(f'[I] Mode RAW-2 hasher: {color.cyan}Enable')
    else: print(f'[I] Mode RAW-2: {color.red}Disabled')    
    if telegram_enable: print(f'[I] Send telegram: {color.cyan}Enable')
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
    
    co = 0
    total_count = 0
    total_st = time()
    # if raw1 or raw2:
    #     if incdec > 1:
    #         list_line = int(10000/10)
    #     else: list_line = 10000
    # else:
    #     if incdec > 1:
    #         list_line = int(5000/10)
    #     else: list_line = 5000
    list_line = 100 * th
    step_print = 0
    l = []
    
    if rnd_word:
        pass
    elif raw1 and save == -1:
        pass
    elif raw2 and save == -1:
        pass
    else:
        if continue_point_seq != "": 
            print(f'[I] Found file continuation. Start Hash {continue_point_seq}')
            word = continue_point_seq
    pool = Pool(th, init_worker)
    while True:
        st = time()
        total_count += list_line
        l = gen_hash([word, list_line, cbtc, calt, ceth, raw1, raw2, dbg, div, incdec])
        st = time()
        results = pool.map(bw_seq, l)

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
                                    print(f'\n{color.green}[F True] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}\n')
                                    save_file('found',f'[F True] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}')
                                    if telegram_enable:
                                        send_telegram(f'[F True] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}', telegram_channel_id, telegram_token)
                                else:
                                    print(f'\n{color.green}[F False] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}\n')
                                    save_file('found-false',f'[F False] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}')
                            else:
                                print(f'\n{color.green}[F] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}\n')
                                save_file('found',f'[F] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}')
                                if telegram_enable:
                                    send_telegram(f'[F] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}', telegram_channel_id, telegram_token) 
                        co += 1
                if res[0] == 'alt' and calt:    
                    for check in list_alt:
                        if BF.check(res[3]):
                            if crescan:
                                rez = rescan(res[3], 'alt', rescan_dir)
                                if rez == None: crescan = False
                                elif rez == True:
                                    print(f'\n{color.green}[F True] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}\n')
                                    save_file('found',f'[F True] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}')
                                    if telegram_enable:
                                        send_telegram(f'[F True] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}', telegram_channel_id, telegram_token)
                                else:
                                    print(f'\n{color.green}[F False] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}\n')
                                    save_file('found-false',f'[F False] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}')
                            else:
                                print(f'\n{color.green}[F] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}\n')
                                save_file('found',f'[F] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}')
                                if telegram_enable:
                                    send_telegram(f'[F] FOUND {date_str()} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}', telegram_channel_id, telegram_token) 
                        co += 1
                            
                if res[0] == 'eth' and ceth:
                    for check in list_eth:
                        if BF.check(res[3]):
                            if crescan:
                                rez = rescan(res[3], 'btc', rescan_dir)
                                if rez == None: crescan = False
                                elif rez == True:
                                    print(f'\n{color.green}[F True] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}\n')
                                    save_file('found',f'[F True] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}')
                                    if telegram_enable:
                                        send_telegram(f'[F True] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}', telegram_channel_id, telegram_token)
                                else:
                                    print(f'\n{color.green}[F false] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}\n')
                                    save_file('found-false',f'[F false] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}')
                            else:
                                print(f'\n{color.green}[F] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}\n')
                                save_file('found',f'[F] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}')
                                if telegram_enable:
                                    send_telegram(f'[F] FOUND {date_str()} ETH:0x{res[3]} word:{res[1]} PVK:{(res[2])} Algo:{res[4]} ID:{id} desc:{desc}', telegram_channel_id, telegram_token)
                        co += 1

        try:
            speed_float, speed_hash = convert_int(co/(time()-st))
        except:
            speed_float, speed_hash = convert_int(co/1)
        ww = str(res[1])
        print(' '*110,end='\r')
        if minout:
            print(f'{color.yellow}Total time: {time()-total_st:.2f}, Total Hash: {total_count}, Speed:{speed_float} {speed_hash} ID:{id} word:{ww[:10]}... desc:{desc}',end='\r')
        else:
            print(f'{color.yellow}Total time: {time()-total_st:.2f}, Total Hash: {total_count}, Speed:{speed_float} {speed_hash} ID:{id} word:{res[1]} desc:{desc}',end='\r')
        step_print = 0
        if (int(time()-total_st)) >= save and save != -1:
            save_station_seq(id,res[1])
            save += save
        co = 0
        word = res[1]
        results = []
        l = []
        if words_iter < 0: pass
        else:
            if rnd_word:
                if words_iter <= total_count:
                    total_count = 0
                    word = gen_word()
                    print (f"\nNEW word:{word} generate.")
            elif raw1 and save == -1:
                if words_iter <= total_count:
                    total_count = 0
                    word = random_key()
                    div = random.randrange(2,2**32)
                    print (f"\nNEW PVK:{word} new divider: {div} generate.")
            elif raw2 and save == -1:
                if words_iter <= total_count:
                    total_count = 0
                    word = random_key()
                    print (f"\nNEW PVK:{word} generate.")
            else:
                if words_iter <= total_count:
                    print (f"\nEnd hash generate.")
                    save_station_seq(id,'')
                    exit(0)
