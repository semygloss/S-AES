import random
import re
import threading
import time

S_box = [0x9, 0x4, 0xA, 0xB,
         0xD, 0x1, 0x8, 0x5,
         0x6, 0x2, 0x0, 0x3,
         0xC, 0xE, 0xF, 0x7]

I_box = [0xA, 0x5, 0x9, 0xB,
         0x1, 0x7, 0x8, 0xF,
         0x6, 0x0, 0x2, 0x3,
         0xC, 0x4, 0xD, 0xE]

# RCON
RCON = ['10000000', '00110000']
MIX_add = [[0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF],
           [0x1, 0x0, 0x3, 0x2, 0x5, 0x4, 0x7, 0x6, 0x9, 0x8, 0xB, 0xA, 0xD, 0xC, 0xF, 0xE],
           [0x2, 0x3, 0x0, 0x1, 0x6, 0x7, 0x4, 0x5, 0xA, 0xB, 0x8, 0x9, 0xE, 0xF, 0xC, 0xD],
           [0x3, 0x2, 0x1, 0x0, 0x7, 0x6, 0x5, 0x4, 0xB, 0xA, 0x9, 0x8, 0xF, 0xE, 0xD, 0xC],
           [0x4, 0x5, 0x6, 0x7, 0x0, 0x1, 0x2, 0x3, 0xC, 0xD, 0xE, 0xF, 0x8, 0x9, 0xA, 0xB],
           [0x5, 0x4, 0x7, 0x6, 0x1, 0x0, 0x3, 0x2, 0xD, 0xC, 0xF, 0xE, 0x9, 0x8, 0xB, 0xA],
           [0x6, 0x7, 0x4, 0x5, 0x2, 0x3, 0x0, 0x1, 0xE, 0xF, 0xC, 0xD, 0xA, 0xB, 0x8, 0x9],
           [0x7, 0x6, 0x5, 0x4, 0x3, 0x2, 0x1, 0x0, 0xF, 0xE, 0xD, 0xC, 0xB, 0xA, 0x9, 0x8],
           [0x8, 0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF, 0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7],
           [0x9, 0x8, 0xB, 0xA, 0xD, 0xC, 0xF, 0xE, 0x1, 0x0, 0x3, 0x2, 0x5, 0x4, 0x7, 0x6],
           [0xA, 0xB, 0x8, 0x9, 0xE, 0xF, 0xC, 0xD, 0x2, 0x3, 0x0, 0x1, 0x6, 0x7, 0x4, 0x5],
           [0xB, 0xA, 0x9, 0x8, 0xF, 0xE, 0xD, 0xC, 0x3, 0x2, 0x1, 0x0, 0x7, 0x6, 0x5, 0x4],
           [0xC, 0xD, 0xE, 0xF, 0x8, 0x9, 0xA, 0xB, 0x4, 0x5, 0x6, 0x7, 0x0, 0x1, 0x2, 0x3],
           [0xD, 0xC, 0xF, 0xE, 0x9, 0x8, 0xB, 0xA, 0x5, 0x4, 0x7, 0x6, 0x1, 0x0, 0x3, 0x2],
           [0xE, 0xF, 0xC, 0xD, 0xA, 0xB, 0x8, 0x9, 0x6, 0x7, 0x4, 0x5, 0x2, 0x3, 0x0, 0x1],
           [0xF, 0xE, 0xD, 0xC, 0xB, 0xA, 0x9, 0x8, 0x7, 0x6, 0x5, 0x4, 0x3, 0x2, 0x1, 0x0]]

MIX_x = [0x0, 0x4, 0x8, 0xC, 0x3, 0x7, 0xB, 0xF, 0x6, 0x2, 0xE, 0xA, 0x5, 0x1, 0xD, 0x9]
MIX_r_x = [[0x0, 0x9, 0x1, 0x8, 0x2, 0xB, 0x3, 0xA, 0x4, 0xD, 0x5, 0xC, 0x6, 0xF, 0x7, 0xE],  # 9 2
           [0x0, 0x2, 0x4, 0x6, 0x8, 0xA, 0xC, 0xE, 0x3, 0x1, 0x7, 0x5, 0xB, 0x9, 0xF, 0xD]]

#初始向量
IV = random.randint(0, 2 ** 16)

# 密钥加,与密钥异或
def addRoundKey(state, kw):
    ls = [[hex(int(state[:4], 2) ^ (int(kw[:4], 2))), hex(int(state[8:12], 2) ^ (int(kw[8:12], 2)))],
          [hex(int(state[4:8], 2) ^ (int(kw[4:8], 2))), hex(int(state[12:16], 2) ^ (int(kw[12:16], 2)))]]
    # print("密钥加后:" + str(ls))
    return ls


# 半字节替代,根据传入的Matrix确定实现字节代替(或逆字节代替)
def subBytes(matrix, state):
    ls_r = [[hex(matrix[int(state[0][0], 16)]),
             hex(matrix[int(state[0][1], 16)])],
            [hex(matrix[int(state[1][0], 16)]),
             hex(matrix[int(state[1][1], 16)])]]
    # print("半字节替代后:" + str(ls_r))
    return ls_r


# 行移位
def shiftRows(state):
    # print("行移位状态:" + str(state))
    return [[state[0][0], state[0][1]],
            [state[1][1], state[1][0]]]


# 列混淆
def mixRow(state):
    ls = [[MIX_add[int(state[0][0], 16)][MIX_x[int(state[1][0], 16)]],
           MIX_add[int(state[0][1], 16)][MIX_x[int(state[1][1], 16)]]],
          [MIX_add[MIX_x[int(state[0][0], 16)]][int(state[1][0], 16)],
           MIX_add[MIX_x[int(state[0][1], 16)]][int(state[1][1], 16)]]]
    # print("列混淆后:" + str(ls))
    return bin(ls[0][0])[2:].rjust(4, '0') + \
           bin(ls[1][0])[2:].rjust(4, '0') + \
           bin(ls[0][1])[2:].rjust(4, '0') + \
           bin(ls[1][1])[2:].rjust(4, '0')


# 列混淆解密
def mixRow_r(state):
    return [[hex(MIX_add[MIX_r_x[0][int(state[0][0], 16)]][MIX_r_x[1][int(state[1][0], 16)]]),
             hex(MIX_add[MIX_r_x[0][int(state[0][1], 16)]][MIX_r_x[1][int(state[1][1], 16)]])],
            [hex(MIX_add[MIX_r_x[1][int(state[0][0], 16)]][MIX_r_x[0][int(state[1][0], 16)]]),
             hex(MIX_add[MIX_r_x[1][int(state[0][1], 16)]][MIX_r_x[0][int(state[1][1], 16)]])]]


# 密钥扩展
def keySprawl(key, rcon):
    # print("RCON:" + rcon)
    w_left = bin(int(key[:8], 2) ^ int(rcon, 2))[2:].rjust(8, '0')
    # print("密钥左半(异或):" + w_left)
    w_right = bin(int(key[8:16], 2) ^ int(rcon, 2))[2:].rjust(8, '0')
    # print("密钥右半(异或):" + w_right)
    w_right_l = bin(int(key, 2))[2:].rjust(16, '0')[12:16]
    w_right_r = bin(int(key, 2))[2:].rjust(16, '0')[8:12]
    new_w_l = bin(S_box[int(w_right_l, 2)])[2:].rjust(4, '0')
    new_w_r = bin(S_box[int(w_right_r, 2)])[2:].rjust(4, '0')
    new_w_right = new_w_l + new_w_r
    new_L = bin(int(w_left, 2) ^ int(new_w_right, 2))[2:].rjust(8, '0')
    # print("密钥新左半:" + new_L)
    new_R = bin(int(new_L, 2) ^ int(key[8:16], 2))[2:].rjust(8, '0')
    # print("密钥新右半:" + new_L)
    # print("新密钥:" + new_L + new_R)
    return new_L + new_R


# 加密
def Encry(plaintext, key):
    ciphertext_arr = []
    if re.search('^[01]+$', plaintext) is None:  # 判断字符串中是否只含0或1，trans返回文本array
        for i in range(len(trans_ASC(plaintext))):
            plaintext_asc = trans_ASC(plaintext)[i]
            # print("加密:")
            # 1 round
            state1 = mixRow(shiftRows(subBytes(S_box, addRoundKey(plaintext_asc, key))))
            # print(state1)
            state2 = addRoundKey(state1, keySprawl(key, RCON[0]))
            # print(state2)
            # 2 round
            cipherstate = shiftRows(subBytes(S_box, state2))
            # print(cipherstate)
            cipherstate = bin(int(cipherstate[0][0], 16))[2:].rjust(4, '0') + \
                          bin(int(cipherstate[1][0], 16))[2:].rjust(4, '0') + \
                          bin(int(cipherstate[0][1], 16))[2:].rjust(4, '0') + \
                          bin(int(cipherstate[1][1], 16))[2:].rjust(4, '0')

            # print("二轮加密后输出密文前:" + cipherstate)
            cipherstate = addRoundKey(cipherstate, keySprawl(keySprawl(key, RCON[0]), RCON[1]))
            ciphertext = bin(int(cipherstate[0][0], 16))[2:].rjust(4, '0') + \
                         bin(int(cipherstate[1][0], 16))[2:].rjust(4, '0') + \
                         bin(int(cipherstate[0][1], 16))[2:].rjust(4, '0') + \
                         bin(int(cipherstate[1][1], 16))[2:].rjust(4, '0')

            # print("输出密文:" + ciphertext)
            ciphertext_arr.append(ciphertext)
        return get_ASC(ciphertext_arr)

    elif re.search('^[01]+$', plaintext):
        # print("加密:")
        # 1 round
        state1 = mixRow(shiftRows(subBytes(S_box, addRoundKey(plaintext, key))))
        # print(state1)
        state2 = addRoundKey(state1, keySprawl(key, RCON[0]))
        # print(state2)
        # 2 round
        cipherstate = shiftRows(subBytes(S_box, state2))
        # print(cipherstate)
        cipherstate = bin(int(cipherstate[0][0], 16))[2:].rjust(4, '0') + \
                      bin(int(cipherstate[1][0], 16))[2:].rjust(4, '0') + \
                      bin(int(cipherstate[0][1], 16))[2:].rjust(4, '0') + \
                      bin(int(cipherstate[1][1], 16))[2:].rjust(4, '0')

        # print("二轮加密后输出密文前:" + cipherstate)
        cipherstate = addRoundKey(cipherstate, keySprawl(keySprawl(key, RCON[0]), RCON[1]))
        ciphertext = bin(int(cipherstate[0][0], 16))[2:].rjust(4, '0') + \
                     bin(int(cipherstate[1][0], 16))[2:].rjust(4, '0') + \
                     bin(int(cipherstate[0][1], 16))[2:].rjust(4, '0') + \
                     bin(int(cipherstate[1][1], 16))[2:].rjust(4, '0')

        # print("输出密文:" + ciphertext)
        return ciphertext


# 解密
def Decry(ciphertext, key):
    plaintext_arr = []
    if re.search('^[01]+$', ciphertext) is None:
        # print(len(trans_ASC(ciphertext)))
        for i in range(len(trans_ASC(ciphertext))):
            ciphertext_asc = trans_ASC(ciphertext)[i]
            print("解密:")
            # 1 round
            new_key = keySprawl(keySprawl(key, RCON[0]), RCON[1])
            state1 = subBytes(I_box, shiftRows(addRoundKey(ciphertext_asc, new_key)))
            stateText = bin(int(state1[0][0], 16))[2:].rjust(4, '0') + \
                        bin(int(state1[1][0], 16))[2:].rjust(4, '0') + \
                        bin(int(state1[0][1], 16))[2:].rjust(4, '0') + \
                        bin(int(state1[1][1], 16))[2:].rjust(4, '0')
            new_state = mixRow_r(addRoundKey(stateText, keySprawl(key, RCON[0])))
            # 2 round
            # print("逆行移位后:" + str(new_state))
            state2 = subBytes(I_box, shiftRows(new_state))
            stateText = bin(int(state2[0][0], 16))[2:].rjust(4, '0') + \
                        bin(int(state2[1][0], 16))[2:].rjust(4, '0') + \
                        bin(int(state2[0][1], 16))[2:].rjust(4, '0') + \
                        bin(int(state2[1][1], 16))[2:].rjust(4, '0')
            new_state = addRoundKey(stateText, key)
            plaintext = bin(int(new_state[0][0], 16))[2:].rjust(4, '0') + \
                        bin(int(new_state[1][0], 16))[2:].rjust(4, '0') + \
                        bin(int(new_state[0][1], 16))[2:].rjust(4, '0') + \
                        bin(int(new_state[1][1], 16))[2:].rjust(4, '0')
            # print("输出明文:" + plaintext)
            plaintext_arr.append(plaintext)
        return get_ASC(plaintext_arr)

    elif re.search('^[01]+$', ciphertext):
        # print("解密:")
        # 1 round
        new_key = keySprawl(keySprawl(key, RCON[0]), RCON[1])
        state1 = subBytes(I_box, shiftRows(addRoundKey(ciphertext, new_key)))
        stateText = bin(int(state1[0][0], 16))[2:].rjust(4, '0') + \
                    bin(int(state1[1][0], 16))[2:].rjust(4, '0') + \
                    bin(int(state1[0][1], 16))[2:].rjust(4, '0') + \
                    bin(int(state1[1][1], 16))[2:].rjust(4, '0')
        new_state = mixRow_r(addRoundKey(stateText, keySprawl(key, RCON[0])))
        # 2 round
        # print("逆行移位后:" + str(new_state))
        state2 = subBytes(I_box, shiftRows(new_state))
        stateText = bin(int(state2[0][0], 16))[2:].rjust(4, '0') + \
                    bin(int(state2[1][0], 16))[2:].rjust(4, '0') + \
                    bin(int(state2[0][1], 16))[2:].rjust(4, '0') + \
                    bin(int(state2[1][1], 16))[2:].rjust(4, '0')
        new_state = addRoundKey(stateText, key)
        plaintext = bin(int(new_state[0][0], 16))[2:].rjust(4, '0') + \
                    bin(int(new_state[1][0], 16))[2:].rjust(4, '0') + \
                    bin(int(new_state[0][1], 16))[2:].rjust(4, '0') + \
                    bin(int(new_state[1][1], 16))[2:].rjust(4, '0')
        # print("输出明文:" + plaintext)
        return plaintext


# 识别ascii码
def trans_ASC(text):
    cipher_letter = []
    i = 0
    text = (''.join(text)).split(' ')
    # text = text.split(' ')
    letter = []
    # 如果是字符则经此转换
    if re.search('^[a-zA-Z]+$', ''.join(text)):
        text = ''.join(text)
        for i in range(len(text)):
            letter.append(ord(text[i:i + 1]))
        for i in range(len(letter)):
            get_asc = bin(int(letter[i]))[2:].rjust(16, '0')
            # print(get_asc)
            cipher_letter.append(get_asc)

    if len(text) < 2 and re.search('^[a-zA-Z]+$', ''.join(text)) is None:
        get_asc = bin(int(text[0]))[2:].rjust(16, '0')
        # print(get_asc)
        cipher_letter.append(get_asc)

    elif len(text) >= 2 and re.search('^[a-zA-Z]+$', ''.join(text)) is None:
        for i in range(len(text)):
            # print(text)
            get_asc = bin(int(text[i]))[2:].rjust(16, '0')
            cipher_letter.append(get_asc)
            i = i + 1
    print("解ascii得到:" + str(cipher_letter))
    return cipher_letter


# 解ascii,输入text为arr
def get_ASC(text):
    i = 0
    str_out = ""
    x = ""
    for i in range(len(text)):
        if i < len(text) - 1:
            str_out = str_out + str(int(text[i], 2)) + " "
        elif i >= len(text) - 1:
            str_out = str_out + str(int(text[i], 2))
    print("输入文本得到的密文:" + str_out)
    return str_out

#多重加密
def aes_multiple_encry(plaintext, multiple_keys):
    print('多重加密：')
    count=int(len(multiple_keys)/16)
    print(f'count:{count}')
    keys={}
    for i in range(int(count)):
        keys[i]=multiple_keys[0+i*16:16+i*16]
    ciphertext=plaintext
    for i in range(int(count)):
        print(f'key:{keys[i]};i:{i};count:{count};ciphertext:{ciphertext}')
        ciphertext=Encry(ciphertext,keys[i])
        print(f'ciphertext:{ciphertext}')
    return ciphertext

#多重解密
def aes_multiple_decry(ciphertext,multiple_keys):
    print('多重解密:')
    count=len(multiple_keys)/16
    print(f'count:{count}')
    keys={}
    for i in range(int(count)):
        keys[i]=multiple_keys[0+i*16:16+i*16]
    plaintext=ciphertext
    for i in reversed(range(int(count))):
        print(f'key:{keys[i]};i:{i};count:{count}')
        plaintext=Decry(plaintext,keys[i])
        print(f'plaintext:{plaintext}')
    return plaintext

#CBC加密工作模式
def aes_CBC_encry(CBC_plaintexts, key):
    #初始化向量
    # IV= random.randint(0, 2**16)
    # IV=24358
    print(f'binIV:{bin(IV)[2:].zfill(16)}')
    #获取明文分组数
    count=int(len(CBC_plaintexts)/16)
    print(f'count:{count}')
    plaintexts={}
    for i in range(int(count)):
        plaintexts[i] = CBC_plaintexts[0 + i * 16:16 + i * 16]
        print(f'plaintexts[{i}]:{plaintexts[i]}')
    get_ciphertexts=''
    for i in range(int(count)):
        if i>0:
            #i>0将明文与前一个生成的密文异或后输出S-AES加密
            get_plaintext=int(plaintexts[i],2) ^ int(ciphertext,2)
            get_plaintext = bin(get_plaintext)[2:].zfill(16)
            print(f'getplaintext[{i}]:{get_plaintext}')
            ciphertext=Encry(get_plaintext, key)
            print(f'ciphertext[{i}]:{ciphertext}')
            get_ciphertexts += ciphertext
            print(f'getciphertexts:{get_ciphertexts};len:{len(get_ciphertexts)}')
        if i==0:
            #i=0将明文与初始向量异或后输入加密
            print(f'IVint:{IV};IVbin:{bin(IV)[2:].zfill(16)}')
            print(f'plaintext[0]int:{int(plaintexts[0],2)};plaintext[0]bin:{bin(int(plaintexts[0],2))[2:].zfill(16)}')
            get_plaintext=int(plaintexts[0],2) ^ int(IV)
            get_plaintext=bin(get_plaintext)[2:].zfill(16)
            print(f'getplaintext[{i}]:{get_plaintext}')
            ciphertext=Encry(get_plaintext, key)
            print(f'i=0；ciphertext[{i}]:{ciphertext}')
            get_ciphertexts += ciphertext
    return get_ciphertexts

#CBC解密工作模式
def aes_CBC_decry(CBC_ciphertexts, key):
    # 初始化向量
    # IV = random.randint(0, 2 ** 16)
    # IV=24358
    print(f'IVbin:{bin(IV)[2:].zfill(16)}')
    # 获取明文分组数
    count = int(len(CBC_ciphertexts) / 16)
    print(f'count:{count}')
    ciphertexts = {}
    get_plaintexts={}
    final_plaintexts=''
    for i in reversed(range(int(count))):
        ciphertexts[i] = CBC_ciphertexts[0 + i * 16:16 + i * 16]
        print(f'ciphertexts[{i}]:{ciphertexts[i]}')
    for i in reversed(range(int(count))):
        if i > 0:
            # i>0将明文与前一个生成的密文异或后输出S-AES加密
            # get_ciphertext = int(ciphertexts[i],2)
            # get_ciphertext = bin(get_ciphertext)[2:].zfill(16)
            # print(f'getciphertext[{i}]:{get_ciphertext}')
            plaintext = Decry(ciphertexts[i], key)
            print(f'plaintext[{i}]:{plaintext}')
            get_plaintexts[i]=int(plaintext,2)^int(ciphertexts[i-1],2)
            print(f'get_plaintext[{i}]:{bin(get_plaintexts[i])[2:].zfill(16)}')
        if i == 0:
            # i=0将明文与初始向量异或后输入加密
            get_ciphertext = int(ciphertexts[i],2)
            get_ciphertext = bin(get_ciphertext)[2:].zfill(16)
            print(f'getciphertext[{i}]:{get_ciphertext}')
            plaintext = Decry(get_ciphertext, key)
            print(f'plaintext[{i}]:{plaintext}')
            get_plaintexts[i]= int(IV)^ int(plaintext,2)
            print(f'i={i}；get_plaintexts[{i}]:{bin(get_plaintexts[i])[2:].zfill(16)}')
    for i in range(int(count)):
        final_plaintexts += bin(get_plaintexts[i])[2:].zfill(16)
    return final_plaintexts

#中间相遇攻击线程
def meet_in_middle_attack(section,plaintext,ciphertext):
    start_time=time.time()
    print(f'starttime:{start_time}')
    key_num = 0
    for key in range(0+section*(2**27), (2**27)+section*(2**27)):  # 遍历所有可能的密钥
        binary_key=bin(key)[2:].zfill(32)
        binary_key0=binary_key[0:16]
        binary_key1=binary_key[16:32]
        midtext_from_encry=Encry(plaintext,binary_key0)
        midtext_from_decry=Decry(ciphertext,binary_key1)
        if midtext_from_encry==midtext_from_decry:
            key_num+=1
            print(f'中间相遇攻击获取密钥:{binary_key}')
            print(f'midtext_from_encry:{midtext_from_encry}')
            print(f'midtextfromdecry:{midtext_from_decry}')
    end_time=time.time()
    print(f'endtime:{end_time}')
    print(f'破解总时长：{end_time-start_time}')
    return key_num
def scheduler(plaintext, ciphertext):
    # 设置线程数量
    num_threads = 32
    # 创建并启动线程
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=meet_in_middle_attack, args=(i, plaintext, ciphertext))
        thread.start()
        threads.append(thread)

    # 等待所有线程执行完毕
    for thread in threads:
        thread.join()

#中间相遇攻击线程2
def meet_in_middle_attack2(plaintext,ciphertext):
    key_num = 0
    for key1 in range(2**4):  # 遍历所有可能的密钥
        binary_key1 = bin(key1)[2:].zfill(12)+'0000'  # 转换为二进制字符串并添加前导零
        # print(f'key1:{binary_key1}')
        #得到经过key1加密的密文
        get_ciphertext=Encry(plaintext,binary_key1)
        for key2 in range(2**16):
            binary_key2 = bin(key2)[2:].zfill(16)  # 转换为二进制字符串并添加前导零
            # print(f'keys:{binary_key2}')
            #得到经过key2解密的明文
            get_plaintext=Decry(ciphertext,binary_key2)
            if get_plaintext == get_ciphertext:
                print(f'中间相遇攻击破解得到密钥：{binary_key1+(binary_key2)}')  # 找到正确的密钥
                key_num = key_num + 1
    return key_num

#中间相遇攻击线程3
def meet_in_middle_attack3(plaintext,ciphertext):
    key_num = 0
    for key1 in range(2**4):  # 遍历所有可能的密钥
        binary_key1 = bin(key1)[2:].zfill(8)+'00000000'  # 转换为二进制字符串并添加前导零
        # print(f'key1:{binary_key1}')
        #得到经过key1加密的密文
        get_ciphertext=Encry(plaintext,binary_key1)
        for key2 in range(2**16):
            binary_key2 = bin(key2)[2:].zfill(16)  # 转换为二进制字符串并添加前导零
            # print(f'keys:{binary_key2}')
            #得到经过key2解密的明文
            get_plaintext=Decry(ciphertext,binary_key2)
            if get_plaintext == get_ciphertext:
                print(f'中间相遇攻击破解得到密钥：{binary_key1+(binary_key2)}')  # 找到正确的密钥
                key_num = key_num + 1
    return key_num

#中间相遇攻击线程4
def meet_in_middle_attack4(section,plaintext,ciphertext):
    key_num = 0
    for key1 in range(2**16):  # 遍历所有可能的密钥
        binary_key1 = bin(key1)[2:].zfill(4)+'000000000000'  # 转换为二进制字符串并添加前导零
        # print(f'key1:{binary_key1}')
        #得到经过key1加密的密文
        get_ciphertext=Encry(plaintext,binary_key1)
        for key2 in range(2**16):
            binary_key2 = bin(key2)[2:].zfill(16)  # 转换为二进制字符串并添加前导零
            # print(f'keys:{binary_key2}')
            #得到经过key2解密的明文
            get_plaintext=Decry(ciphertext,binary_key2)
            if get_plaintext == get_ciphertext:
                print(f'中间相遇攻击破解得到密钥：{binary_key1+(binary_key2)}')  # 找到正确的密钥
                key_num = key_num + 1
    return key_num

#中间相遇攻击线程调度函数
def meet_in_middle_attack_scheduler(plaintext, ciphertext):
    #创建并启动进程
    thread1=threading.Thread(target=meet_in_middle_attack, args=(plaintext,ciphertext))
    thread2=threading.Thread(target=meet_in_middle_attack2, args=(plaintext,ciphertext))
    thread3=threading.Thread(target=meet_in_middle_attack3, args=(plaintext,ciphertext))
    thread4=threading.Thread(target=meet_in_middle_attack4, args=(plaintext,ciphertext))

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    #等待线程执行完毕
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()

# sample_pla = "blue"
# sample_key = "0010110101010101"
# sample_cipher = "11567 36131 4457 7465"

#print(Encry(sample_pla, sample_key))
#print(Decry(sample_cipher, sample_key))
