import csv
import os
from custom_csv import CustomCsvReader, CustomCsvWriter

def verify_implementation():
    test_file = "verify_test.csv"
    
    # 1. Define complex data (The "Edge Cases")
    # Includes commas inside quotes, newlines inside quotes, and escaped quotes.
    expected_data = [
        ["ID", "Name", "Bio"],
        ["1", "John Doe", "Standard text"],
        ["2", "Jane, Doe", "Bio with a comma"],
        ["3", "Bob \"The Builder\"", "Bio with escaped quotes"],
        ["4", "Alice", "Bio with a\nnewline character"]
    ]

    print("--- Starting Verification Test ---")

    # 2. Test the Writer
    print("Testing Writer...")
    writer = CustomCsvWriter(test_file)
    writer.write_all(expected_data)
    
    # Check if the file was actually created
    if os.path.exists(test_file):
        print("✅ CSV file generated successfully.")
    else:
        print("❌ Failed to generate CSV file.")
        return

    # 3. Test the Reader and compare with Standard Library
    print("Testing Reader logic...")
    custom_rows = []
    reader = CustomCsvReader(test_file)
    for row in reader:
        custom_rows.append(row)

    # Use the standard library as the 'Ground Truth'
    standard_rows = []
    with open(test_file, 'r', encoding='utf-8', newline='') as f:
        std_reader = csv.reader(f)
        for row in std_reader:
            standard_rows.append(row)

    # 4. Final Comparison
    if custom_rows == expected_data:
        print("✅ Custom Reader output matches original data!")
    else:
        print("❌ Custom Reader output differs from original data.")
        print(f"Expected: {expected_data}")
        print(f"Got:      {custom_rows}")

    if custom_rows == standard_rows:
        print("✅ Custom Reader matches Standard CSV Library exactly!")
    else:
        print("❌ Logic Mismatch: Your reader is behaving differently than the standard library.")

    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)

if __name__ == "__main__":
    verify_implementation()