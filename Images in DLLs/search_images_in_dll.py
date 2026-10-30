import os
import struct

dll_path = "dll_u_want_to_modify.dll"                  # path to the dll u want to modify

with open(dll_path, "rb") as f:
    data = f.read()

PNG_SIGNATURE = bytes.fromhex("89 50 4E 47 0D 0A 1A 0A")           # replace if u want jpg, jpeg, etc...

# Automatically find PNG offsets
offsets = []
start = 0

while True:
    position = data.find(PNG_SIGNATURE, start)

    if position == -1:
        break

    offsets.append(position)
    start = position + 1

print("File size:", len(data))
print("PNG signatures found:", len(offsets))

# Create images folder beside the DLL
output_dir = os.path.join(
    os.path.dirname(os.path.abspath(dll_path)),
    "images"
)

os.makedirs(output_dir, exist_ok=True)

# Extract PNG images using discovered offsets
for image_number, offset in enumerate(offsets, 1):

    pos = offset + 8

    while pos + 12 <= len(data):
        chunk_length = struct.unpack(">I", data[pos:pos + 4])[0]
        chunk_type = data[pos + 4:pos + 8]

        chunk_end = pos + 12 + chunk_length

        if chunk_end > len(data):
            break

        pos = chunk_end

        if chunk_type == b"IEND":
            break

    # Validate PNG completion
    if pos > len(data) or data[pos - 8:pos - 4] != b"IEND":
        print(f"Image {image_number}: Incomplete PNG at offset {offset}")
        continue

    image_data = data[offset:pos]

    filename = os.path.join(
        output_dir,
        f"image_{image_number}.png"
    )

    with open(filename, "wb") as img:
        img.write(image_data)

    print(
        f"Extracted: image_{image_number}.png "
        f"({len(image_data)} bytes) - Offset {offset}"
    )

print("\nExtraction finished.")
print("Output folder:", output_dir)
