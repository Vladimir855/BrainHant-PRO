import bitcoin,sys,random,os,time, secrets
import hashlib

def random_electrum_seed():
    entropy = str(os.urandom(32)) \
        + str(random.randrange(2**256)) \
        + str(int(time.time() * 1000000))
    h = hashlib.new('sha256')
    h.update(entropy.encode('utf-8'))
    return h.hexdigest()

if __name__ == '__main__':
    while True:
        print(random_electrum_seed())
        print(secrets.token_hex(32))
