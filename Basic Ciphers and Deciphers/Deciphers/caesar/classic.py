from Ciphers.caesar import classic

def caesar_decipher(text, shift):
    print(classic.caesar_cipher(text, -shift))