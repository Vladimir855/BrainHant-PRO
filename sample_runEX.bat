rem mp64 ?d?d?d?d?d?d | python BrainHunt_EX.py -th 1 -id 0 -dbdir D:\GitHub\BrainHant-PRO\BF -desc home -save 300 -minout
rem mp64 ?d?d?d?d?d?d | python BrainHunt_EX.py -th 1 -id 0 -dbdir D:\GitHub\BrainHant-PRO\BF -desc home -incdec 200 -save 300 -minout
python genhash.py | python BrainHunt_EX.py -th 1 -id 0 -dbdir D:\GitHub\BrainHant-PRO\BF -raw -desc home -incdec 200 -save 300 -minout
rem python genhash.py | python BrainHunt_EX.py -th 1 -id 0 -dbdir D:\GitHub\BrainHant-PRO\BF -desc home -incdec 200 -save 300 -minout
pause