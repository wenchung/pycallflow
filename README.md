# PyCallFlow

A static analysis tool for Python that generates function call flow diagrams, similar to the `cflow` tool for C.

## Features

- **Static AST Analysis**: Parse Python source code without execution
- **Multi-file Support**: Analyze single files or entire directories
- **Tree-structured Output**: Clear hierarchical display of function call relationships
- **Recursion Detection**: Automatically marks recursive calls
- **Class Method Support**: Properly handles method calls within classes
- **Reverse Tracing**: See which functions call a specified function
- **Graphviz Export**: Generate visual diagrams
- **Line Number Display**: Precise function definition locations

## Installation

No external dependencies required - only Python 3.6+ standard library.

```bash
git clone https://github.com/wenchung/pycallflow.git
cd pycallflow

# Make executable (Linux/macOS)
chmod +x pycflow.py
```

## Quick Start

### Basic Usage

```bash
# Run as executable (Linux/macOS)
./pycflow.py script.py

# Or run with Python (all platforms)
python pycflow.py script.py

# Analyze from a specific function
./pycflow.py script.py -f main

# Show reverse call tree (who calls this function)
./pycflow.py script.py -r -f process_data

# Control depth
./pycflow.py script.py -f main -d 3

# Export to Graphviz
./pycflow.py script.py --dot output.dot
dot -Tpng output.dot -o callgraph.png
```

## Example Output

```
main() [example.py:25]
    fetch_data() [example.py:20]
        print()
    process_data() [example.py:8]
        helper_function() [example.py:4]
        validate_result() [example.py:12]
    print()
```

## Command Line Options

```
usage: pycflow.py [-h] [-f FUNCTION] [-r] [-d DEPTH] [--dot DOT] path

Python Call Flow Analyzer

positional arguments:
  path                  Python file or directory to analyze

optional arguments:
  -h, --help            show this help message and exit
  -f FUNCTION, --function FUNCTION
                        Start analysis from specific function
  -r, --reverse         Show reverse call tree (who calls this function)
  -d DEPTH, --depth DEPTH
                        Maximum depth for call tree (default: unlimited)
  --dot DOT             Export to Graphviz DOT format
```

## Use Cases

- **Code Review**: Understand function call relationships in unfamiliar codebases
- **Documentation**: Generate call flow diagrams for documentation
- **Refactoring**: Identify function dependencies before refactoring
- **Learning**: Study the structure of open source projects
- **Debugging**: Trace execution paths to locate bugs

## Limitations

- Static analysis only - doesn't detect dynamic calls (e.g., `getattr()`, `eval()`)
- Doesn't track external library calls beyond the call site
- Method resolution order in complex inheritance hierarchies may be incomplete

## Example: Analyzing PyCallFlow Itself

```bash
# See the tool's own structure
./pycflow.py pycflow.py -f main

# Output:
main() [pycflow.py:290]
    PyCallFlow() [pycflow.py:138]
    analyzer.analyze_file() [pycflow.py:165]
        CallFlowAnalyzer() [pycflow.py:28]
        open()
        ast.parse()
        analyzer.visit()
    analyzer.print_call_tree() [pycflow.py:204]
        self._print_tree() [pycflow.py:216]
            self._print_tree() [pycflow.py:216] <recursive>
```

## Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

MIT License - see LICENSE file for details

## Author

Created by wenchung

## Acknowledgments

Inspired by the classic Unix `cflow` tool for C programs.