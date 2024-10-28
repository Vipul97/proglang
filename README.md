# ProgLang

A lexical and syntax analyzer for a custom programming language grammar in Python 3.12. It parses input code and
generates an Abstract Syntax Tree (AST) based on the specified grammar.

## Features

- **Lexical Analysis**: Breaks down source code into tokens.
- **Syntax Analysis**: Validates the structure of the code against the defined grammar.
- **Abstract Syntax Tree (AST)**: Constructs a tree representation of the code for easy analysis.

## Grammar

The language grammar is defined in Backus-Naur Form (BNF) and can be found in the [`grammar.txt`](grammar.txt) file.

## Getting Started

To run the program, execute `main.py`.

### Usage

#### Input Source Code

Your source code should be provided in a plain text file format. Ensure that the file adheres to the specified grammar
for accurate parsing.

    usage: main.py [-h] file
    
    positional arguments:
      file        Path to the code file.
    
    options:
      -h, --help  show this help message and exit

### Example

Here's how to run the program with a sample code file:

```commandline
python main.py path/to/your/code.txt
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.