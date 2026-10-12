#DES: Data Encryption Standard


#DES main functions
#permutation
def permutar(bits,tabla):
    return  ''.join(bits[pos-1] for pos in tabla)

#XOR Operation
def xor(bits1, bits2):
    if len(bits1) != len(bits2):
        raise ValueError("The block must be the same lenght")
    
    return ''.join(
        '0' if a == b else '1'
        for a, b in zip(bits1, bits2)
    )

#shift to the left 
def left_shift_function(bits,cantidad):
    cantidad = cantidad % len(bits)
    return bits[cantidad:] + bits[:cantidad]

#Odd-Even function(KEDES)
def odd_even (bits):
    result = ""
    
    for i in range(len(bits)):
        if i % 2 ==0:
            result +="0"
        else:
            result += "1"
    return result

#Permuted Choice 1 64 bits -> 56 bits
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

#Permuted Choice 2 56 bits -> 48 bits
PC2= [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

#number of shifts for the 16 rounds
SHIFTS = [
    1, 1, 2, 2, 2, 2, 2, 2,
    1, 2, 2, 2, 2, 2, 2, 1
]

#Initial Permutation
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

#Inverse Initial Permutation
IP_inv = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

#SBOXES
S_BOXES = [
    # S1
    [
        [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
        [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
        [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
        [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
    ],
    # S2
    [
        [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
        [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
        [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
        [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
    ],
    # S3
    [
        [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
        [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
        [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
        [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]
    ],
    # S4
    [
        [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
        [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
        [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
        [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
    ],
    # S5
    [
        [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
        [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
        [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
        [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
    ],
    # S6
    [
        [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
        [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
        [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
        [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]
    ],
    # S7
    [
        [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
        [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
        [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
        [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
    ],
    # S8
    [
        [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
        [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
        [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
        [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
    ]
]
#Permutation P
P = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]

#Positions for KD function
KD_PC1 = [8, 16, 24, 32, 40, 48, 56, 64]
KD_PC2 = [9, 18, 27, 36, 15, 22, 29, 4]

def key_generator(key, mode="DES"):
    
    if len(key) != 64 or any(bit not in "01" for bit in key):
        raise ValueError("The key must contain 64 binary bits")
    #Apply PC1
    key_56 = permutar(key,PC1)
    
    if mode=="KE-DES":
        key_56= odd_even(key_56)
        
    
    #Divide in 2 the key
    C = key_56[:28]
    D = key_56[28:]
    
    subkeys = []
    
    #16 subkeys
    for shifts in SHIFTS:
        C = left_shift_function(C,shifts)
        D = left_shift_function(D,shifts)
        
        #Concatenate two halves
        combine = C + D
        
        #Apply PC2
        subkey = permutar(combine, PC2)
        subkeys.append(subkey)
        
    return subkeys 

def prepare_blocks(texto):
    if len(texto) != 64 or any(bit not in "01" for bit in texto):
        raise ValueError("The block must contain 64 bits")
    
    #Apply IP
    block = permutar(texto, IP)
    
    #Divide 2 blocks in 32 bits
    L = block[:32]
    R = block[32:]
    
    return L, R

def S_box(bits):
    
    if len(bits) != 48:
        raise ValueError("S-Boxes require 48 bits")
    
    result = ""
    
    for i in range (8):
        
        #take  6 bits
        block = bits[i * 6:(i + 1)*6]
        
        #first and last bit for the row
        row = int(block[0] + block[5],2)
        
        #miiddle 4 bits the column
        column = int(block[1:5],2)
        
        #Respective Sbox
        value = S_BOXES[i][row][column]
        
        #Convert the value to 4 binary bits
        result +=format(value, "04b")
        
    return result

def permutation_p(bits):
    
    if len(bits) != 32:
        raise ValueError("Permutation P requires 32 bits")
    
    return permutar(bits, P)

def function_kd(R, original_key, subkey):
    if len(R) != 32:
        raise ValueError("R must contain 32 bits")
    
    if len(original_key) != 64:
        raise ValueError("The original key must contain 64 bits")
    
    if len(subkey) != 48:
        raise ValueError("The subkey must contain 48 bits")
    
    #Select the 8 bits from pc1
    pc1_part = permutar(original_key, KD_PC1)
    
    #select 8 bits from pc2
    pc2_part =permutar(subkey, KD_PC2)
    
    #Combine R, and the 16 bits from pc1 and pc2
    result = pc1_part+ R + pc2_part
    
    return result

def f_function(R, subkey, original_key):
    
    #step 1 KD function 32 bits --> 48 bits
    kd_result = function_kd(R, original_key, subkey)
    
    #Step 2 XOR with round key
    xor_result = xor(kd_result, subkey)
    
    #step 3 S-Boxes 48 bits --> 32 bits
    sbox_result = S_box(xor_result)
    
    #Step 4 Permutation P 32 bits --> 32 bits
    p_result = permutation_p(sbox_result)
    
    return p_result

def feistel_rounds(L, R, subkeys, original_key):
    
    for i in range(16):
        
        new_L = R
        
        f_result = f_function(R, subkeys[i], original_key)
        
        new_R = xor(L, f_result)
        
        L = new_L
        R = new_R
        
        print(f"Round {i + 1}")
        print("L:", L)
        print("R:", R)
        print()
        
    return L, R

def kedes_cipher(text, key):
    
    #Step 1 IP and Split
    L, R = prepare_blocks(text)
    
    #Step 2 Generate 16 round keys
    subkeys = key_generator(key, "KE-DES")
    
    #Step 3 Apply 16 rounds
    L_final, R_final = feistel_rounds(L, R, subkeys, key)
    
    #step 4 Swap the final halves
    final_block = R_final + L_final
    
    #step 5 Apply inverse IP
    
    cipher_text = permutar(final_block, IP_inv)
    
    return cipher_text

def kedes_decipher(cipher, key):
    
    #Initial Permutation
    L, R = prepare_blocks(cipher)
    
    #Generate the same 16 keys
    round_keys = key_generator(key,"KE-DES")
    
    #reverse the order of the keys
    reversed_keys= round_keys[::-1]
    
    #Apply 16 rounds
    L_final, R_final = feistel_rounds(
        L, R, reversed_keys, key
    )

    #swap the final halves
    final_block = R_final + L_final
    
    #Inverse IP
    original_text = permutar(final_block, IP_inv)
    
    return original_text
    

if __name__ == "__main__":
    
    hex_key = "133457799BBCDFF1"
    
    key = format(int(hex_key, 16),"064b")
    
    text_hex = "0123456789ABCDEF"
    text = format(int(text_hex, 16), "064b")
    
    cipher = kedes_cipher(text, key)
    
    print("Original:",text)
    print("Encrypted:", cipher)
    print("Encrypted lenght", len(cipher))
    
    cipher_hex = format(int(cipher, 2), "016X")
    print("Encrypted Value:",cipher_hex)
    
    
    print("\nDecryption\n")
    
    decrypted = kedes_decipher(cipher,key)
    
    print("Original: ", text)
    print("Decrypted: ", decrypted)
    
    print("Match:", text == decrypted)
    
    decrypted_hex = format(int(decrypted, 2),"016X")
    print("Decrypted HEX:", decrypted_hex)
    
    if text_hex == decrypted_hex:
        print("Lo logro señor")