rem mp64 ?d?d?d?d?d?d | python BrainHunt_EX.py -th 1 -id 0 -dbbtc btc.bin -dbalt btc.bin -dbeth btc.bin -raw -telegram -desc home -save 300 -minout
python genhash.py | python BrainHunt_EX.py -th 1 -id 0 -dbdir D:\GitHub\BrainHant-PRO\BF -telegram -desc home -save 300 -minout
rem python genhash.py | python BrainHunt_EX.py -th 1 -id 0 -dbbtc btc.bin -dbalt btc.bin -dbeth btc.bin -telegram -desc home -save 300 -minout
pause