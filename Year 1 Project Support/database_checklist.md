### SQLite Database Requirements

2nd Normal Form
- All requirements of 1NF:
  - no duplicate rows
  - columns must contain single values
  - no repeated columns representing the same attribute
  - there must be a clear primary key
- No 'partial dependencies', in order to eliminate redundancy
  - columns that aren't part of any candidate key (column(s) that could be a primary key) should rely on the entirety of every candidate key ('full functional dependency')
  - you will likely have to split one table into multiple to satisfy this requirement!

No ID/'surrogate primary key'/'RowID' columns where possible - this means ensuring there is another reasonable primary key within the data itself.

All column types specified in the brief should be included (numeric, free text, categorical).

At least 3 tables, connected with reasonable foreign keys.

Tables should have a reasonable number of rows (check the assignment brief), so that SQL statements can be executed and show results.