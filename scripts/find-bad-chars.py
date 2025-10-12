# -*- coding: utf-8 -*-
"""
!py find-bad-chars.py --address esp+1 --start 00 --end 7f --bad 00 01 0A 0D 25 26 2B
(...)
[+] bad bytes (hex):
00 01 0A 0D 25 26 2B 3D
"""
from __future__ import print_function
import pykd
import argparse

def hex_byte(byte_str):
    """validate user input is a hex representation of an int between 0 and 255 inclusive"""
    if byte_str == "??":
        # windbg shows ?? when it can't access a memory region, but we shouldn't stop execution
        return byte_str

    try:
        val = int(byte_str, 16)
        if 0 <= val <= 255:
            return val
        else:
            raise ValueError
    except ValueError:
        raise argparse.ArgumentTypeError(
            "only *hex* bytes between 00 and ff are valid, found {0}".format(byte_str)
        )


class Memdump(object):
    def __init__(self, line):
        self.__bytes = list()
        self.__address = ""
        self._parse_line(line)

    @property
    def bytes(self):
        return self.__bytes

    @bytes.setter
    def bytes(self, val):
        # val is expected to be a space-separated string of hex byte tokens (or '??')
        self.__bytes = [hex_byte(x) for x in val.split()]

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, val):
        self.__address = val

    def _parse_line(self, line):
        # Example input format:
        # 0185ff54  99 77 9e 77 77 c9 03 8c-60 77 9e 77 60 77 9e 77  .wžwwÉ.Œ`wžw`wžw
        parts = line.split("  ")[:2]  # discard the ascii portion right away

        if len(parts) == 0:
            return

        self.address = parts[0]
        bytes_str = ""

        for i, byte in enumerate(parts[1].split()):
            if i == 7:
                # handle the hyphen separator between the 8th and 9th byte
                bytes_str += " ".join(byte.split("-")) + " "
                continue
            bytes_str += "{0} ".format(byte)

        # pass to the setter as a space separated string of hex bytes for further processing/assignment
        self.bytes = bytes_str

    def __str__(self):
        byte_str = ""
        for byte in self.bytes:
            if byte == "??":
                byte_str += "{0} ".format(byte)
            else:
                byte_str += "%02X " % byte

        return "{0}  {1}".format(self.address, byte_str)


def find_bad_chars(args):
    # canonical list of known bad bytes (filtered to the requested range)
    known_bad = sorted(x for x in args.bad if args.start <= x <= args.end)

    # chars is the sequence we will request from memory: all bytes in the range except known_bad
    chars = [i for i in range(args.start, args.end + 1) if i not in known_bad]

    # if there is nothing to request (e.g. user excluded entire range), exit
    if not chars:
        print("[!] No bytes to check (all bytes in range are marked as known-bad).")
        return

    # request memory for the number of bytes we expect (chars length)
    command = "db {0} L 0n{1}".format(args.address, len(chars))
    result = pykd.dbgCommand(command)

    if result is None:
        print("[!] Ran '{0}', but received no output; exiting...".format(command))
        raise SystemExit

    # flatten parsed memdump bytes into a list in order
    observed = []
    # We will also keep the formatted memdump lines for pretty-printing (optional)
    memdump_lines = []

    for line in result.splitlines():
        memdump = Memdump(line)
        memdump_lines.append(memdump)
        observed.extend(memdump.bytes)

    # observed should have at least len(chars) items; if it has more, truncate; if less, pad with '??'
    if len(observed) < len(chars):
        # pad unreadable/missing bytes
        observed.extend(['??'] * (len(chars) - len(observed)))
    elif len(observed) > len(chars):
        observed = observed[:len(chars)]

    # Now iterate in order and detect the first unexpected bad byte(s)
    discovered_bad = []  # will hold newly discovered bad bytes (not the pre-known ones)
    # Start with known bads (to report them first as you requested)
    reported_bad = list(known_bad)

    stop_at_first_unexpected = True

    # iterate through expected chars and observed bytes in parallel
    for idx, expected in enumerate(chars):
        obs = observed[idx]

        # if obs is the expected integer -> OK
        if obs != "??" and obs == expected:
            continue

        # mismatch or unreadable
        # this expected byte is missing/bad
        discovered_bad.append(expected)

        # If we found an expected byte that is in known_bad (shouldn't happen because chars excludes them),
        # we would continue; but since chars excludes known_bad, any discovered here is an unexpected bad.
        # So we stop after recording it.
        break

    # Combine reported list: known_bad (already included) + discovered_bad (if any)
    if discovered_bad:
        # append discovered (they are ints)
        reported_bad.extend(discovered_bad)

    # Pretty-print the memory lines and comparison markers (similar to original script)
    char_counter = 0
    for memdump in memdump_lines:
        print(memdump)
        print(" " * 10, end="")

        for byte in memdump.bytes:
            # if we've already compared all expected chars, show filler
            if char_counter >= len(chars):
                print("--", end=" ")
            else:
                expected = chars[char_counter]
                if byte != "??" and byte == expected:
                    print("%02X" % byte, end=" ")
                else:
                    print("--", end=" ")
            char_counter += 1
        print()

    # Final reporting
    if reported_bad:
        print()
        print("[+] bad bytes (hex):")
        print(" ".join("%02X" % b for b in reported_bad))
    else:
        print()
        print("[+] No bad bytes found in the scanned range.")


def generate_byte_string(args):
    known_bad = ", ".join("%02X" % x for x in args.bad)
    var_str = "chars = bytes(i for i in range({0}, {1}) if i not in [{2}])".format(
        args.start, args.end + 1, known_bad
    )

    print("[+] characters as a range of bytes")
    print(var_str)
    print()

    print("[+] characters as a byte string")

    counter = 0
    for i in range(args.start, args.end + 1):
        if i in args.bad:
            continue

        if i == args.start:
            # first byte
            print("chars  = b'\\x%02X" % i, end="")
        elif counter % 16 == 0:
            # start a new line
            print("'")
            print("chars += b'\\x%02X" % i, end="")
        else:
            print("\\x%02X" % i, end="")

        counter += 1

    if counter % 16 != 0 and counter != 0:
        print("'")


def main(args):
    if args.address is not None:
        find_bad_chars(args)
    else:
        generate_byte_string(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s",
        "--start",
        help="hex byte from which to start searching in memory (default: 00)",
        default=0,
        type=hex_byte,
    )
    parser.add_argument(
        "-e",
        "--end",
        help="last hex byte to search for in memory (default: ff)",
        default=255,
        type=hex_byte,
    )
    parser.add_argument(
        "-b",
        "--bad",
        help="space separated list of hex bytes that are already known bad (ex: -b 00 0a 0d)",
        nargs="+",
        type=hex_byte,
        default=[],
    )

    mutuals = parser.add_mutually_exclusive_group(required=True)
    mutuals.add_argument(
        "-a", "--address", help="address from which to begin character comparison"
    )
    mutuals.add_argument(
        "-g",
        "--generate",
        help="generate a byte string suitable for use in source code",
        action="store_true",
    )

    parsed = parser.parse_args()

    if parsed.start > parsed.end:
        print("[!] --start value must be higher than --end; exiting...")
        raise SystemExit

    main(parsed)
