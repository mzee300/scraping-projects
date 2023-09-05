import csv
import time
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import os


def scrape_page(driver, city_name):
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'lxml')
    gym_data = []

    tr = soup.find_all('div', class_='v-card')
    for t in tr:
        try:
            description = t.find('div', class_='categories').text
        except:
            description = ''
        if "GYM" in description or "Fitness" in description:
            try:
                name = t.find('a', class_='business-name').text
            except:
                name = ''
            try:
                phone = t.find('div', class_='phones phone primary').text
            except:
                phone = ''
            try:
                adr = t.find('div', class_='adr').text
            except:
                adr = ''
            gym_data.append([name, phone, adr, description])

    return gym_data, soup


def save_to_csv(data, city_name):
    with open(f"gymdata_TX/{city_name}.csv", 'a', newline="", encoding="utf-8") as f:
        csvwriter = csv.writer(f)
        for row in data:
            csvwriter.writerow(row)


def setup_driver():
    options = uc.ChromeOptions()
    options.add_argument("C:\\Users\\scrap\\PycharmProjects\\yelb\\selenium")
    return uc.Chrome(options=options)


def scrape_city(city_name, driver):
    driver.get("https://www.yellowpages.com/")
    time.sleep(3)
    search = driver.find_element(By.NAME, "search_terms")
    search.send_keys("attorneys")
    location = driver.find_element(By.NAME, "geo_location_terms")
    location.clear()
    location.send_keys(city_name + " TX")
    time.sleep(1)
    location.submit()
    time.sleep(3)

    rv_data, soup = scrape_page(driver, city_name)
    save_to_csv(rv_data, city_name)

    try:
        all_pages = soup.find('div', class_='pagination').find_all('li')
        all_links = [page.find('a').attrs['href'] for page in all_pages[2:-1] if page.find('a')]
        for l in all_links:
            li = "https://www.yellowpages.com" + l
            driver.get(li)
            time.sleep(3)
            rv_data, _ = scrape_page(driver, city_name)
            save_to_csv(rv_data, city_name)
    except Exception as e:
        print(f"Oops! {str(e)}")


def run_scraper(last_file_index=None, start_index=0):
    driver = setup_driver()

    with open('texas cities.csv', 'r') as file:
        reader = csv.reader(file)
        lsit_reader = list(reader)

    folder_path = r"C:\Users\scrap\PycharmProjects\YellowPages\gymdata_TX"
    files = []
    for file in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file)):
            files.append(file)
    if files:
        last_file = max(files).split('.')[-2]
        if last_file == last_file_index:
            return
        search_file_path = r"C:\Users\scrap\PycharmProjects\YellowPages\texas cities.csv"
        with open(search_file_path, "r") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if last_file in line:
                    start_index = i + 1
                    break
            else:
                print(f"Could not find {last_file} in the file.")
                return

    for i, link in enumerate(lsit_reader[start_index:], start_index):
        try:
            print(f"({i + 1}/{len(lsit_reader)}) Scraping city {link[0]}")
            scrape_city(link[0], driver)
        except Exception as e:
            print(f"Error in scraping city {link[0]}: {e}")
            driver.quit()
            return i

    driver.quit()


def main():
    run_scraper()


if __name__ == "__main__":
    main()
