from bitarray import bitarray


class Sha256:
    binary_message = bitarray()
    blocks = []

    def __init__(self):
        self.h0 = bitarray(format(0x6a09e667, "032b"))
        self.h1 = bitarray(format(0xbb67ae85, "032b"))
        self.h2 = bitarray(format(0x3c6ef372, "032b"))
        self.h3 = bitarray(format(0xa54ff53a, "032b"))
        self.h4 = bitarray(format(0x510e527f, "032b"))
        self.h5 = bitarray(format(0x9b05688c, "032b"))
        self.h6 = bitarray(format(0x1f83d9ab, "032b"))
        self.h7 = bitarray(format(0x5be0cd19, "032b"))

        k_int = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]
        self.k = []
        self.tt = []
        for i in k_int:
            self.k.append(bitarray(format(i, "032b")))

    def __logic_and(self, array1, array2):
        return_array = bitarray()
        for i in range(len(array1)):
            if array1[i] == 1 and array2[i] == 1:
                return_array.append(1)
            else:
                return_array.append(0)
        return return_array

    def __logic_not(self, array):
        return_array = bitarray()
        for i in range(len(array)):
            if array[i] == 0:
                return_array.append(1)
            else:
                return_array.append(0)
        return return_array

    def __array_sum(self, array1, array2):
        return_array = bitarray()
        hold = 0
        for i in range(32):
            return_array.append(0)
        for i in range(31, -1, -1):
            return_array[i] = (array1[i] + array2[i] + hold) % 2
            if array1[i] + array2[i] + hold > 1:
                hold = 1
            else:
                hold = 0
        return return_array

    def __xor(self, array1, array2):
        return_array = bitarray()
        for i in range(len(array1)):
            if (array1[i] == 1 and array2[i] == 0) or (array1[i] == 0 and array2[i] == 1):
                return_array.append(1)
            else:
                return_array.append(0)
        return return_array

    def __leftshift(self, array, count):
        return array[count:] + (bitarray('0') * count)

    def __rightshift(self, array, count):
        return (bitarray('0') * count) + array[:-count]

    def __rightrotate(self, array, count):
        return (array[-count:]) + array[:-count]

    def __build_blocks(self):
        for block_start in range(0, len(self.binary_message), 512):
            self.blocks.append(self.binary_message[block_start:block_start + 512])

    def __create_message_schedule(self, block):
        schedules = []
        for block in self.blocks:
            for chunk_start in range(0, len(block), 32):
                schedules.append(block[chunk_start: chunk_start + 32])
        for i in range(16, 64):
            # schedules.append(bitarray())
            s0 = self.xor(self.xor(self.rightrotate(schedules[i - 15], 7), self.rightrotate(schedules[i - 15], 18)),
                          self.rightshift(schedules[i - 15], 3))
            s1 = self.xor(self.xor(self.rightrotate(schedules[i - 2], 17),
                                   self.rightrotate(schedules[i - 2], 19)), self.rightshift(schedules[i - 2], 10))
            schedules.append(
                self.array_sum(self.array_sum(self.array_sum(schedules[i - 16], s0), schedules[i - 7]), s1))

        return schedules

    def __pad_message(self):
        original_length = len(self.binary_message)
        self.binary_message.append(1)
        while (len(self.binary_message)) % 512 != 448:
            self.binary_message.append(0)
        for i in range(len(bin(original_length)[2:]), 64):
            self.binary_message.append(0)

        for binary_digit in bin(original_length)[2:]:
            self.binary_message.append(int(binary_digit))

    def __calculate(self):
        self.pad_message()
        self.build_blocks()

        print(len(self.blocks))
        for block in self.blocks:
            schedules = self.create_message_schedule(block)
            a = self.h0
            b = self.h1
            c = self.h2
            d = self.h3
            e = self.h4
            f = self.h5
            g = self.h6
            h = self.h7
            for i in range(64):
                S1 = self.xor(self.xor(self.rightrotate(e, 6), self.rightrotate(e, 11)), self.rightrotate(e, 25))
                ch = self.xor(self.logic_and(e, f), self.logic_and(self.logic_not(e), g))
                temp1 = self.array_sum(self.array_sum(self.array_sum(self.array_sum(h, S1), ch), self.k[i]),
                                       schedules[i])
                S0 = self.xor(self.xor(self.rightrotate(a, 2), self.rightrotate(a, 13)), self.rightrotate(a, 22))
                maj = self.xor(self.xor(self.logic_and(a, b), self.logic_and(a, c)), self.logic_and(b, c))
                temp2 = self.array_sum(S0, maj)
                h = g
                g = f
                f = e
                e = self.array_sum(d, temp1)
                d = c
                c = b
                b = a
                a = self.array_sum(temp1, temp2)
            self.h0 = self.array_sum(self.h0, a)
            self.h1 = self.array_sum(self.h1, b)
            self.h2 = self.array_sum(self.h2, c)
            self.h3 = self.array_sum(self.h3, d)
            self.h4 = self.array_sum(self.h4, e)
            self.h5 = self.array_sum(self.h5, f)
            self.h6 = self.array_sum(self.h6, g)
            self.h7 = self.array_sum(self.h7, h)
        self.digest = self.h0 + self.h1 + self.h2 + self.h3 + self.h4 + self.h5 + self.h6 + self.h7

    def __calculate_hash_from_file(self,file_path):
        file = open(file_path,'rb')
        self.binary_message.fromfile(file)
        self.calculate()
        file.close()
        return hex(int(str(self.digest)[10:-2],2))[2:]
