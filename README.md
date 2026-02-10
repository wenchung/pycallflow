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
main() [pycflow.py:360]
    parse_arguments() [pycflow.py:337]
        ArgumentParser()
        ArgumentParser.add_argument()
        ArgumentParser.parse_args()
    CallFlowAnalyzer() [pycflow.py:25]
    CallFlowAnalyzer.analyze() [pycflow.py:117]
        os.path.isfile()
        CallFlowAnalyzer._analyze_file() [pycflow.py:93]
        ...
```

## Support This Project

If you find PyCallFlow useful, please consider supporting its development!

[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-pink?logo=github)](https://github.com/sponsors/wenchung)

Your sponsorship helps:
- Maintain and improve the tool
- Add new features and enhancements
- Provide better documentation and support
- Keep the project actively developed

You can also:
- ⭐ Star this repository
- 🐛 Report bugs or suggest features via [Issues](https://github.com/wenchung/pycallflow/issues)
- 🔧 Contribute code via Pull Requests

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
