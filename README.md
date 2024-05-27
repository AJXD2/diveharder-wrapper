# DiveharderWrapper For Python

A Helldivers 2 API wrapper using the [Diveharder API](https://github.com/helldivers-2/diveharder_api.py).

> [!WARNING]
> 
> This project is still under heavy development. Expect things to break in the future. There be dragons ahead.

## Introduction

This project aims to provide a convenient Python wrapper for the Diveharder API, allowing developers to easily interact with Helldivers 2 game data.

## Installation

For now, I have decided not to publish this on PyPI as it is in development. However, I have reserved the [diveharder name on PyPI](https://pypi.org/project/diveharder/).

1. Clone the repository:

    ```sh
    git clone https://github.com/ajxd2/diveharder-wrapper
    cd diveharder-wrapper
    ```

2. Install Poetry:

    ```sh
    pip install poetry
    ```

3. Build the package:

    ```sh
    poetry build
    ```

4. Install the package using the `.whl` file:

    ```sh
    python -m venv venv
    # On Windows
    source venv/Scripts/activate
    # On Unix or MacOS
    source venv/bin/activate
    pip install dist/diveharder-*.whl
    ```

## Usage

Here's a simple example of how to use the DiveharderWrapper:

```python
from diveharder import DiveHarderApiClient

api = DiveHarderApiClient()

print(api.dispatches.get_latest_dispatch().message)
```

