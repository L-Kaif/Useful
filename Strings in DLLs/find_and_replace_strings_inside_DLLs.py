
from pathlib import Path
import shutil

DLL_PATH = Path("DLLs/your_dll.dll")                # Path to the DLL file


# Enter the strings to search for
# Example:
# SEARCH_STRINGS = [
#     "string_1",
#     "interim_loser",
#     "abcdefgh"
# ]

SEARCH_STRINGS = [
    
]

ENCODINGS = [
    ("ASCII", "ascii"),
    ("UTF-8", "utf-8"),
    ("UTF-16 LE", "utf-16-le"),
]


def find_matches(data, text):
    matches = []

    for label, encoding in ENCODINGS:
        pattern = text.encode(encoding)
        start = 0

        while True:
            pos = data.find(pattern, start)

            if pos == -1:
                break

            matches.append({
                "offset": pos,
                "encoding": encoding,
                "label": label,
                "length": len(pattern),
                "pattern": pattern
            })

            start = pos + len(pattern)

    # Remove duplicate matches
    unique = {}

    for match in matches:
        unique[(match["offset"], match["length"])] = match

    return sorted(unique.values(), key=lambda m: m["offset"])



def replace_all(data, matches, replacement):
    if not matches:
        return 0

    # Group matches by their original byte length and encoding.
    groups = {}

    for match in matches:
        key = (match["encoding"], match["length"])
        groups.setdefault(key, []).append(match)

    total = 0

    for (encoding, old_length), group in groups.items():
        new_pattern = replacement.encode(encoding)

        if len(new_pattern) > old_length:
            print(
                f"[REJECTED] {encoding}: replacement needs "
                f"{len(new_pattern)} bytes, but only "
                f"{old_length} bytes are available."
            )
            continue

        replacement_bytes = (
            new_pattern +
            b"\x00" * (old_length - len(new_pattern))
        )

        for match in reversed(group):
            start = match["offset"]
            end = start + old_length

            data[start:end] = replacement_bytes
            total += 1

    return total



def main():
    if not DLL_PATH.is_file():
        print(f"[ERROR] DLL not found: {DLL_PATH}")
        return

    backup = DLL_PATH.with_suffix(".dll.bak")

    if not backup.exists():
        shutil.copy2(DLL_PATH, backup)
        print(f"[BACKUP] {backup}")
    else:
        print(f"[INFO] Existing backup: {backup}")

    data = bytearray(DLL_PATH.read_bytes())
    original_size = len(data)

    print(f"\nScanning: {DLL_PATH}")
    print(f"Size: {original_size:,} bytes")

    total_replaced = 0

    for text in SEARCH_STRINGS:
        matches = find_matches(data, text)

        if not matches:
            print(f"\n[NOT FOUND] {text}")
            continue

        print(f"\n[FOUND] {text}")
        print(f"Occurrences: {len(matches)}")
        print(f"Encoding: {matches[0]['label']}")

        for match in matches:
            print(f"    Offset: 0x{match['offset']:X}")

        replacement = input("\nReplace ALL occurrences with (ENTER to skip): ")

        if not replacement:
            print("[SKIPPED]")
            continue

        try:
            count = replace_all(data, matches, replacement)

            if count:
                print(f"[SUCCESS] Replaced {count} occurrence(s).")
                total_replaced += count

        except UnicodeEncodeError:
            print("[ERROR] Incompatible replacement encoding.")

    print("\n" + "=" * 50)
    print(f"Total replacements: {total_replaced}")

    if len(data) != original_size:
        print("[ERROR] DLL size changed. Aborting.")
        return

    if total_replaced == 0:
        print("[INFO] Nothing was replaced.")
        return

    confirm = input("\nSave modified DLL? (y/n): ")

    if confirm.lower() == "y":
        DLL_PATH.write_bytes(data)
        print("[SAVED] DLL modified successfully.")
    else:
        print("[CANCELLED] No changes saved.")


if __name__ == "__main__":
    main()
