from PIL import Image
import math
import re

PIXEL_SIZE = 10       # Size of each 0/1 square in pixels
COLUMNS = 64          # Bits per row
BACKGROUND = 255      # White
BLACK = 0             # Black


# Encoder: 
def encode_binary(binary, output_file=None):
    """
    Converts binary into an image.

    0 = black
    1 = white

    The original size is stored in the filename.
    """

    bits = "".join(binary.split())

    if not bits:
        raise ValueError("Binary string is empty.")

    if any(bit not in "01" for bit in bits):
        raise ValueError("Input must contain only 0 and 1.")

    original_length = len(bits)
    rows = math.ceil(original_length / COLUMNS)
    padded_bits = bits.ljust(rows * COLUMNS, "1")

    # Create image
    width = COLUMNS * PIXEL_SIZE
    height = rows * PIXEL_SIZE

    img = Image.new("L", (width, height), BACKGROUND)
    pixels = img.load()

    for i, bit in enumerate(padded_bits):

        x = (i % COLUMNS) * PIXEL_SIZE
        y = (i // COLUMNS) * PIXEL_SIZE

        # 0 = black
        # 1 = white
        value = BLACK if bit == "0" else BACKGROUND

        for py in range(y, y + PIXEL_SIZE):
            for px in range(x, x + PIXEL_SIZE):
                pixels[px, py] = value

    if output_file is None:
        output_file = f"binary_{original_length}.png"

    img.save(output_file)

    print()
    print("-ENCODE-")
    print(f"Bits:       {original_length}")
    print(f"Columns:    {COLUMNS}")
    print(f"Rows:       {rows}")
    print(f"Image size: {width} x {height}")
    print(f"Saved as:   {output_file}")

    return output_file


# Deocde: 
def decode_image(image_file):
    """
    Converts an encoded image back into binary.

    The original number of bits is read from the filename.
    """

    filename = image_file.split("/")[-1]

    numbers = re.findall(r"\d+", filename)

    if not numbers:
        raise ValueError(
            "Could not find the original bit count in the filename."
        )

    original_length = int(numbers[-1])

    img = Image.open(image_file).convert("L")

    width, height = img.size

    # Check dimensions
    if width % PIXEL_SIZE != 0:
        raise ValueError("Image width is not compatible with PIXEL_SIZE.")

    if height % PIXEL_SIZE != 0:
        raise ValueError("Image height is not compatible with PIXEL_SIZE.")

    image_columns = width // PIXEL_SIZE
    image_rows = height // PIXEL_SIZE

    if image_columns != COLUMNS:
        raise ValueError(
            f"Wrong image format. Expected {COLUMNS} columns, "
            f"but image has {image_columns}."
        )

    # Make sure the image is large enough
    total_bits = image_columns * image_rows

    if original_length > total_bits:
        raise ValueError(
            "Filename says the image contains more bits than it actually does."
        )

    pixels = img.load()

    bits = []

    # Read each square
    for row in range(image_rows):

        for column in range(image_columns):

            # Read the center of the square
            x = column * PIXEL_SIZE + PIXEL_SIZE // 2
            y = row * PIXEL_SIZE + PIXEL_SIZE // 2

            pixel = pixels[x, y]

            # Black = 0
            # White = 1
            if pixel < 128:
                bits.append("0")
            else:
                bits.append("1")

    # Remove Padding
    bits = "".join(bits)

    original_bits = bits[:original_length]

    print()
    print("=Decode-")
    print(f"Bits recovered: {len(original_bits)}")
    print(f"Source image:   {image_file}")

    return original_bits



if __name__ == "__main__":

    print("1. Encode binary -> image")
    print("2. Decode image -> binary")
    print()

    choice = input("Choose 1 or 2: ").strip()

    # Encode: 
    if choice == "1":

        print()
        print("Paste your binary.")
        print("Spaces and newlines are allowed.")
        print()

        binary = input("Binary: ")

        encode_binary(binary)

    # Decode:
    elif choice == "2":

        print()
        image_file = input("Image filename: ").strip()

        try:
            recovered = decode_image(image_file)

            print()
            print("Recovered binary:")
            print(recovered)

        except Exception as error:
            print()
            print("ERROR:")
            print(error)

    else:
        print("Invalid choice.")
