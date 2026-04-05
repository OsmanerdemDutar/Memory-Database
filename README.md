# Memory Database Management System (DBMS)

This repository contains a Python-based Memory Database Management System developed to parse, execute, and manage custom SQL-like commands. The program reads operations from a text file, processes the data entirely within the system's memory using structured dictionaries, and outputs the results in dynamically formatted ASCII tables.

This project was developed as part of the BBM103 course assignments, focusing on advanced data structures, string manipulation, and creating a custom command parser.

## 🚀 Features

- **Custom Command Parser:** Reads and executes database operations sequentially from a given text file.
- **Supported Operations:**
  - `CREATE_TABLE`: Initializes a new table with specified column headers.
  - `INSERT`: Adds new records to a specified table.
  - `SELECT`: Retrieves data based on specific conditions (JSON-like syntax).
  - `UPDATE`: Modifies existing records based on given criteria.
  - `DELETE`: Removes records that match specific conditions.
  - `JOIN`: Merges two tables based on a common column.
  - `COUNT`: Returns the total number of entries matching a condition.
- **Dynamic ASCII Table Rendering:** Automatically adjusts column widths to neatly display queried data in the console.
- **Error Handling:** Gracefully handles missing tables or columns, notifying the user without crashing the system.

## 🛠️ Tech Stack
- **Language:** Python 3.9+
- **Libraries:** `sys` (for command-line argument handling)

## 📦 Input Format Example
The engine processes text files containing custom commands. Example (`i1.txt`):
```text
CREATE_TABLE students id,name,age,major
INSERT students 1,John Doe,20,CS
INSERT students 2,Jane Smith,22,EE
SELECT students id,name WHERE {"major": "CS"}
UPDATE students {"major": "SE"} WHERE {"name": "John Doe"}
DELETE students WHERE {"age": 22}
```

## ⚙️ How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/OsmanerdemDutar/Memory-Database.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Memory-Database
   ```
3. Run the Python script via terminal, providing the input text file as an argument:
   ```bash
   python src/database.py data/i1.txt
   ```
4. The system will execute the commands and print the formatted database tables and operation logs directly to the console. *(You can also redirect the output to a text file using `> output.txt`)*.

## 📊 Output Example

When a table is queried or modified, the engine generates a clean visual representation:
```text
###################### INSERT #########################
Inserted into 'students': ('1', 'John Doe', '20', 'CS')

Table: students
+----+----------+-----+-------+
| id | name     | age | major |
+----+----------+-----+-------+
| 1  | John Doe | 20  | CS    |
+----+----------+-----+-------+
#######################################################
```
