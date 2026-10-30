## How to Use

### Steps

1. Copy the DLL to the root directory.
2. Run `search_images_in_dll.py` after changing the value of **`dll_path`**.
2. Add the images you to want the originals to be replaced with their corresponding position names to `replacewith/` folder
3. Run `replace_images_inside_a_dll.py` after changing the values of  **`DLL`** and **`TARGET`**.

---

### What do they do?

- `search_images_in_dll.py` → Searches for all raw images inside a DLL, copies them to the `images/` folder, and prints their offsets.
- `replace_images_inside_a_dll.py` → Replaces the images inside the DLL. (Use the offsets from running `search_images_in_dll.py`.)

---

### Precautions:
- The images inside `replacewith/` folder should'nt be uncompressible (**use .png**).
- Otherwise ... *bad stuff* will happen.


### Disclaimer:
- **Won't work if the images are encrytped inside the DLL**