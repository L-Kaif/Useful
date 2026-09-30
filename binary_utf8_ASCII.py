binary = input('Enter Binary: ')

print("Number of bits:", len(binary))
print("Complete bytes:", len(binary) // 8)
print("Extra bits:", len(binary) % 8)

if len(binary) % 8 == 0:
    data = bytes(
        int(binary[i:i + 8], 2)
        for i in range(0, len(binary), 8)
    )

    print("Hex:", data.hex())
    print("Decoded:", data.decode("utf-8"))
else:
    print("Cannot cleanly decode: incomplete byte(s).")
    print("Last bits:", binary[-(len(binary) % 8):])