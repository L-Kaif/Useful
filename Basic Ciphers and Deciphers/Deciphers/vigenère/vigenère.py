def vigenere_decipher(text, key):
    result = ""
    key_index = 0
    key = key.lower()
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            key_char = key[key_index % len(key)]
            shift = -(ord(key_char) - ord('a'))
            shifted = (ord(char) - base + shift) % 26 + base
            result += chr(shifted)
            key_index += 1
        else:
            result += char
    return result