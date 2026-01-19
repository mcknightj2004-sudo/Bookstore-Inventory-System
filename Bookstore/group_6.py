
import pandas as pd
import csv
from collections import Counter
import matplotlib.pyplot as plt

# Load CSV data
def load_books_data(file_path="Books data.csv"):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print("CSV file not found.")
        return pd.DataFrame()


# Feature 1: Output list of book titles and their respective details
def list_book_titles_and_details(df, limit=20):
    if df.empty:
        print("No data available.")
        return
    print(df[["Title","Author","Genre","Cost"]].head(limit).to_string(index=False))
    print(f"\nShowing {min(limit, len(df))} of {len(df)} rows.")


# Feature 2: Summary report

def summary_report(df):
    total_value = 0
    total_titles = 0
    total_price = 0
    skipped = 0  # <--- add this

    for _, row in df.iterrows():
        try:
            price = float(row['Cost'])
            stock = float(row['Stock'])

            if pd.isna(price) or pd.isna(stock):
                raise ValueError("Missing value")

            total_titles += 1
            total_price += price
            total_value += price * stock

        except (ValueError, KeyError):
            skipped += 1         
            continue

    average_price = total_price / total_titles if total_titles > 0 else 0

    print("\nSummary Report")  
    print(f"The Total Titles: {total_titles}")
    print(f"The Total Value of The Books: ${total_value:.2f}")
    print(f"The Average Price: ${average_price:.2f}")

    if skipped > 0:
        print(f"Skipped {skipped} bad rows.")



# Feature 3: Report on number of titles in each genre
def genre_title_report(df):
    print("Feature 3 selected: Titles by genre.")
    report = df.groupby("Genre")["Title"].nunique().reset_index()
    report.columns = ["Genre", "Number of Titles"]
    print(report.sort_values(by="Number of Titles", ascending=False))

# Feature 4: Add a new book 
def prompt_for_new_book(df, filename="Books data.csv"):
    if input("Add a new book? (Y/N): ").strip().upper() != "Y":
        return df

    title = input("Enter book title: ")
    author = input("Enter author name: ")
    genre = input("Enter genre: ")
    try:
        price = float(input("Enter price: "))
    except ValueError:
        print("Invalid price.")
        return df

    # you probably need Stock too:
    try:
        stock = int(input("Enter stock: "))
    except ValueError:
        stock = 0

    new_row = {"Title": title, "Author": author, "Genre": genre, "Cost": price, "Stock": stock}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(filename, index=False)
    print(f"Added: {title}")
    return df



# Feature 5: Search and update stock of a book
def query_and_update_stock(df, title_input, filename="Books data.csv"):

    books = df.to_dict(orient='records')
    updated = False

    for book in books:
        if book['Title'].lower() == title_input.lower():
            try:
                current_stock = float(book['Stock'])
            except ValueError:
                print("Invalid stock value. Skipping this book.")
                return

            print(f"Found: {book['Title']} (Stock: {int(current_stock)})")
            action = input("Type 'i' to increase or 'd' to decrease stock: ").lower()

            if action in ['i', 'd']:
                try:
                    amount = int(input("Enter amount: "))
                except ValueError:
                    print("Invalid amount. Aborting update.")
                    return

                if action == 'i':
                    stock = current_stock + amount
                else:
                    stock = current_stock - amount
                    if stock <= 0:
                        stock = 0
                        print("Book is out of stock")

                book['Stock'] = str(int(stock))
                updated = True
                break

    if not updated:
        print("Book not found or no changes made.")
    else:
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=books[0].keys())
            writer.writeheader()
            writer.writerows(books)
        print("Stock updated")


# Feature 6: Output books ordered by author
def list_books_by_author(df):
    print("Feature 6 selected: Books ordered by author.")
    sorted_df = df.sort_values(by="Author")
    for _, row in sorted_df.iterrows():
        print(f"{row['Author']} - \"{row['Title']}\"")



# Feature 7: Plot the bar chart for genres
def plot_genre_bar_chart(df):
    print("Feature 7 selected: Bar chart of number of books per genre.")
    genre_list = []
    for _, book in df.iterrows():
        genres = [genre.strip() for genre in str(book['Genre']).split(',')]
        genre_list.extend(genres)

    genre_count = Counter(genre_list)

    genres = list(genre_count.keys())
    counts = list(genre_count.values())

    plt.figure(figsize=(10, 6))
    plt.bar(genres, counts, color='skyblue')
    plt.xlabel('Genres')
    plt.ylabel('Number of Books')
    plt.title('Number of Books in Each Genre')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


# Menu system
def main():
    df = load_books_data()
    while True:
        print("\nBookstore System Menu:")
        print("1. List of book titles and their respective details")
        print("2. Summary report of titles, stock, and average price")
        print("3. Report of number of titles in each genre")
        print("4. Add a new book item")
        print("5. Query or update book stock")
        print("6. List books ordered by author")
        print("7. Bar chart of number of books per genre")
        print("0. Exit")

        choice = input("Enter your choice (0-7): ")

        if choice == "1":
            try:
                limit = int(input("How many books to show? (e.g. 20): "))
            except ValueError:
                limit = 20
            list_book_titles_and_details(df, limit)
        elif choice == "2":
            summary_report(df)
        elif choice == "3":
            genre_title_report(df)
        elif choice == "4":
            df = prompt_for_new_book(df) 
        elif choice == "5":
            title_input = input("Enter the book title to search: ")
            query_and_update_stock(df, title_input)
            df = load_books_data()  
        elif choice == "6":
            list_books_by_author(df)
        elif choice == "7":
            plot_genre_bar_chart(df)
        elif choice == "0":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number from 0 to 7.")

if __name__ == "__main__":
    main()
