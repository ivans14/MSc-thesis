# Example Server

This module defines a SiLA 2 Server that implements multiple features for demonstration purposes. Documentation on SiLA Server development can be found [here](https://sila2.gitlab.io/sila_python/content/server/index.html).

## Setup

Run `pip install .` from the directory containing this file, or `pip install example_server/` from the parent directory.

## Starting the server

Run the module with `python -m sila2_example_server` to start the server program. Use `--help` to see the available options.
By default, the server starts on 127.0.0.1:50052 with SiLA Server Discovery enabled.
python -m sila2_example_server --ca-export-file ca.pem to create certificate file

## Features

### [GreetingProvider](sila2_example_server/features/greetingprovider/GreetingProvider.sila.xml)

- Unobservable Command: `SayHello`
  - Takes a string parameter `Name`
  - Responds with a string `Greeting`
- Unobservable Property: `StartYear`
  - The start year of the server, as integer

### [TimerProvider](sila2_example_server/features/timerprovider/TimerProvider.sila.xml)

- Observable Property: `CurrentTime`
  - The current time
- Observable Command: `Countdown`
  - Takes a positive integer `N` and a string `Message`
  - Counts down from `N` to zero
  - Sends each number as intermediate response `CurrentNumber`
  - Responds with the timestamp of completion, and the message

### [DelayProvider](sila2_example_server/features/delayprovider/DelayProvider.sila.xml)

- Unobservable Property: `Random Number`
  - A random integer
  - Affected by the `Delay` metadata
- Metadata: `Delay`
  - Non-negative integer with unit `Millisecond`
  - When sent, the requested call is delayed by the given duration
  - Affects the property `StartYear` from the feature [GreetingProvider](#GreetingProvider)
- DefinedExecutionError: `DelayTooLong`

### [DataTypeProvider](sila2_example_server/features/datatypeprovider/DataTypeProvider.sila.xml)

- Custom type: `IntegerAlias`
  - An alias for the basic type Integer
- Custom type: `StructureType`
  - A `tructure with two elements:
    - `ListOfStrings`: A list of strings
    - `Boolean`: A boolean
- Unobservable Command: `ComplexCommand`
  - Parameters:
    - `Number`: Custom type `IntegerAlias`
    - `Structure`: Custom type `StructureType`
  - Responses:
    - `StructureType`: Custom type `StructureType`
    - `InlineStructure`: Structure with two elements:
      - `Element1`: A string
      - `Element2`: A float
- UnobservableProperty: `StructureProperty`
  - Structure with two elements:
    - `Binary`: A binary
    - `Dates`: A list of dates

## Module structure

### `generated/`

This directory contains files that are generated from feature definitions (`.sila.xml` files).

### `feature_implementations/`

This directory contains feature implementations. They inherit from a base class located in the `feature/` directory and
define the server behavior related to the features.

### `server.py`

This file defines the actual server.

### `client.py`

This file defines a client class that can be used to control the server. The class `SilaClient` implements a dynamic
client. The class `Client` inherits from it and provides two benefits:

1. type annotations for code completion and static type checking
2. defined execution errors are raises as actual instances of the error types (e.g. `UnimplementedFeature`) instead of the generic type `DefinedExecutionError`

### `__main__.py`

This file is the entry point when executing the module. It defines a basic server application.
