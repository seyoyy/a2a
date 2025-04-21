#!/usr/bin/env python3
"""
CLI tool to extract a single APK from a .apks archive.
Usage:
  apks_to_apk_cli.py input.apks [-o output.apk] [--temp-dir temp_directory]

If -o/--output is omitted, the output filename defaults to replacing .apks with .apk.
"""
import argparse
import zipfile
import os
import shutil
import sys

def extract_apks(apks_file: str, output_dir: str) -> str:
    """Extract .apks archive and return the best APK candidate path."""
    if not os.path.isfile(apks_file):
        raise FileNotFoundError(f"APKS file not found: {apks_file}")

    os.makedirs(output_dir, exist_ok=True)
    try:
        with zipfile.ZipFile(apks_file, 'r') as zf:
            zf.extractall(output_dir)
    except zipfile.BadZipFile:
        raise RuntimeError(f"Failed to open as zip: {apks_file}")

    # Find all .apk files
    candidates = []
    for root, _, files in os.walk(output_dir):
        for fname in files:
            if fname.lower().endswith('.apk'):
                candidates.append(os.path.join(root, fname))

    if not candidates:
        raise FileNotFoundError("No .apk files found in the .apks archive.")

    # Prioritize: universal > base-master > base.apk > others
    def priority(p):
        name = os.path.basename(p).lower()
        if 'universal' in name:
            return 0
        if 'base-master' in name:
            return 1
        if name == 'base.apk':
            return 2
        return 3

    candidates.sort(key=priority)
    return candidates[0]


def main():
    parser = argparse.ArgumentParser(
        description='Extract a single APK from a .apks archive'
    )
    parser.add_argument('apks_file', help='Path to the .apks file')
    parser.add_argument('-o', '--output', dest='output_apk', nargs='?',
                        help='Destination APK path (optional)')
    parser.add_argument('--temp-dir', default='./.apks_extract_tmp',
                        help='Temporary directory for extraction')
    args = parser.parse_args()

    # Derive output if not provided
    if not args.output_apk:
        base, _ = os.path.splitext(os.path.basename(args.apks_file))
        args.output_apk = os.path.join(os.getcwd(), base + '.apk')

    try:
        apk_path = extract_apks(args.apks_file, args.temp_dir)
        shutil.copy(apk_path, args.output_apk)
        print(f"[+] APK extracted: {args.output_apk}")
        sys.exit(0)
    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
