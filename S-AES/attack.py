from s_ase import meet_in_middle_attack_scheduler, scheduler, meet_in_middle_attack, aes_CBC_encry

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    plaintext=input('Please input the plaintext: ')
    # key=input('Please input the key:')
    # ciphertext=aes_CBC_encry(plaintext,key)
    ciphertext=input('please input the ciphertext: ')
    scheduler(plaintext, ciphertext)
    #ciphertext = '255 95 175'
    # key_number=meet_in_middle_attack(plaintext,ciphertext)
    print('The number of main key:')
    # print(key_number)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
