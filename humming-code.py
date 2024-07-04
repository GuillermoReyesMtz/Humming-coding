import os
import sys
import numpy as np


def add_padding(bitschain):
    if len(bitschain) % 4 != 0:
        bitschain.append(1)
        bitschain.append(0)
        add_padding(bitschain)
    if len(bitschain) % 4 == 0:
        return bitschain


def remove_padding(bitschain_paded, original_data):
    diff = len(bitschain_paded) - len(original_data)
    for i in range(0, 2):
        del bitschain_paded[-1]
    return bitschain_paded

def split_into_4bits(databits):
    data_in_4bits = []
    for i in range(0, len(databits)):
        j = databits[i]
        data_in_4bits.append(j[0:4])
        data_in_4bits.append((j[4:8]))
    return data_in_4bits

def turn_4bits_into_matrixes(bitslist):
    mat = []
    for i in bitslist:
        for j in i:
            mat.append(j)
    return mat
    

# Open a binary file
huffman_compressed_file = open(
    r'C:\Users\memo_\OneDrive - Universidad Autonoma de Yucatan\MCC'
    r'\Matemáticas Discretas\Humming-coding\Alejo-Carpentier-Los-Pasos-Perdidos.bin', 'rb')

# Read lines
huffman_compressed_file_data = huffman_compressed_file.read()
# Lista del archivo en bytes
huffman_compressed_file_data_in_bytes = []
# Lista del archivo en bits
huffman_compressed_file_data_in_8bits = []
# Matriz G
g = [[1, 1, 1, 0, 0, 0, 0, 1],
     [1, 0, 0, 1, 1, 0, 0, 1],
     [0, 1, 0, 1, 0, 1, 0, 1],
     [1, 1, 0, 1, 0, 0, 1, 0]]

# Display the data
# print("compressed = ", huffman_compressed_file_data)

try:
    with open(r'C:\Users\memo_\OneDrive - Universidad Autonoma de Yucatan\MCC\Matemáticas '
              r'Discretas\Humming-coding\Alejo-Carpentier-Los-Pasos-Perdidos.bin', 'rb') as f:
        byte = f.read(1)
        while byte:
            # Do stuff with byte.
            byte = f.read(1)
            huffman_compressed_file_data_in_bytes.append(byte)
            # print(byte)
    #print("compressed = ", huffman_compressed_file_data_in_bytes[1])
except IOError:
    print('Error While Opening the file!')

for bytes in huffman_compressed_file_data_in_bytes:
    bits: int
    for bits in bytes:
        byteabit = f'{bits:0>8b}'
        huffman_compressed_file_data_in_8bits.append(byteabit)

print(len(huffman_compressed_file_data_in_8bits))
huffman_compressed_file_data_in_bits_padded = add_padding(huffman_compressed_file_data_in_8bits)
print(len(huffman_compressed_file_data_in_bits_padded))
huffman_compressed_file_data_in_bits_depadded = remove_padding(huffman_compressed_file_data_in_bits_padded,
                                                               huffman_compressed_file_data_in_8bits)
print(len(huffman_compressed_file_data_in_bits_depadded))
print(huffman_compressed_file_data_in_8bits[-1])
print(huffman_compressed_file_data_in_bits_padded[0])
print(huffman_compressed_file_data_in_bits_depadded[0])
a = split_into_4bits(huffman_compressed_file_data_in_8bits)
b = turn_4bits_into_matrixes(a)
real = np.bitwise_and(b, 0x0f)
print(real)

# functions for humming error prevention code generation
