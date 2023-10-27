# Cryptology S-AES
# User Guide
## Overview
S-AES (Simplified Advanced Encryption Standard) is a simplified version of the Advanced Encryption Standard (AES). It is a symmetric encryption algorithm used for ensuring the confidentiality and security of data.
S-AES operates on 128-bit keys and 16-bit plaintext blocks for encryption and decryption. The encryption process involves four main steps: key expansion, round key generation, byte substitution and shift rows, and column mixing. The decryption process is the inverse of the encryption process.
### Key-Expansion
During the key expansion phase, S-AES generates 10 round keys from the initial key, each consisting of 128 bits. These round keys are used in subsequent encryption and decryption operations.
### Byte-sustitution and shift rows 
In the byte substitution and shift rows phase, S-AES performs byte substitution using a substitution box (S-box) and shifts the rows of the state. These operations enhance the complexity and security of the encryption algorithm.
### Column-mixing
In the column mixing phase, S-AES applies a fixed matrix to mix the columns of the state. This matrix is XORed with the round key, further increasing the strength of the encryption algorithm.

## Environment and Configuration
IDE: Pycharm 2023.2
Environment configuration: python3

## Running

### Encryption
Run app.py file, terminal input:
```python
#加密过程
python app.py 
```
#### Key Generation
keep the length of plaintext 16 bit while encription or keep the length of ciphertext 16 bit while decription
generate a 16 bit binary key for basic-encry/decry, or choose a more than 16 bit binary key (eg: 32bit key for dual-encry/decry，48 bit binary key for triple-encry/decry and so on) for multiple-encry
sample code:
```python
plaintext='1010101010101010'
(ciphertext='0000110100111010')
#basic-encry/decry
key='0110010010101001'
#multiple-encry/decry
key='0110010010101001111111111111111'                   #dual-encry/decry
key='01100100101010011111111111111110000000000000000'   #triple-encry/decry
```
#### Plaintext Input
input a plaintext to suppose this encrypt program, you can choose ASCII、string or binary string to input. As for binary string input, keep the length of ciphertext 16 bit while encription, you can choose a 16 bit binary-string or more than 16 bit binary-string (eg: k*16 bit for CBC_encry where k is a positive integer) 
example:
```python
key='1111111111111111'
#basic-encry
plaintext='1010101010101010'
plaintext='blue'
plaintext='120 236 29 29 153' #using space to seperate each letter's ASCII encode
#CBC_encry
plaintext='10101010101010101010101010101010'
```

### Decryption 
Run app.py file, terminal input:
```python
'#解密过程'
'python app.py'
```

##### Ciphertext Input
input a ciphertext to suppose this encrypt program, you can choose ASCII、string or binary string to input as well. As for binary string input, keep the length of ciphertext 16 bit while encription, you can choose a 16 bit binary-string or more than 16 bit binary-string (eg: k*16 bit for CBC_encry where k is a positive integer) 
example:
```python
#basic-decry
ciphertext='0110110000111001'
ciphertext='string'
ciphertext='26 204 191 191 9'  #using space to seperate each letter's ASCII encode
#CBC_decry
ciphertext='1101011010011100100111011011100'
```

### Matters Need Attention
the length of input will lead to entirely different result
for the input and output format of plaintext and ciphertext, please read the **running** part

### Example Application
#### Encryption
```python
'#Input'
'Plaintext String: 1010101010101010'
'Key String: 1111111111111111'
click the 'Encrypt' button
#output
'Returned Message: Encrypt successfully! The ciphertext is:0111010110010110'
```

#### Decryption
```python
'#Input'
'Ciphertext String: 0111010110010110'
'Key String: 1111111111111111'
click the 'Decrypt' button
'#output'
'Returned Message: Decrypt successfully! The plaintext is:1010101010101010'
```

### Extended Usage
For dual-encry/decry, we design a function called meet_in_mid_attack(plaintext,ciphertext) to acquire the key in the situation of just knowing a set of plaintext and ciphertext.The method we use is meet in middle attack method
you can run this function by running the main.py file, terminal input:
```python
'python attack.py'
```
Then, input a plaintext and a ciphertext one by one and you'll get the key you want. In fact, you can find that there are always more than one key returned. The account of key is generally of great deal so we choose to display just a part of result below:
sample code:
```python
'#meet in middle attack'
'python attack.py'
'please input the plaintext: 1101011010101010'
'please input the ciphertext: 0001110110000010'
'# suitable key:'
starttime:1698032775.7515764
中间相遇攻击获取密钥:0010000000000000000101001110001
mid_text_from_encry:11101100000011
midtextfromdecry:1111011000000011
...
```

### Reference Files
[More details for S-AES](https://terenceli.github.io/%E6%8A%80%E6%9C%AF/2014/04/17/SDES)  
[Test result please click here to download]([https://github.com/semygloss/cryptology/blob/main/The%20Alpha%20group%20test1-5.docx](https://github.com/semygloss/S-AES/blob/main/Source-new/S-AES%E6%B5%8B%E8%AF%95%E7%BB%93%E6%9E%9C.docx)https://github.com/semygloss/S-AES/blob/main/Source-new/S-AES%E6%B5%8B%E8%AF%95%E7%BB%93%E6%9E%9C.docx)  
[More details for boxes]()
