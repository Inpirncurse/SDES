import fileinput

init = [1,5,2,0,3,7,4,6]
p_10 = [2,4,1,6,3,9,0,8,7,5]
p_8 = [5,2,6,3,7,4,9,8]
fei = [3,0,1,2,1,2,3,0]
inv = [3,0,2,4,6,1,7,5]

def permutation(key, original):

    perm_key = ''
    for i in range(len(original)):
        perm_key += key[original[i]]
    return perm_key

def sub_keys(key):
    
    perm_key = permutation(key,p_10)
    perm_key_left = perm_key[:5]
    perm_key_right = perm_key[5:]
    perm_key_left_shift = shift_left(perm_key_left)
    perm_key_right_shift = shift_left(perm_key_right)
    perm = perm_key_left_shift + perm_key_right_shift
    k1 = ''
    k1 = permutation(perm, p_8)
    perm_key_left_shift = permutation(perm_key_left_shift, [2,3,4,0,1])
    perm_key_right_shift = permutation(perm_key_right_shift, [2,3,4,0,1])
    perm = perm_key_left_shift + perm_key_right_shift
    k2 = ''
    k2 = permutation(perm, p_8)

    return (k1,k2)

def shift_left(perm_key_part):
    shift_string = perm_key_part[1:] + perm_key_part[0]
    return shift_string

def xor(s1, s2):
    return int(s1, base=2) ^ int(s2, base=2)

def feistel(perm_text, key, box1, box2):

    right_part = perm_text[4:]
    left_part = perm_text[:4]
    exp_r = permutation(right_part, fei)
    xor_r = xor(exp_r, key)
    xor_r = format(xor_r, '08b')
    row = int(permutation(xor_r[:4], [0,3]), base=2)
    col = int(permutation(xor_r[:4], [1,2]), base=2)
    s0 = box1[row][col]
    row = int(permutation (xor_r[4:], [0,3]), base=2)
    col = int(permutation (xor_r[4:], [1,2]), base=2)
    s1 = box2[row][col]
    sbox1_sbox2 = format(s0, '02b')+format(s1, '02b') #these are strings
    sbox1_sbox2 = permutation(sbox1_sbox2, [1,3,2,0])
    xor_l = xor(left_part, sbox1_sbox2)
    xor_l = format(xor_l, '04b')
    
    return xor_l, right_part

def main():
    lines = []
    for line in fileinput.input():
        lines.append(line.rstrip())

    action = lines[0]
    key = lines[1]
    plain_text = lines[2]

    box1 = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
    box2 = [[0,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]

    if "E" in action:
        tup = sub_keys(key)
        sub_key1 = tup[0]
        sub_key2 = tup[1]
        perm_text = permutation(plain_text, init)
        left_part, right_part = feistel(perm_text, sub_key1, box1, box2)
        comb = right_part + left_part
        left_part, right_part = feistel(comb, sub_key2, box1, box2)
        comb2 = left_part + right_part
        inverse = permutation(comb2, inv)
        print(inverse)
    else:
        tup = sub_keys(key)
        sub_key1 = tup[1]
        sub_key2 = tup[0]
        perm_text = permutation(plain_text, init)
        left_part, right_part = feistel(perm_text, sub_key1, box1, box2)
        comb = right_part + left_part
        left_part, right_part = feistel(comb, sub_key2, box1, box2)
        comb2 = left_part + right_part
        inverse = permutation(comb2, inv)
        print(inverse)

if __name__ == '__main__':
    main()
