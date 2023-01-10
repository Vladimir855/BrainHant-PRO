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
    parser = ArgumentParser(description='BrainHunt-SEQ')
    parser.add_argument ('-th', '--threading', action='store', type=int, help='threading', default='1')
    parser.add_argument ('-dbbtc', '--database1', action='store', type=str, help='File BF', default='')
    parser.add_argument ('-dbeth', '--database2', action='store', type=str, help='File BF ETH', default='')
    parser.add_argument ('-dbalt', '--database3', action='store', type=str, help='File BF ALT', default='')
    parser.add_argument ('-telegram', '--telegram', action='store_true', help='enable update')
    parser.add_argument ('-id', '--id', action='store', type=int, help='threading', default='0')
    parser.add_argument ('-desc', '--desc', action='store', type=str, help='description', default='local')
    parser.add_argument ('-save', '--save', action='store', type=int, help='save continue sec', default='-1')
    parser.add_argument ('-minout', '--minout', action='store_true', help='minimal out console')
    parser.add_argument ('-wordstop', '--wordstop', action='store', type=int, help='word stop', default=-1)
    parser.add_argument ('-word', '--word', action='store', type=str, help='word', default='')
    parser.add_argument ('-raw1', '--raw1', action='store_true', help='RAW1 divider')
    parser.add_argument ('-raw2', '--raw2', action='store_true', help='RAW2 Hasher')
    parser.add_argument ('-dbg', '--dbg', action='store_true', help='Debug')
    parser.add_argument ('-div', '--div', action='store', type=int, help='divider', default=-1)
    return parser.parse_args().threading, parser.parse_args().database1, parser.parse_args().database2, parser.parse_args().database3, \
        parser.parse_args().telegram, parser.parse_args().id, parser.parse_args().desc, parser.parse_args().save, \
        parser.parse_args().minout, parser.parse_args().wordstop, parser.parse_args().word, parser.parse_args().raw1, parser.parse_args().raw2, parser.parse_args().dbg, parser.parse_args().div

if __name__ == "__main__":
    freeze_support()
    print(clear_screen)
    local_version_brain_seq:float = 0.0
    telegram_token:str = ''
    telegram_channel_id:str = ''
    telegram_enable:bool = False
    continue_point_seq:str = ''
    th:int = 1
    balance_enable:bool = False
    bfbtc_dir:str = ''
    bfeth_dir:str = ''
    bfalt_dir:str = ''
    cbtc:bool = False
    ceth:bool = False
    calt:bool = False
    bfbtc:BF
    bfeth:BF
    bfalt:BF
    data_local:any
    desc:str = 'local'
    id:int = 0
    save = -1
    coin_blockchain:list = []
    coin_ice_num:list = []
    minout = False
    words_iter:int = 0
    word = ''
    rnd_word = False
    
    th, bfbtc_dir, bfeth_dir, bfalt_dir, telegram_enable, id, desc, save, minout, words_iter, word, raw1, raw2, dbg, div  = createParser()

    data_local = load_configure('setings.json')
    try:
        local_version_brain_seq:float = data_local['general']['version_brain_seq']
        telegram_token = data_local['telegram']['token']
        telegram_channel_id = data_local['telegram']['id']
        continue_point_seq = data_local['general'][f'continue_point_seq{id}@']
    except:
        print(f'[E] {red}Please Update file configuration!')
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
        telegram_enable = send_telegram(f'[I] Version BrainHunt SEQ: {local_version_brain_seq} ID:{id} desc:{desc} Start programm: {date_str()}', telegram_channel_id, telegram_token)
        if telegram_enable == False:
            balance_enable = False

    print('-'*70,end='\n')
    print(f'[I] Version BrainHunt: {cyan}v{local_version_brain_seq} SEQ')
    print(f'[I] Start proogramm: {cyan}{date_str()}')
    print(f'[I] Total kernel of CPU: {cyan}{cpu_count()}')
    print(f'[I] Used kernel: {cyan}{th}')
    print(f'[I] Description: {cyan}{desc}')
    print(f'[I] Used ID: {cyan}{id}')
    print(f'[I] iterate word: {cyan}{words_iter}')
    print(f'[I] Save continuation time: {cyan}{save}/sec')
    print(f'[I] Input DATA: {cyan}{word}')
    print(f'[I] Database Bloom Filter BTC: {cyan}{bfbtc_dir}')
    if ceth: print(f'[I] Database Bloom Filter ETH: {cyan}{bfeth_dir}')
    if calt: print(f'[I] Database Bloom Filter ALT: {cyan}{bfalt_dir}')
    if minout: print(f'[I] minimalistic OUT console: {cyan}Enable')
    else: print(f'[I] minimalistic OUT console: {red}Disabled')
    if rnd_word: 
        print(f'[I] Mode Random generate word: {cyan}Enable')
    else: print(f'[I] Mode Random generate word: {red}Disabled')
    if raw1: 
        print(f'[I] Mode RAW-1 divider: {cyan}Enable')
        print(f'[I] Divider: {cyan}{div}')
    else: print(f'[I] Mode RAW-1: {red}Disabled')
    if raw2: print(f'[I] Mode RAW-2 hasher: {cyan}Enable')
    else: print(f'[I] Mode RAW-2: {red}Disabled')    
    if balance_enable: print(f'[I] Check balance BTC: {cyan}Enable')
    else: print(f'[I] Check balance: {red}Disabled')
    if telegram_enable: print(f'[I] Send telegram: {cyan}Enable')
    else: print(f'[I] Send telegram: {red}Disabled')
    print('-'*70,end='\n')
    if cbtc: bfbtc = load_BF(bfbtc_dir)
    if ceth: bfeth = load_BF(bfeth_dir)
    if calt: bfalt = load_BF(bfalt_dir)
    print(f'{green}Bloomfilter loaded...')
    print('-'*70,end='\n')
    co = 0
    total_count = 0
    total_st = time()
    list_line = th*100
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
        l = gen_hash([word,list_line,cbtc,calt,ceth,raw1,raw2, dbg, div])
        st = time()
        results = pool.map(bw_seq, l)
        for ii in range(len(results)):
            for iii in range(len(results[ii])):
                if results[ii][iii][0] == 'btc':
                    if cbtc:
                        if results[ii][iii][3].hex() in bfbtc:
                            print(f'\nFOUND word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} ID:{id} desc:{desc}\n')
                            save_file('found',f'FOUND word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} ID:{id} desc:{desc}')
                            if telegram_enable:
                                send_telegram(f'FOUND word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} ID:{id}desc:{desc}', telegram_channel_id, telegram_token)
                        co += 4
                    if calt:
                        if results[ii][iii][3].hex() in bfalt:
                            print(f'\nFOUND word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} ID:{id} desc:{desc}\n')
                            save_file('found',f'FOUND word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} ID:{id} desc:{desc}')
                            if telegram_enable:
                                send_telegram(f'FOUND word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} ID:{id} desc:{desc}', telegram_channel_id, telegram_token)
                        co += 4
                if results[ii][iii][0] == 'eth':
                    if ceth:
                        if results[ii][iii][3] in bfeth:
                            print(f'\nFOUND ETH:0x{results[ii][iii][3]} word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} ID:{id} desc:{desc}\n')
                            save_file('found',f'FOUND ETH:0x{results[ii][iii][3]} word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} ID:{id} desc:{desc}')
                            if telegram_enable:
                                send_telegram(f'FOUND ETH:0x{results[ii][iii][3]} word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} ID:{id}desc:{desc}', telegram_channel_id, telegram_token)
                        co += 1
        if step_print >= 20:
            try:
                speed_float, speed_hash = convert_int(co/(time()-st))
            except:
                speed_float, speed_hash = 0.0 , 'Key'
            ww = str(results[ii][iii][1])
            print(' '*110,end='\r')
            if minout:
                print(f'{yellow}Total time: {time()-total_st:.2f}, Total Hash: {total_count}, Speed:{speed_float} {speed_hash} ID:{id} word:{ww[:10]}... desc:{desc}',end='\r')
            else:
                print(f'{yellow}Total time: {time()-total_st:.2f}, Total Hash: {total_count}, Speed:{speed_float} {speed_hash} ID:{id} word:{results[ii][iii][1]} desc:{desc}',end='\r')
            step_print = 0
        else: step_print += 1
        if (int(time()-total_st)) >= save and save != -1:
            save_station_seq(id,results[ii][iii][1])
            save += save
        co = 0
        word = results[ii][iii][1]
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
