from Ciphers.caesar import classic

def brute_force_caesar(text):
    for shift in range(26):
        print(f"Shift {shift:2}: {classic.caesar_cipher(text, -shift)}")
