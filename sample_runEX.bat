rem mp64 ?d?d?d?d?d?d | python BrainHunt_EX.py -th 3 -id 0 -dbbtc BF/btc.bf -dbalt BF/alt.bf -dbeth BF/eth.bf -telegram -desc home -save 30 -minout
rem python genhash.py | python BrainHunt_EX.py -th 3 -id 0 -dbbtc BF/btc.bf -dbalt BF/alt.bf -dbeth BF/eth.bf -telegram -desc home -save 30 -minout
python genhash.py | python BrainHunt_EX.py -th 2 -id 0 -dbbtc btc.bin -dbalt btc.bin -dbeth btc.bin -telegram -desc home -save 30 -minout
pause