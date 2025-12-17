import csv
import timeit
from custom_csv import CustomCsvReader, CustomCsvWriter

def run_benchmark():
    # 1. Generate Synthetic Data (10,000 rows, 5 columns)
    data = [[f"Col_{j} Row_{i}" for j in range(5)] for i in range(10000)]
    # Add an edge case
    data[500] = ["Simple", "With, Comma", 'With "Quote"', "With\nNewline", "Normal"]
    
    # 2. Benchmark Writer
    def test_custom_writer():
        writer = CustomCsvWriter("test_custom.csv")
        writer.write_all(data)

    def test_std_writer():
        with open("test_std.csv", "w", newline="") as f:
            csv.writer(f).writerows(data)

    print(f"Writer (Custom): {timeit.timeit(test_custom_writer, number=3):.4f}s")
    print(f"Writer (Standard): {timeit.timeit(test_std_writer, number=3):.4f}s")

    # 3. Benchmark Reader
    def test_custom_reader():
        return list(CustomCsvReader("test_custom.csv"))

    def test_std_reader():
        with open("test_std.csv", "r") as f:
            return list(csv.reader(f))

    print(f"Reader (Custom): {timeit.timeit(test_custom_reader, number=3):.4f}s")
    print(f"Reader (Standard): {timeit.timeit(test_std_reader, number=3):.4f}s")

if __name__ == "__main__":
    run_benchmark()