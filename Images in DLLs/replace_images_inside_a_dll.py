
import struct
from pathlib import Path
from io import BytesIO
from PIL import Image

DLL = Path("dll_u_want_to_modify.dll")                          # path to the dll u want to modify
REPLACE = Path("replacewith")               # folder containing images you want to replace the originals with
OUTPUT = Path("DLLs")                       # folder where the modified DLL will go to


# run search_images_in_dll.py to get the offsets.
# Example:
# TARGETS = {
#     "image_1.png": 3668640,
#     "image_7.png": 5746944,
#     "image_6.png": 3854864,
# }

TARGETS = {

}

SIGNATURE = b"\x89PNG\r\n\x1a\n"   # .png sig


def png_end(data, offset=0):
    if data[offset:offset + 8] != SIGNATURE:
        raise ValueError(f"Invalid PNG at offset {offset}")

    pos = offset + 8

    while pos + 12 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        chunk = data[pos + 4:pos + 8]
        end = pos + 12 + length

        if end > len(data):
            raise ValueError("Incomplete PNG")

        pos = end

        if chunk == b"IEND":
            return pos

    raise ValueError("PNG ending not found")


# Compress the images to fit into the region.
# It may ovverwrite or break the entire DLL if u can't fit.
# WARNING: This may make your image look worse


def optimize_png(path, max_size):
    image = Image.open(path).convert("RGBA")

    # Try palette-based PNG compression first.
    for scale in [1.0, 0.9, 0.8, 0.7, 0.6,
                  0.5, 0.4, 0.3, 0.2]:

        width = max(1, int(image.width * scale))
        height = max(1, int(image.height * scale))

        resized = image.resize(
            (width, height),
            Image.Resampling.LANCZOS
        )

        for colors in [256, 128, 64, 32, 16]:
            palette = resized.convert("RGB").quantize(
                colors=colors,
                method=Image.Quantize.MEDIANCUT
            )

            output = BytesIO()
            palette.save(output, format="PNG", optimize=True)
            result = output.getvalue()
            if len(result) <= max_size:
                print(
                    f"Optimized {path.name}: "
                    f"{width}x{height}, {len(result)} bytes"
                )
                return result
    raise ValueError(
        f"Could not fit {path.name} into {max_size} bytes."
    )


# Read original DLL
data = bytearray(DLL.read_bytes())

patches = []

# Validate and prepare all replacements
for filename, offset in TARGETS.items():

    original_end = png_end(data, offset)
    available = original_end - offset

    replacement_path = REPLACE / filename

    if not replacement_path.exists():
        raise FileNotFoundError(replacement_path)

    replacement = optimize_png(
        replacement_path,
        available
    )

    patches.append((offset, original_end, replacement))

# Apply patches only after all replacements pass validation
for offset, end, replacement in patches:

    data[offset:end] = (
        replacement + b"\x00" * (end - offset - len(replacement))
    )

# Save modified DLL
OUTPUT.mkdir(exist_ok=True)

output_path = OUTPUT / "Nyx_modified.dll"
output_path.write_bytes(data)

print("\nReplacement completed.")
print("Saved to:", output_path.resolve())
print("Original DLL unchanged.")
