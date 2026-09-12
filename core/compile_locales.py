"""
Pure-Python GNU gettext MO compiler.
Converts .po files in locale/ to valid binary .mo files without requiring msgfmt.exe.
Conforms strictly to GNU gettext binary file specifications.
"""
import os
import re
import struct
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOCALE_DIR = BASE_DIR / "locale"

DEFAULT_PO_HEADER = "Content-Type: text/plain; charset=UTF-8\nContent-Transfer-Encoding: 8bit\n"


def parse_po(po_filepath):
    """
    Parses a .po file into a dictionary of {msgid: msgstr}.
    Handles multi-line strings, escaped characters, and headers.
    """
    with open(po_filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    messages = {}
    
    # Use regex to extract all msgid and msgstr pairs
    # Matches: msgid "..." (optional "..." lines) followed by msgstr "..." (optional "..." lines)
    entry_pattern = re.compile(
        r'msgid\s+((?:"(?:\\.|[^"\\])*"\s*)+)\s*msgstr\s+((?:"(?:\\.|[^"\\])*"\s*)+)',
        re.MULTILINE
    )

    def extract_str_literal(raw_block):
        # Find all quoted strings and unescape them
        matches = re.findall(r'"((?:\\.|[^"\\])*)"', raw_block)
        joined = "".join(matches)
        # Unescape standard gettext escapes
        joined = (
            joined.replace('\\"', '"')
            .replace('\\n', '\n')
            .replace('\\r', '\r')
            .replace('\\t', '\t')
            .replace('\\\\', '\\')
        )
        return joined

    for match in entry_pattern.finditer(content):
        raw_msgid, raw_msgstr = match.groups()
        msgid = extract_str_literal(raw_msgid)
        msgstr = extract_str_literal(raw_msgstr)
        messages[msgid] = msgstr

    # Enforce valid UTF-8 header
    header_val = messages.get("", "")
    if "charset=" not in header_val:
        messages[""] = DEFAULT_PO_HEADER
    elif not header_val.endswith("\n"):
        messages[""] = header_val + "\n"

    return messages


def build_mo(messages):
    """
    Encodes messages {msgid: msgstr} into GNU gettext binary format (.mo).
    """
    # Enforce header presence
    if "" not in messages or "charset=" not in messages[""]:
        messages[""] = DEFAULT_PO_HEADER

    keys = sorted(messages.keys())
    num_strings = len(keys)

    orig_table_offset = 28
    trans_table_offset = orig_table_offset + 8 * num_strings
    data_offset = trans_table_offset + 8 * num_strings

    orig_data = bytearray()
    trans_data = bytearray()
    orig_table = []
    trans_table = []

    cur_orig_offset = data_offset
    for k in keys:
        b_k = k.encode("utf-8")
        orig_table.append((len(b_k), cur_orig_offset))
        orig_data.extend(b_k + b"\x00")
        cur_orig_offset += len(b_k) + 1

    cur_trans_offset = cur_orig_offset
    for k in keys:
        v = messages[k]
        b_v = v.encode("utf-8")
        trans_table.append((len(b_v), cur_trans_offset))
        trans_data.extend(b_v + b"\x00")
        cur_trans_offset += len(b_v) + 1

    # Header: magic, revision, num_strings, orig_table_offset, trans_table_offset, hash_size, hash_offset
    header = struct.pack(
        "<Iiiiiii",
        0x950412de,  # Magic number
        0,           # Format revision
        num_strings,
        orig_table_offset,
        trans_table_offset,
        0,           # Hash table size
        0,           # Hash table offset
    )

    orig_table_bytes = bytearray()
    for length, offset in orig_table:
        orig_table_bytes.extend(struct.pack("<ii", length, offset))

    trans_table_bytes = bytearray()
    for length, offset in trans_table:
        trans_table_bytes.extend(struct.pack("<ii", length, offset))

    return bytes(header + orig_table_bytes + trans_table_bytes + orig_data + trans_data)


def compile_all_locales(locale_dir=None):
    """
    Finds all .po files in locale_dir and compiles them to .mo files.
    """
    if locale_dir is None:
        locale_dir = LOCALE_DIR

    compiled = []
    for root, dirs, files in os.walk(locale_dir):
        for f in files:
            if f.endswith(".po"):
                po_path = Path(root) / f
                mo_path = po_path.with_suffix(".mo")
                messages = parse_po(po_path)
                mo_bytes = build_mo(messages)
                with open(mo_path, "wb") as out:
                    out.write(mo_bytes)
                compiled.append((po_path, mo_path, len(messages)))
                print(f"[OK] Compiled {po_path.name} -> {mo_path.name} ({len(messages)} messages)")
    return compiled


if __name__ == "__main__":
    compile_all_locales()
