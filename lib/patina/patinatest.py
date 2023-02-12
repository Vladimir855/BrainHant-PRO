from patina import HashMap
import secrets

hm: HashMap[str, int] = HashMap()
for I in range(100000):
    sec = secrets.token_hex(20)
    hm.insert(sec, I)
print(hm.len())
print(hm.contains_key(sec))
print(hm.contains_key('sec'))
hm.save('aaaaaaaaa.bbin')
hm.save_h5('H5-aaaaaaaaa.bbin')


hml = HashMap.load('aaaaaaaaa.bbin')
print('--------------------------')
print(hml.len())
print(hml.contains_key(sec))
print(hml.contains_key('sec'))

hml = HashMap.load2('aaaaaaaaa.bbin')
print('--------------------------')
print(hml.len())
print(hml.contains_key(sec))
print(hml.contains_key('sec'))

hml = HashMap.load_h5('H5-aaaaaaaaa.bbin')
print('--------------------------')
print(hml.len())
print(hml.contains_key(sec))
print(hml.contains_key('sec'))
