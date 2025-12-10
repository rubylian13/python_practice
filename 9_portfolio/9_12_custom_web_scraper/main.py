from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

URL = "https://www.audible.com/search?keywords=book&node=18573211011"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
BOOKS = []

class WebScraper:
    """
    Build a custom web scraper to collect data on things that you are interested in.
    """
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_books_info(self):
        self.driver.get(URL)
        time.sleep(3)

        items = self.driver.find_elements(By.CSS_SELECTOR, "li.bc-list-item.productListItem")

        for item in items:
            try:
                book_name = item.find_element(By.CSS_SELECTOR, "h3.bc-heading.bc-color-link.bc-pub-break-word"
                                                               ".bc-size-medium").text.strip()
                try:
                    subtitle = item.find_element(By.CSS_SELECTOR, "li.bc-list-item.subtitle").text
                except:
                    subtitle = ""
                author = item.find_element(By.CSS_SELECTOR, "li.bc-list-item.authorLabel").text.strip()
                run_time_length = item.find_element(By.CSS_SELECTOR, "li.bc-list-item.runtimeLabel").text.strip()
                release_date =  item.find_element(By.CSS_SELECTOR, "li.bc-list-item.releaseDateLabel").text.strip()
                language = item.find_element(By.CSS_SELECTOR, "li.bc-list-item.languageLabel").text.strip()
                ratings = item.find_element(By.CSS_SELECTOR, "span.bc-text.bc-size-callout").text.strip()

                BOOKS.append([book_name, subtitle, author, run_time_length, release_date, language, ratings])
            except:
                pass

        self.driver.quit()

    def save_to_csv(self):
        # 輸出 CSV
        with open("books_selenium.csv", "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Book_Name", "Subtitle", "Author", "Length", "Release Date", "Language", "Ratings"])
            for b in BOOKS:
                writer.writerow(b)

        print("✅ 完成！共有", len(BOOKS), "本書")

if __name__ == "__main__":
    bot = WebScraper()
    bot.get_books_info()
    bot.save_to_csv()




