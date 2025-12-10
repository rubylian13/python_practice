import requests
from bs4 import BeautifulSoup
import csv

URL = "https://www.audible.com/search?keywords=book&node=18573211011"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

BOOKS = []


def get_books_info():
    response = requests.get(URL, headers=HEADERS)
    if response.status_code != 200:
        print("Failed to retrieve the page")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Find all book items
    items = soup.select("li.bc-list-item.productListItem")

    for item in items:
        try:
            book_name_tag = item.select_one("h3.bc-heading.bc-color-link.bc-pub-break-word.bc-size-medium")
            book_name = book_name_tag.text.strip() if book_name_tag else ""

            subtitle_tag = item.select_one("li.bc-list-item.subtitle")
            subtitle = subtitle_tag.text.strip() if subtitle_tag else ""

            author_tag = item.select_one("li.bc-list-item.authorLabel")
            author = author_tag.text.strip() if author_tag else ""

            length_tag = item.select_one("li.bc-list-item.runtimeLabel")
            run_time_length = length_tag.text.strip() if length_tag else ""

            release_tag = item.select_one("li.bc-list-item.releaseDateLabel")
            release_date = release_tag.text.strip() if release_tag else ""

            language_tag = item.select_one("li.bc-list-item.languageLabel")
            language = language_tag.text.strip() if language_tag else ""

            ratings_tag = item.select_one("span.bc-text.bc-size-callout")
            ratings = ratings_tag.text.strip() if ratings_tag else ""

            BOOKS.append([book_name, subtitle, author, run_time_length, release_date, language, ratings])
        except Exception as e:
            print("Error parsing book:", e)
            continue


def save_to_csv():
    with open("books_beautifulsoup.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Book_Name", "Subtitle", "Author", "Length", "Release Date", "Language", "Ratings"])
        for b in BOOKS:
            writer.writerow(b)

    print(f"✅ 完成！共有 {len(BOOKS)} 本書")


if __name__ == "__main__":
    get_books_info()
    save_to_csv()
