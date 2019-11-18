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
