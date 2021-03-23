# Enqueue

Library for building stream-based applications.

## Prerequisites

* [Python (>=3.6.0)](https://www.python.org)

## Installation

### Production

Install package:

```
pip install enqueue>=1.0.0
```

### Development

Install package:

```
pip install .
```

Install package and sample dependencies:

```
pip install .[sample]
```

Install package and test dependencies:

```
pip install .[test]
```

Use the `-e, --editable` flag to install the package in development mode.

## Usage

Check the sample scripts available in the `scripts` directory for examples.

Run sample script:

```
python scripts/double_values.py
```

> **Note:** requires sample dependencies.

## Test

Run tests:

```
pytest
```

> **Note:** requires test dependencies.

## Copyright and license

Copyright (c) 2021, Danilo Peixoto. All rights reserved.

Project developed under a [BSD-3-Clause License](LICENSE.md).
