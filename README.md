# Custom CSV Parser Implementation:

A robust, low-level CSV reader and writer built from scratch in Python. This project demonstrates the mechanics of data parsing and serialization using a Finite State Machine (FSM) to handle complex data formats without relying on Python's built-in csv module.

**🚀 Overview:**

Standard CSV parsing is deceptively complex. A simple `.split(',')` approach fails when fields contain commas, quotes, or newlines. This implementation handles these edge cases by processing files character-by-character and managing internal states to ensure 100% data integrity.

**📁 Project Structure:**

- `custom_csv.py:` Contains the core logic for the CustomCsvReader (iterator-based) and CustomCsvWriter classes.
- `benchmark.py:` Script to quantitatively measure performance against Python's standard library.
- `test_parser.py:` A verification suite to ensure parity with standard library output.
- `requirements.txt:` List of dependencies (empty, as this uses only Standard Library).

**🛠 Setup & Usage:** 

**Installation:** 

No external libraries are required. Simply ensure you have Python 3.x installed.

**Usage Example:**

```
from custom_csv import CustomCsvReader, CustomCsvWriter

# Writing data with edge cases
data = [
    ["ID", "Name", "Comment"],
    ["1", "Alice", "Likes \"quotes\" and , commas"],
    ["2", "Bob", "Comment with\nmultiple lines"]
]

writer = CustomCsvWriter('output.csv')
writer.write_all(data)

# Reading data in a streaming fashion (Memory Efficient)
reader = CustomCsvReader('output.csv')
for row in reader:
    print(row)
```
**📊 Benchmarking & Performance Analysis:**

The benchmark was executed using a synthetic dataset of 10,000 rows and 5 columns.
```
Implementation         Writer Speed (avg)      Reader Speed (avg)
Custom (Pure Python)      0.0818s                0.3350s
Standard (C-Optimized)    0.0508s                0.0615s
```
**Analysis:**
1. **Writer Efficiency:** The custom writer is only about **1.6x slower** than the standard library. This is because the logic (string joining and basic escaping) is relatively straightforward for the Python interpreter to execute.
2. **Reader Overhead:** The custom reader is approximately **5.5x slower**. This is due to the character-by-character iteration and state-switching logic being executed within the Python virtual machine rather than at the hardware level.
3. **The "C" Advantage:** Python’s built-in `csv` module is implemented in C. It performs character-level parsing at machine speed, whereas our custom version incurs overhead for every function call and character processed by the interpreter.
4. **Streaming Architecture:** Despite the speed difference, the custom reader is highly memory-efficient. By using the `iterator` protocol (`__next__`), it processes one row at a time, allowing it to handle files far larger than the available RAM.

**🧠 Design Decisions:**
- **State Machine Logic:** I used a state machine to track if the parser is currently `Inside_Quotes` or `Outside_Quotes`. This allows the parser to treat a comma as a literal character when quoted and a delimiter when not.
- **Escaping Strategy:** Per RFC 4180 standards, double quotes inside a field are handled by looking for a sequence of two double quotes (`""`) and converting them into a single literal quote.
- **PEP 8 Compliance:** The code follows strict Python styling guidelines, including meaningful naming conventions and the use of context managers (`with` statements) for safe file I/O.