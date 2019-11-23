HexPi
=====================================

## What's this?
This is GPIO frontend for IR Remote Controller etc.

## How to Build?
> You should be install `pipenv`.

### Install requirements
```bash
pipenv install
```

### Build
```bash
pipenv run pyinstaller -F --clean ./hexpi.py
```
> binary files are export to `dist` directory.

## How to Use?
```bash
hexpi <gpio> [options...]

# Start HTTP Endpoint
hexpi 3 http

# Just send with HexCode(AEHA)
hexpi 3 hex 0x00 0x01 ....

# Just send IR Signal...
hexpi 3 ir 3000 200 ....
```
