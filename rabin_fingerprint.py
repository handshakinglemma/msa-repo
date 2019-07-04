import random
# import matplotlib.pyplot as plt
from collections import deque
import os
import json
import pdb

class fingerprinter:
    def __init__(self, d_size):
        self.window = pow(2, d_size + 1) - 1
        self.remainder = 0
        self.mask = 1 << d_size
        self.irreducible = irreducible_polynomial(d_size)

    def update(self, b): #Updates the remainder when supplied the next bit in the sequence
        self.remainder <<= 1 #Left shift the remainder
        self.remainder |= b #Append the new bit
        self.remainder &= self.window #Prevent the remainder from growing larger than needed
        if self.remainder & self.mask > 0:
            self.remainder ^= self.irreducible
        return self.remainder

    def flush(self):
        self.remainder = 0

class windowFingerprinter:
    def __init__(self, degree, irreducible):
        self.remainder = 0
        self.irreducible = irreducible
        self.window = deque([0] * (degree + 1))
        self.mask = 1 << degree
        self.pop_polynomial = divide_polynomial(1 << (degree + 1), self.irreducible)

    def update(self, bit):
        self.remainder <<= 1
        self.remainder |= bit
        if self.remainder & self.mask > 0:
            self.remainder ^= self.irreducible
        if self.window.pop() == 1:
            self.remainder ^= self.pop_polynomial
        self.window.appendleft(bit)
        return self.remainder

    def flush(self):
        self.remainder =  0

class byteWindowFingerprinter:
    def __init__(self, degree, irreducible):
        self.remainder = 0
        self.irreducible = irreducible
        self.leading_window_bit = 0
        self.window = deque([0] * (degree // 8)) #Degree must be divisible by 8
        self.incoming_table = compute_incoming_table(self.irreducible, degree)
        self.outgoing_table = compute_outgoing_table(self.irreducible, degree)
        self.degree = degree

    def update(self, byte):
        outgoing_byte = self.window.pop()
        new_leading_bit = outgoing_byte & 1
        outgoing_byte >>= 1
        outgoing_byte |= self.leading_window_bit << 7
        self.leading_window_bit = new_leading_bit
        self.remainder = (self.remainder << 8) | byte
        self.remainder = self.remainder ^ self.incoming_table[self.remainder >> self.degree] ^ self.outgoing_table[outgoing_byte]
        self.window.appendleft(byte)
        return self.remainder

    def flush(self):
        self.remainder =  0
        self.window = deque([0] * (self.degree // 8))

def compute_incoming_table(irreducible, degree):
    table = [0] * 256
    for byte in range(256):
        poly_sum = byte << degree
        irreducible <<= 7
        mask = 1 << (degree + 7)
        for i in range(8):
            if mask & poly_sum > 0:
                poly_sum ^= irreducible
            mask >>= 1
            irreducible >>= 1
        table[byte] = poly_sum
    return table

def compute_outgoing_table(irreducible, degree):
    table = [0] * 256
    divs = [0] * 8
    for i in range(8):
        divs[i] = divide_polynomial(1 << (i + degree + 1), irreducible)
    for byte in range(256):
        poly_sum = 0
        bcopy = byte
        for i in range(8):
            if byte & 1 > 0:
                poly_sum ^=  divs[i]
            byte >>= 1
        table[bcopy] = poly_sum
    return table

#Most recent one, work off of this code (as well as incoming/outgoing table3)
class byteWindowFingerprinter3:
    def __init__(self, irreducible, window_size):
        self.window = deque([0] * window_size)
        self.incoming_table = compute_incoming_table3(irreducible)
        self.outgoing_table = compute_outgoing_table3(irreducible, window_size)
        self.fingerprint = 0
        self.degree = irreducible.bit_length() - 1
        self.mask1 = ((2**8) - 1) << (self.degree - 8)
        self.mask2 = (2**self.degree) - 1

    def update(self, byte):
        top_byte = self.mask1 & self.fingerprint
        self.fingerprint = self.incoming_table[top_byte >> (self.degree - 8)] ^ self.outgoing_table[self.window.pop()] ^ \
                            ((self.fingerprint << 8) | byte) & self.mask2
        self.window.appendleft(byte)
        return self.fingerprint

    def flush(self):
        self.fingerprint = 0
        self.window = deque([0] * len(self.window))

def compute_incoming_table3(irreducible):
    table = [0] * 2**8
    for byte in range(2**8):
        table[byte] = divide_polynomial(byte << (irreducible.bit_length() - 1), irreducible)
    return table

def compute_outgoing_table3(irreducible, window_size):
    table = [0] * (2**8)
    for byte in range(2**8):
        r = byte
        for i in range(window_size):
            r = divide_polynomial(r << 8, irreducible)
        table[byte] = r
    return table


# class byteWindowFingerprinter2:
#     def __init__(self, degree, irreducible, step_size):
#         self.remainder = 0
#         self.step_size = step_size
#         self.irreducible = irreducible
#         self.window = deque([0] * (degree // 8)) #Degree must be divisible by 8
#         self.leading_window_bit = 0
#         self.incoming_table = compute_incoming_table2(self.irreducible, degree, step_size)
#         self.outgoing_table = compute_outgoing_table2(self.irreducible, degree, step_size)
#         self.degree = degree
#
#     def update(self, byte):
#         pdb.set_trace()
#         self.remainder <<= self.step_size
#         self.remainder |= byte
#         top_byte = self.remainder >> self.degree
#         self.remainder ^= self.incoming_table[top_byte]
#         outgoing_byte = self.window.pop()
#         new_leading_bit = outgoing_byte & 1
#         outgoing_byte >>= 1
#         outgoing_byte |= self.leading_window_bit << 7
#         self.remainder ^= self.outgoing_table[outgoing_byte]
#         self.leading_window_bit = new_leading_bit
#         self.window.appendleft(byte)
#         return self.remainder
#
#     def flush(self):
#         self.remainder =  0

# def compute_incoming_table2(irreducible, degree, step_size):
#     # file_name = "incoming_table_" + str(irreducible) + "_" + str(degree) + "_" + str(step_size) + ".json"
#     # if os.path.isfile(file_name):
#     #     return json.loads(open(file_name, 'r').read())
#     # pdb.set_trace()
#     table = [0] * (2 ** step_size)
#     for step in range(2 ** step_size):
#         poly_sum = step << degree
#         irreducible <<= step_size - 1
#         mask = 1 << (degree + step_size - 1)
#         for i in range(step_size):
#             if mask & poly_sum > 0:
#                 poly_sum ^= irreducible
#             if i == step_size - 1:
#                 break
#             mask >>= 1
#             irreducible >>= 1
#         table[step] = poly_sum
#         # if poly_sum != divide_polynomial(step << degree, irreducible):
#         #     raise(str(step))
#     # f = open(file_name, 'w')
#     # f.write(json.dumps(table))
#     return table
#
# def compute_outgoing_table2(irreducible, degree, step_size):
#     # file_name = "outgoing_table_" + str(irreducible) + "_" + str(degree) + "_" + str(step_size) + ".json"
#     # if os.path.isfile(file_name):
#     #     return json.loads(open(file_name, 'r').read())
#     pdb.set_trace()
#     table = [0] * (2 ** step_size)
#     divs = [0] * step_size
#     for i in range(step_size):
#         divs[i] = divide_polynomial(1 << (i + degree + 1), irreducible)
#     for step in range(2 ** step_size):
#         poly_sum = 0
#         step_copy = step
#         for i in range(step_size):
#             if step & 1 > 0:
#                 poly_sum ^=  divs[i]
#             step >>= 1
#         table[step_copy] = poly_sum
#     # f = open(file_name, 'w')
#     # f.write(json.dumps(table))
#     return table


def irreducible_polynomial(d): #Return a random polynomial of degree. Degree must be > 1
    random.seed(d)
    p = 1 #Start with leading coefficient of 1 so the polynomial is of degree d
    odd = False #is there an odd number of non-zero coefficients? Must be odd to be irreducible.
                #Starts False as the constant coefficient is always set to 1 at the end
    for i in range(d - 1):
        p = p << 1
        if bool(random.getrandbits(1)): #Randomly set coefficients to 1
            p = p | 1
            odd = not odd
    p = p << 1
    p = p | 1 #Add the trailing coefficient of one. Must have this for irreducible polynomials
    if not odd: #Make sure there's an odd number of non-zero coefficients
        index = random.randint(1, d - 1) #Get a random non-leading and non-trailing coefficient
        mask = 1 << index
        if p & mask == 0: #Swap the coefficient value to make an odd number
            p = p | mask #The bit is 0, set to 1
        else:
            p = p ^ mask #The bit is 1, set to 0
    return p


def divide_polynomial(p1, p2): #return p1 - p2. Assuming p1 >= p2
    mask = 1
    org_p2 = p2
    while mask <= p2: #Align the mask to be one bit higher than the leading coefficient of p2
        mask = mask << 1
    while mask <= p1: #Push the mask and p2 left untill the mask is one bit higher than p1, making
                      #the leading coefficients of p1 and p2 line up
        mask = mask << 1
        p2 = p2 << 1
    mask = mask >> 1 #The mask is now inline with the leading coefficient of p1
    while p2 >= org_p2:
        if mask & p1 > 0: #If there is a coefficient in the place being currently looked at
            p1 = p1 ^ p2 #Subtract p2 from p1
        mask = mask >> 1 #Move the mask and p2 over
        p2 = p2 >> 1
    return p1 #Return the remainder

def print_bits(x, n=0):
    lst = []
    while x > 0:
        lst.insert(0, str(x & 1) + " ")
        x = x >> 1
    while n > len(lst):
        lst.insert(0, "0 ")
    print("".join(lst))

def print_bit_len(x):
    n = 0
    while x > 0:
        n += 1
        x >>= 1
    print(n)

def eval(p):
    sum = 0
    while p > 0:
        sum = (sum + (p & 1)) % 2
        p = p >> 1
        return sum
