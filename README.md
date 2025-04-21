# a2a - APKS to APK Converter

A command-line tool for extracting a single APK from an .apks archive file.

## Description

a2a is a simple utility that extracts the most suitable APK file from an Android App Bundle (.apks) archive. It automatically prioritizes APK candidates in the following order:
1. Universal APK files
2. Base-master APK files
3. base.apk files
4. Other APK files

## Installation

```bash
git clone https://github.com/username/a2a.git
cd a2a
```

## Requirements

- Python 3

## Usage

Basic usage:
```bash
python main.py input.apks
```

Specify output path:
```bash
python main.py input.apks -o output.apk
```

Specify a custom temporary directory:
```bash
python main.py input.apks --temp-dir custom_temp_dir
```

## Options

- `apks_file`: Path to the .apks file (required)
- `-o, --output`: Destination APK path (optional, defaults to input filename with .apk extension)
- `--temp-dir`: Temporary directory for extraction (defaults to ./.apks_extract_tmp)

## Example

```bash
python main.py game.apks -o extracted_game.apk
```

## License

See the LICENSE file for details.
