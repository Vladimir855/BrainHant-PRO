import ctypes
import os
import platform

version_LIB = "2.9 / 05.02.23"

class LibHUNT:
    if platform.system().lower().startswith('win'):
        dllfile = 'lib/libhunt.dll'
        if os.path.isfile(dllfile) == True:
            pathdll = os.path.realpath(dllfile)
            __lib = ctypes.CDLL(pathdll)
        else:
            print('File {} not found'.format(dllfile))
            exit(1)
        
    elif platform.system().lower().startswith('lin'):
        dllfile = 'lib/libhunt.so'
        if os.path.isfile(dllfile) == True:
            pathdll = os.path.realpath(dllfile)
            __lib = ctypes.CDLL(pathdll)
        else:
            print('File {} not found'.format(dllfile))
            exit(1)
        
    else:
        print('[-] Unsupported Platform currently for ctypes dll method. Only [Windows and Linux] is working')
        exit(1)
    
    # bloom_alloc
    __lib.bloom_alloc.argtypes = []
    __lib.bloom_alloc.restype = ctypes.c_void_p
    __bloom_alloc = __lib.bloom_alloc
    # bloom_dealloc
    __lib.bloom_dealloc.argtypes = [ctypes.c_void_p]
    __lib.bloom_dealloc.restype = None
    __bloom_dealloc = __lib.bloom_dealloc
    # bloom_init2
    __lib.bloom_init2.argtypes = [ctypes.c_void_p, ctypes.c_ulonglong, ctypes.c_double]
    __lib.bloom_init2.restype = ctypes.c_ulonglong
    __bloom_init2 = __lib.bloom_init2
    # bloom_check
    __lib.bloom_check.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulonglong]
    __lib.bloom_check.restype = ctypes.c_longlong
    __bloom_check = __lib.bloom_check
    # bloom_add
    __lib.bloom_add.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulonglong]
    __lib.bloom_add.restype = ctypes.c_longlong
    __bloom_add = __lib.bloom_add
    # bloom_free
    __lib.bloom_free.argtypes = [ctypes.c_void_p]
    __lib.bloom_free.restype = None
    __bloom_free = __lib.bloom_free
    # bloom_reset
    __lib.bloom_reset.argtypes = [ctypes.c_void_p]
    __lib.bloom_reset.restype = ctypes.c_ulonglong
    __bloom_reset = __lib.bloom_reset
    # bloom_save
    __lib.bloom_save.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    __lib.bloom_save.restype = ctypes.c_ulonglong
    __bloom_save = __lib.bloom_save
    # bloom_load
    __lib.bloom_load.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    __lib.bloom_load.restype = ctypes.c_ulonglong
    __bloom_load = __lib.bloom_load
    # bloom_version
    __lib.bloom_version.argtypes = []
    __lib.bloom_version.restype = ctypes.c_char_p
    __bloom_version = __lib.bloom_version
    #keccak-sha3
    __lib.sha3_256.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.c_size_t, ctypes.POINTER(ctypes.c_ubyte)]
    __lib.sha3_256.restype = None
    __lib_sha3 = __lib.sha3_256
    #keccak-keyhunt
    __lib.KECCAK_256.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t, ctypes.POINTER(ctypes.c_uint8)]
    __lib.KECCAK_256.restype = None
    __lib_keccak_KH = __lib.KECCAK_256
    #keccak
    __lib.keccak_256.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.c_size_t, ctypes.POINTER(ctypes.c_ubyte)]
    __lib.keccak_256.restype = None
    __lib_keccak = __lib.keccak_256
    #sha256
    __lib.sha256.argtypes = [ctypes.c_void_p, ctypes.c_ulonglong, ctypes.c_void_p]
    __lib.sha256.restype = ctypes.c_void_p
    __lib_sha256 = __lib.sha256
    #old electrum seed
    __lib.elec_old_seed.argtypes = [ctypes.c_char_p]
    __lib.elec_old_seed.restype = ctypes.c_char_p
    __lib_old_elec_seed = __lib.elec_old_seed

    @staticmethod
    def old_elec(data: bytes) -> bytes:
        hash = LibHUNT.__lib_old_elec_seed(data)
        return hash

    @staticmethod
    def get_keccak_KH(data: bytes):
        digest = ctypes.create_string_buffer(32)
        data_array = (ctypes.c_ubyte * len(data))(*data)
        LibHUNT.__lib_keccak_KH(data_array, len(data_array), ctypes.cast(digest, ctypes.POINTER(ctypes.c_ubyte)))
        return digest.raw

    @staticmethod
    def get_keccak(data: bytes):
        digest = ctypes.create_string_buffer(32)
        data_array = (ctypes.c_ubyte * len(data))(*data)
        LibHUNT.__lib_keccak(data_array, len(data_array), ctypes.cast(digest, ctypes.POINTER(ctypes.c_ubyte)))
        return digest.raw
    
    @staticmethod
    def get_sha3(data: bytes) -> bytes:
        digest = ctypes.create_string_buffer(32)
        data_array = (ctypes.c_ubyte * len(data))(*data)
        LibHUNT.__lib_sha3(data_array, len(data_array), ctypes.cast(digest, ctypes.POINTER(ctypes.c_ubyte)))
        return digest.raw

    @staticmethod
    def get_sha256(data: bytes) -> bytes:
        output = (ctypes.c_ubyte * 32)()
        LibHUNT.__lib_sha256(data, len(data), ctypes.byref(output))
        return bytes(output)

    @staticmethod
    def version() -> str:
        """Returns libbloom version.

            Returns:
                str: Version number"""
        return LibHUNT.__bloom_version().decode("utf-8")

    def __init__(self, entries: int, error: float):
        """Creates LibBloom instance.

            Parameters:
                entries (int): Number of entries (>= 1000)
                error (float): Error rate (0 to 1 inclusively)"""
        self.__bloom = LibHUNT.__bloom_alloc()
        result = LibHUNT.__bloom_init2(self.__bloom, entries, error)
        if result != 0:
            LibHUNT.__bloom_dealloc(self.__bloom)
            raise RuntimeError("LibBloom.__init__: bad parameters (entries or error)")

    def __del__(self):
        LibHUNT.__bloom_dealloc(self.__bloom)

    def free(self) -> None:
        """Releases the internal buffer.

        Not recommended because the internal buffer is released automatically
        when LibBloom instance is garbage-collected."""
        LibHUNT.__bloom_free(self.__bloom)

    def reset(self) -> None:
        """Resets the internal buffer as if nothing was added to the filter and it is empty."""
        result = LibHUNT.__bloom_reset(self.__bloom)
        if result != 0:
            raise RuntimeError("LibBloom.reset: bloom not ready")

    def check(self, buffer: str) -> bool:
        """Checks if the given item is present in the filter.

            Parameters:
                buffer (bytes): Item to check.
            Returns:
                bool: Is item in the filter."""
        if type(buffer) == str: fixed = buffer.zfill(40)
        binary_data = buffer if isinstance(buffer, bytes) else bytes.fromhex(buffer)
        result = LibHUNT.__bloom_check(self.__bloom, binary_data, len(binary_data))
        if result == -1:
            raise RuntimeError("[E] libhunt check bloom: bloom not ready")
        else:
            return result == 1

    def add(self, buffer: str) -> bool:
        """Adds the given item to the filter.

            Parameters:
                buffer (bytes): Item to add.
            Returns:
                bool: True if the item added, False if the item is already in the filter"""
        if type(buffer) == str: fixed = buffer.zfill(40)
        binary_data = buffer if isinstance(buffer, bytes) else bytes.fromhex(buffer)
        result = LibHUNT.__bloom_add(self.__bloom, binary_data, len(binary_data))
        if result == -1:
            raise RuntimeError("[E] libhunt add bloom: bloom not ready")
        else:
            return result == 0

    def save(self, filename: str) -> None:
        """Saves the filter to the file.

            Parameters:
                filename (str): File name to save the filter to.
                """
        bytebuf = filename.encode("utf-8")
        result = LibHUNT.__bloom_save(self.__bloom, bytebuf)
        if result != 0:
            raise RuntimeError("LibBloom.save: cannot save")

    def load(self, filename: str) -> None:
        """Loads the filter from the file.

            Parameters:
                filename (str): File name to load the filter from.
                """
        bytebuf = filename.encode("utf-8")
        result = LibHUNT.__bloom_load(self.__bloom, bytebuf)
        if result != 0:
            error = None
            if result == 1:
                error = "empty file name"
            elif result == 2:
                error = "bloom is null pointer"
            elif result == 3:
                error = "cannot open file"
            elif result == 4:
                error = "incorrect BLOOM_MAGIC length"
            elif result == 5:
                error = "incorrect BLOOM_MAGIC value"
            elif result == 6:
                error = "cannot read bloom size"
            elif result == 7:
                error = "incorrect bloom size"
            elif result == 8:
                error = "cannot read bloom"
            elif result == 9:
                error = "incorrect BLOOM_VERSION_MAJOR"
            elif result == 10:
                error = "cannot allocate buffer"
            elif result == 11:
                error = "cannot read bloom buffer"
            else:
                error = "unknown error"
            raise RuntimeError(error)
