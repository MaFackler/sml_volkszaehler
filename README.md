# SML Volkszaehler

Package to read SML Data from tty device.

## Installation

### Building the package

```bash
# The build package has to be installed
# pip install build
python -m build
```

### Installation
```bash
pip install dist/<filename>.whl
```

### Development installation

```bash
# Create virtual env
python -m venv .myenv

# Activate virtual env
source .myenv/bin/activate

# install the current repo
pip install -e .
```

### Run tests

```bash
pytest -v
```

### Usage
```bash
python -m sml_volkszaehler /dev/<ttyDevice>
```
