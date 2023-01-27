import platform
import os
import sys
import ctypes

version_lib_non = 'NonameHunt LIB 0.3/27.01.23'

if platform.system().lower().startswith('win'):
    dllfile = 'lib/libnon.dll'
    if os.path.isfile(dllfile) == True:
        pathdll = os.path.realpath(dllfile)
        bloom_lib = ctypes.CDLL(pathdll)
    else:
        print('File {} not found'.format(dllfile))
        exit()
    
elif platform.system().lower().startswith('lin'):
    dllfile = 'lib/libnon.so'
    if os.path.isfile(dllfile) == True:
        pathdll = os.path.realpath(dllfile)
        bloom_lib = ctypes.CDLL(pathdll)
    else:
        print('File {} not found'.format(dllfile))
        exit()
    
else:
    print('[-] Unsupported Platform currently for ctypes dll method. Only [Windows and Linux] is working')
    sys.exit()

class bloom(ctypes.Structure):
    _fields_ = [("entries", ctypes.c_int),
                ("bits", ctypes.c_ulong),
                ("bytes", ctypes.c_ulong),
                ("hashes", ctypes.c_ubyte),
                ("error", ctypes.c_double),
                ("ready", ctypes.c_ubyte),
                ("major", ctypes.c_ubyte),
                ("minor", ctypes.c_ubyte),
                ("bpe", ctypes.c_double),
                ("bf", ctypes.POINTER(ctypes.c_ubyte))]
    
def bloom_add(bloom_filter, data, len_data):
    data = data if isinstance(data, bytes) else bytes(data, 'utf-8')
    c_data = ctypes.c_char_p(data)
    c_len = ctypes.c_int(len_data)
    bloom_lib.bloom_add(ctypes.byref(bloom_filter), c_data, c_len)
    
def bloom_check(bloom_filter, data, len_data):
    data = data if isinstance(data, bytes) else bytes(data, 'utf-8')
    c_data = ctypes.c_char_p(data)
    c_len = ctypes.c_int(len_data)
    return bloom_lib.bloom_check(ctypes.byref(bloom_filter), c_data, c_len)

def bloom_load(bloom_filter, path):
    c_path = ctypes.c_char_p(path.encode())
    return bloom_lib.bloom_load(ctypes.byref(bloom_filter), c_path)

def bloom_save(bloom_filter, path):
    c_path = ctypes.c_char_p(path.encode())
    return bloom_lib.bloom_save(ctypes.byref(bloom_filter), c_path)


def bloom_loadcustom(bloom_filter, path):
    c_path = ctypes.c_char_p(path.encode())
    return bloom_lib.bloom_loadcustom(ctypes.byref(bloom_filter), c_path)

def bloom_savecustom(bloom_filter, path):
    c_path = ctypes.c_char_p(path.encode())
    return bloom_lib.bloom_savecustom(ctypes.byref(bloom_filter), c_path)

def bloom_free(bloom_filter):
    bloom_lib.bloom_free(ctypes.byref(bloom_filter))

def bloom_reset(bloom_filter):
    bloom_lib.bloom_reset(ctypes.byref(bloom_filter))
    
def bloom_print(bloom_filter):
    bloom_lib.bloom_print(ctypes.byref(bloom_filter))

def init_bloom(bloom_filter,col,err):
    result = bloom_lib.bloom_init2(ctypes.byref(bloom_filter), col, ctypes.c_double(err))
    return result

'''
bloom_filter = bloom()
result = bloom_lib.bloom_init2(ctypes.byref(bloom_filter), 450000, ctypes.c_longdouble(0.0000000000001))
if result == 0:
    print("filter initialized successfully")
else:
    print("Error initializing the filter")
    
for _ in range(400000):
    res = secrets.token_hex(20)
    bloom_add(bloom_filter, res, len(res))

result = bloom_check(bloom_filter, res, len(res))
if result == 1:
    print("Data found in the filter")
elif result == 0:
    print("Data not in the filter")
else:
    print("Error")
 
#-----------------------------------------------------------

bloom_print(bloom_filter)
result = bloom_savecustom(bloom_filter, "file.bloom")
if result == 0:
    print("filter saved successfully")
else:
    print("Error saving the filter")

bloom_free(bloom_filter)
if result == 0:
    print("bloom_reset successfully")
else:
    print("Error bloom_reset")
    
bloom_filter = bloom()
result = bloom_loadcustom(bloom_filter, "file.bloom")
if result == 0:
    print("filter loaded successfully")
else:
    print(f"Error {result} loading the filter")

result = bloom_check(bloom_filter, res, len(res))
if result == 1:
    print("Data found in the filter")
elif result == 0:
    print("Data not in the filter")
else:
    print("Error")

bloom_free(bloom_filter)

'''