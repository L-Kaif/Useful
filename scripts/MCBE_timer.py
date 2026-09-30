import pymem
from pymem.process import module_from_name

PROCESS_NAME = "Minecraft.Windows.exe"
BASE_OFFSET_HEX = "0x0907BF28"
OFFSETS_HEX = ["0x0", "0x2E8", "0x410", "0x8", "0x70", "0x38", "0x130"]

def hex_list_to_ints(hex_list):
    return [int(x, 16) for x in hex_list]

def follow_pointer_chain_and_read_float(pm, module_name, base_offset, offsets):
    module = module_from_name(pm.process_handle, module_name)
    base_addr = module.lpBaseOfDll + base_offset


    read_ptr = pm.read_ulonglong(base_addr)

    addr = base_addr
    try:
        for off in offsets[:-1]:
            addr = read_ptr(addr + off)
            if not addr:
                raise RuntimeError(f"Null/invalid pointer encountered at offset {hex(off)}")
        final_addr = addr + offsets[-1]
        value = pm.read_float(final_addr)
        return final_addr, value
    except Exception as e:
        raise

if __name__ == "__main__":
    pm = pymem.Pymem(PROCESS_NAME)
    offsets = hex_list_to_ints(OFFSETS_HEX)
    base_off = int(BASE_OFFSET_HEX, 16)

    try:
        final_address, float_value = follow_pointer_chain_and_read_float(
            pm, PROCESS_NAME, base_off, offsets
        )
        print(f"Final address: 0x{final_address:016X}")
        print(f"Float value: {float_value}")
    except Exception as e:
        print("Error following pointer chain:", e)
