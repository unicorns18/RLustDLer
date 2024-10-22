class ChaCha20PRNG:
    def __init__(self, key, nonce):
        if len(key) != 32 or len(nonce) != 12:
            raise ValueError("Key must be 32 bytes and nonce must be 12 bytes")
        self.state = [0] * 16
        self.set_key(key)
        self.set_nonce(nonce)
        self.counter = 0
        self.buffer = []
    
    def set_key(self, key):
        constants = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
        self.state[:4] = constants
        self.state[4:12] = [int.from_bytes(key[i:i+4], 'little') for i in range(0, 32, 4)]
    
    def set_nonce(self, nonce):
        self.state[13:16] = [int.from_bytes(nonce[i:i+4], 'little') for i in range(0, 12, 4)]

    def chacha20_block(self):
        x = self.state.copy()
        for _ in range(10):
            self.quarter_round(x, 0, 4, 8, 12)
            self.quarter_round(x, 1, 5, 9, 13)
            self.quarter_round(x, 2, 6, 10, 14)
            self.quarter_round(x, 3, 7, 11, 15)
            self.quarter_round(x, 0, 5, 10, 15)
            self.quarter_round(x, 1, 6, 11, 12)
            self.quarter_round(x, 2, 7, 8, 13)
            self.quarter_round(x, 3, 4, 9, 14)    
        return [((x[i] + self.state[i]) & 0xffffffff) for i in range(16)]
    
    @staticmethod
    def quarter_round(x, a, b, c, d):
        x[a] = (x[a] + x[b]) & 0xffffffff
        x[d] = ChaCha20PRNG.rotate((x[d] ^ x[a]), 16)
        x[c] = (x[c] + x[d]) & 0xffffffff
        x[b] = ChaCha20PRNG.rotate((x[b] ^ x[c]), 12)
        x[a] = (x[a] + x[b]) & 0xffffffff
        x[d] = ChaCha20PRNG.rotate((x[d] ^ x[a]), 8)
        x[c] = (x[c] + x[d]) & 0xffffffff
        x[b] = ChaCha20PRNG.rotate((x[b] ^ x[c]), 7)

    @staticmethod
    def rotate(v, c):
        return ((v << c) & 0xffffffff) | (v >> (32 - c))

    def get_bytes(self, n):
        result = []
        while len(result) < n:
            if not self.buffer:
                self.state[12] = self.counter
                block = self.chacha20_block()
                self.buffer = [b for word in block for b in word.to_bytes(4, 'little')]
                self.counter += 1
            result.append(self.buffer.pop(0))
        return bytes(result[:n])

    def randint(self, a, b):
        range_size = b - a + 1
        if range_size <= 0:
            raise ValueError("Invalid range")        
        bytes_needed = (range_size.bit_length() + 7) // 8
        while True:
            value = int.from_bytes(self.get_bytes(bytes_needed), 'little')
            if value < range_size * (256 ** bytes_needed // range_size):
                return a + (value % range_size)
