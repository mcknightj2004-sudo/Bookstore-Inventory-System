# Bookstore Inventory System (Python)

Menu-driven bookstore inventory program using a CSV file for data storage.  
Features include listing books, summary reporting, genre reports, adding new books, updating stock, sorting by author, and a genre bar chart.

## Features
1. List book titles and details (limited output)
2. Summary report (total titles, total value, average price)
3. Titles by genre report
4. Add a new book (writes to CSV)
5. Query a book and update stock (writes to CSV)
6. List books ordered by author
7. Bar chart of number of books per genre

## Requirements
- Python 3.x
- pandas
- matplotlib

## Setup

Install dependencies:

### Windows
```bash
py -m pip install -r requirements.txt
```
## Run
### Windows
```bash
cd Bookstore
py group_6.py
```
## Data File
This program reads and writes to:
``` Books data.csv ```
The CSV must be in the same folder as the Python file.

## Expected columns
Your CSV should contain these column headers:
- Title
- Author
- Genre
- Cost
- Stock



