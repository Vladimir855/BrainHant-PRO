import bitcoin,sys,random,os,time, secrets

def random_electrum_seed():
    entropy = str(os.urandom(32)) \
        + str(random.randrange(2**256)) \
        + str(int(time.time() * 1000000))
    return bitcoin.sha256(entropy.encode('utf-8'))

if __name__ == '__main__':
    while True:
        #rnd_hash = secrets.token_hex(maxLength)
        #trezor = bitcoin.entropy_to_words(rnd_hash.encode('utf-8'))
        print(random_electrum_seed())
        print(bitcoin.random_key())