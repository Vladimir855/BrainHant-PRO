# #!/usr/bin/python3
# encoding=utf-8
# -*- coding: utf-8 -*-
"""
@author: NonameHUNT
@GitHub: https://github.com/Noname400
@telegram: https://t.me/NonameHunt
"""
version = 'BrainHunt SEQ 3.05/12.01.23'
from lib.function import *

def init_worker():
    signal(SIGINT, SIG_IGN)
    
def createParser():
    parser = ArgumentParser(description='BrainHunt-SEQ')
    parser.add_argument ('-th', '--threading', action='store', type=int, help='threading', default='1')
    parser.add_argument ('-dbdir', '--database_dir', action='store', type=str, help='File BF', default='')
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
    return parser.parse_args().threading, parser.parse_args().database_dir, \
        parser.parse_args().telegram, parser.parse_args().id, parser.parse_args().desc, parser.parse_args().save, \
        parser.parse_args().minout, parser.parse_args().wordstop, parser.parse_args().word, parser.parse_args().raw1, parser.parse_args().raw2, parser.parse_args().dbg, parser.parse_args().div

if __name__ == "__main__":
    freeze_support()
    print(color.clear_screen)
    telegram_token:str = ''
    telegram_channel_id:str = ''
    telegram_enable:bool = False
    continue_point_seq:str = ''
    th:int = 1
    bf_dir:str = ''
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
    
    th, bf_dir, telegram_enable, id, desc, save, minout, words_iter, word, raw1, raw2, dbg, div  = createParser()

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

    print('-'*70,end='\n')
    print(f'[I] Version: {color.cyan}{version}')
    print(f'[I] Start proogramm: {color.cyan}{date_str()}')
    print(f'[I] Total kernel of CPU: {color.cyan}{cpu_count()}')
    print(f'[I] Used kernel: {color.cyan}{th}')
    print(f'[I] Description: {color.cyan}{desc}')
    print(f'[I] Used ID: {color.cyan}{id}')
    print(f'[I] iterate word: {color.cyan}{words_iter}')
    print(f'[I] Save continuation time: {color.cyan}{save}/sec')
    print(f'[I] Input DATA: {color.cyan}{word}')
    print(f'[I] Directory Bloom Filter: {color.cyan}{bf_dir}')
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
    currentDirectory = pathlib.Path(bf_dir)
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
    print(f'[I] {color.green}Bloomfilter loaded...')
    print('-'*70,end='\n')
    co = 0
    total_count = 0
    total_st = time()
    if raw1 or raw2:
        list_line = 10000
    else:
        list_line = 5000
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
                        for check in list_btc:
                            if check_in_bloom(results[ii][iii][3].hex(), check.bit, check.hash, check.bf):
                                print(f'\nFOUND word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} ID:{id} desc:{desc}\n')
                                save_file('found',f'FOUND word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} ID:{id} desc:{desc}')
                                if telegram_enable:
                                    send_telegram(f'FOUND word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} ID:{id}desc:{desc}', telegram_channel_id, telegram_token)
                        co += 3
                    if calt:
                        for check in list_alt:
                            if check_in_bloom(results[ii][iii][3].hex(), check.bit, check.hash, check.bf):
                                print(f'\nFOUND word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} ID:{id} desc:{desc}\n')
                                save_file('found',f'FOUND word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} ID:{id} desc:{desc}')
                                if telegram_enable:
                                    send_telegram(f'FOUND word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} ID:{id} desc:{desc}', telegram_channel_id, telegram_token)
                        co += 3
                if results[ii][iii][0] == 'eth':
                    if ceth:
                        for check in list_eth:
                            if check_in_bloom(results[ii][iii][3], check.bit, check.hash, check.bf):
                                print(f'\nFOUND ETH:0x{results[ii][iii][3]} word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} ID:{id} desc:{desc}\n')
                                save_file('found',f'FOUND ETH:0x{results[ii][iii][3]} word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} ID:{id} desc:{desc}')
                                if telegram_enable:
                                    send_telegram(f'FOUND ETH:0x{results[ii][iii][3]} word:{results[ii][iii][1]} PVK:{(results[ii][iii][2])} ID:{id}desc:{desc}', telegram_channel_id, telegram_token)
                        co += 1
        try:
            speed_float, speed_hash = convert_int(co/(time()-st))
        except:
            speed_float, speed_hash = 0.0 , 'Key'
        ww = str(results[ii][iii][1])
        print(' '*110,end='\r')
        if minout:
            print(f'{color.yellow}Total time: {time()-total_st:.2f}, Total Hash: {total_count}, Speed:{speed_float} {speed_hash} ID:{id} word:{ww[:10]}... desc:{desc}',end='\r')
        else:
            print(f'{color.yellow}Total time: {time()-total_st:.2f}, Total Hash: {total_count}, Speed:{speed_float} {speed_hash} ID:{id} word:{results[ii][iii][1]} desc:{desc}',end='\r')
        step_print = 0
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
