from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join
import time
import hashlib


class Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)
        

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".aes", 'wb') as fo:
            fo.write(enc)
        #os.remove(file_name)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open("dec"+file_name[:-4], 'wb') as fo:
            fo.write(dec)
        

    # def getAllFiles(self):
    #     dir_path = os.path.dirname(os.path.realpath(__file__))
    #     dirs = []
    #     for dirName, subdirList, fileList in os.walk(dir_path):
    #         for fname in fileList:
    #             if (fname != 'aes.py'):
    #                 dirs.append(dirName + "/" + fname)
    #     return dirs

    # def encrypt_all_files(self):
    #     dirs = self.getAllFiles()
    #     for file_name in dirs:
    #         self.encrypt_file(file_name)

    # def decrypt_all_files(self):
    #     dirs = self.getAllFiles()
    #     for file_name in dirs:
    #         self.decrypt_file(file_name)
                       
def key_generator(password):
    password = password.encode()
    key = hashlib.sha256(password).digest()
    enc= Encryptor(key)
    return enc
    

while True:
    choice = int(input(
            "1. Press '1' to encrypt file.\n2. Press '2' to decrypt file.\n3. Press '3' to exit.\n"))
    
    if choice == 1:
        password = input("Enter the password to encrypt the file. Remember the password as the same should be used to decrypt this file: ")
        enc = key_generator(password)
        enc.encrypt_file(str(input("Enter name of file to encrypt: ")))
    elif choice == 2:
        password = input("Enter the password to decrypt the file: ")
        enc = key_generator(password)
        enc.decrypt_file(str(input("Enter name of file to decrypt: ")))    
    elif choice == 3:
        exit()
    else:
        print("Please select a valid option!")

#key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
#key = b'K{\xb8\xc3\x01\x06[\xe3\x8e\xbe\xd6N\xd1\xe8^N\xf6\xf6\xa0b\x10\xb6\xc2\x9a\xbcY\x19a\x98\x19\xb7\xc0'
#enc = Encryptor(key)
#clear = lambda: os.system('cls')

#if os.path.isfile('data.txt.enc'):
    #while True:
        #password = str(input("Enter password: "))
        #enc.decrypt_file("data.txt.enc")
        #p = ''
        #with open("data.txt", "r") as f:
            #p = f.readlines()
        #if p[0] == password:
            #enc.encrypt_file("data.txt")
            #break

    #while True:
        #clear()
        #choice = int(input(
            #"1. Press '1' to encrypt file.\n2. Press '2' to decrypt file.\n3. Press '3' to Encrypt all files in the directory.\n4. Press '4' to decrypt all files in the directory.\n5. Press '5' to exit.\n"))
        #clear()
        #if choice == 1:
            #enc.encrypt_file(str(input("Enter name of file to encrypt: ")))
        #elif choice == 2:
            #enc.decrypt_file(str(input("Enter name of file to decrypt: ")))
        #elif choice == 3:
            #enc.encrypt_all_files()
        #elif choice == 4:
            #enc.decrypt_all_files()
        #elif choice == 5:
            #exit()
        #else:
            #print("Please select a valid option!")

#else:
    #while True:
        #clear()
        #password = str(input("Setting up stuff. Enter a password that will be used for decryption: "))
        #repassword = str(input("Confirm password: "))
        #if password == repassword:
            #break
        #else:
            #print("Passwords Mismatched!")
    #f = open("data.txt", "w+")
    #f.write(password)
    #f.close()
    #enc.encrypt_file("data.txt")
    #print("Please restart the program to complete the setup")
    #time.sleep(2)
