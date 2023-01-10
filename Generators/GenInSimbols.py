import itertools
import sys
import datetime, time
from itertools import combinations_with_replacement,product
import string
#abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_,.#$

if __name__ == '__main__':
    a1 = '0;1;2;3;4;5;6;7;8;9'
    a2 = '.;-;_;#;$'
    a3 = 'a;b;c;d;e;f;g;h;i;j;k;l;m;n;o;p;q;r;s;t;u;v;w;x;y;z'
    a4 = 'A;B;C;D;E;F;G;H;I;J;K;L;M;N;O;P;Q;R;S;T;U;V;W;X;Y;Z'
    a5 = '.'
    s1 = [f'{a1}',f'{a1};{a5}',f'{a3}',f'{a3};{a5}',f'{a4};{a5}',f'{a1};{a3}'f'{a1};{a4}']
    s2 = '@aol.com'
    maxLength = 10
    for str in s1:
        pwdKeys = str.split(';')
        for t in range(maxLength+1):
            pwd = product(pwdKeys, repeat = int(t))
            for i in pwd:
                password = "".join(i)
                sys.stdout.write(f'{password}{s2} \n')