import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import Tk, Label, Entry, Button, StringVar, filedialog

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.headless = True

# Create an empty list to store data dictionaries
def noon_link_product(base_url, last_url, tab_name, download_folder):
    data_list = []
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
        # Replace the URL with the actual URL of the page you are testing
        base_url = base_url
        last_url = last_url
        current_page = 1
        urla = f"{base_url}{current_page}{last_url}"
        driver.get(urla)
        time.sleep(1)
        # Find the pagination element
        page_links = driver.find_elements(By.CLASS_NAME,"pageLink")
        total_pages = len(page_links)
        last_page_number = int(total_pages)

        base_url = base_url
        last_url = last_url
        current_page = 1
        time.sleep(1)
        while True:
            time.sleep(1)
            url = f"{base_url}{current_page}{last_url}"
            time.sleep(1)
            driver.get(url)
            time.sleep(1)
            try:
                parent_elements = driver.find_elements(By.CSS_SELECTOR, ".sc-5c17cc27-0.eCGMdH.wrapper.productContainer")
                time.sleep(1)
                vg = len(parent_elements)
                # import pdb
                # pdb.set_trace()
                def check_n_get_element(parent_element, attr):
                    try:
                        c_val = parent_element.find_element(By.CSS_SELECTOR, attr)
                        return c_val
                    except NoSuchElementException:
                        return None

                for parent_element in parent_elements:
                    #Name_element = parent_element.find_element(By.CSS_SELECTOR, ".sc-5c17cc27-0.eCGMdH.wrapper.productContainer")
                    link = parent_element.find_element(By.TAG_NAME, 'a').get_attribute("href")
                    print(link)
                    data_list.append(link)
                current_page += 1
                # Break the loop if we have reached the last page
                if current_page > last_page_number:
                    break

            except NoSuchElementException:
                # Break the loop if there is no pagination element (e.g., on the last page)
                break

    scrape_list = []

    def check_n_get_element(parent_element, attr):
        try:
            c_val = parent_element.find_element(By.CSS_SELECTOR, attr)
            return c_val
        except NoSuchElementException:
            return None

    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
        for link in data_list:
            print(link)
            driver.get(link)
            time.sleep(1)

            try:
                brand_name_element = driver.find_element(By.CLASS_NAME, 'sc-6f72a2a1-16')
                brand_name = brand_name_element.text.strip()

                product_name_element = driver.find_element(By.CLASS_NAME, 'sc-6f72a2a1-17')
                product_name = product_name_element.text.strip()

                price_element = driver.find_element(By.CLASS_NAME, 'priceWas')
                price_old = price_element.text.strip()

                price_element = driver.find_element(By.CLASS_NAME, 'priceNow')
                price_new = price_element.text.strip()

                offer_element = driver.find_element(By.CLASS_NAME, 'profit')
                offer = offer_element.text.strip()

                # Continue extracting other product details as needed

                noon_data = {
                    'brand_name': brand_name,
                    'product_name': product_name,
                    'price_old': price_old,
                    'price_new': price_new,
                    'offer': offer
                    # Add other details here
                }

                scrape_list.append(noon_data)

            except NoSuchElementException:
                print(f"Skipping invalid link: {link}")

    # Create a DataFrame from the scraped data
    df = pd.DataFrame(scrape_list)

    # Save the DataFrame to an Excel file with the provided sheet name and download folder
    file_path = os.path.join(download_folder, f'{tab_name}.xlsx')
    df.to_excel(file_path, index=False)
    print(f"Data saved to: {file_path}")

def noon_link_page(base_url, last_url, tab_name, download_folder):
    data_list = []
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
        # Replace the URL with the actual URL of the page you are testing
        base_url = base_url
        last_url = last_url
        current_page = 1
        urla = f"{base_url}{current_page}{last_url}"
        driver.get(urla)
        time.sleep(1)
        # Find the pagination element
        page_links = driver.find_elements(By.CLASS_NAME, "pageLink")
        if page_links:
            # Extract the last page number
            last_page_element = page_links[-1]
            last_page_number = int(last_page_element.text) if last_page_element.text.isdigit() else 0
            print(f"Total Pages: {last_page_number}")
        else:
            print("No page links found.")

        base_url = base_url
        last_url = last_url
        current_page = 1
        time.sleep(1)
        while True:
            time.sleep(1)
            url = f"{base_url}{current_page}{last_url}"
            time.sleep(1)
            driver.maximize_window()
            driver.get(url)
            time.sleep(1)
            try:
                parent_elements = driver.find_elements(By.CSS_SELECTOR,
                                                       ".sc-5c17cc27-0.eCGMdH.wrapper.productContainer")
                time.sleep(1)
                vg = len(parent_elements)

                # import pdb
                # pdb.set_trace()
                def check_n_get_element(parent_element, attr):
                    try:
                        c_val = parent_element.find_element(By.CSS_SELECTOR, attr)
                        return c_val
                    except NoSuchElementException:
                        return None

                for parent_element in parent_elements:
                    # Name_element = parent_element.find_element(By.CSS_SELECTOR, ".sc-5c17cc27-0.eCGMdH.wrapper.productContainer")
                    try:
                        brand_name_element = parent_element.find_element(By.CLASS_NAME,'sc-51b852f7-21')
                        brand_name_title= brand_name_element.get_attribute('title')
                        brand_name = brand_name_title
                    except NoSuchElementException:
                        # Handle the case where the element is not found
                            brand_name = None

                    try:
                        price_element = parent_element.find_element(By.CLASS_NAME, 'oldPrice')
                        price_old = price_element.text.strip()
                    except NoSuchElementException:
                    # Handle the case where the element is not found
                        price_old = None

                    try:
                        price_element = parent_element.find_element(By.CLASS_NAME, 'amount')
                        price_new = price_element.text.strip()
                    except NoSuchElementException:
                    # Handle the case where the element is not found
                        price_new = None

                    try:
                        offer_element = parent_element.find_element(By.CLASS_NAME, 'discount')
                        offer = offer_element.text.strip()
                    except NoSuchElementException:
                    # Handle the case where the element is not found
                        offer = None
                    # info_element = parent_element.find_element(By.CLASS_NAME, 'sc-76e59b60-1')
                    # additional_info = info_element.text.strip()
                    # print(additional_info)

                    try:
                        link = parent_element.find_element(By.TAG_NAME, 'a').get_attribute("href")
                    except NoSuchElementException:
                    # Handle the case where the element is not found
                        link = None

                    Noon_data = {
                            'product_name': brand_name,
                            'old_price': price_old,
                            'current_price': price_new,
                            'offer': offer,
                            # 'additional_info': additional_info,
                            'URL': link
                        }

                    print(Noon_data)
                    data_list.append(Noon_data)
                current_page += 1


                # Break the loop if we have reached the last page
                if current_page > last_page_number:
                    break

            except NoSuchElementException:
                # Break the loop if there is no pagination element (e.g., on the last page)
                break
        df = pd.DataFrame(data_list)

        # Save the DataFrame to an Excel file with the provided download folder
        file_path = os.path.join(download_folder, f'{tab_name}.xlsx')
        df.to_excel(file_path, index=False)
        print(f"Data saved to: {file_path}")

def on_noon_link_page():
    base_url = base_url_entry.get()
    last_url = last_url_entry.get()
    tab_name = tab_name_entry.get()
    download_folder = download_folder_var.get()
    noon_link_page(base_url, last_url, tab_name, download_folder)

def on_noon_link_product():
    base_url = base_url_entry.get()
    last_url = last_url_entry.get()
    tab_name = tab_name_entry.get()
    download_folder = download_folder_var.get()
    noon_link_product(base_url, last_url, tab_name, download_folder)

def on_select_download_folder():
    folder_selected = filedialog.askdirectory()
    download_folder_var.set(folder_selected)

# Create the main window
root = Tk()
root.title("Noon Link Scraper")
# Set the window size
window_width = 500  # You can adjust this value
window_height = 200  # You can adjust this value
root.geometry(f"{window_width}x{window_height}")
# Create and pack labels, entries, and buttons
base_url_label = Label(root, text="Base URL:")
base_url_label.place(x=10, y=10)

base_url_entry = Entry(root)
base_url_entry.place(x=100, y=10)

last_url_label = Label(root, text="Last URL:")
last_url_label.place(x=10, y=40)

last_url_entry = Entry(root)
last_url_entry.place(x=100, y=40)

tab_name_label = Label(root, text="Tab Name:")
tab_name_label.place(x=10, y=70)

tab_name_entry = Entry(root)
tab_name_entry.place(x=100, y=70)

download_folder_label = Label(root, text="Download Folder:")
download_folder_label.place(x=10, y=100)

download_folder_var = StringVar()
download_folder_entry = Entry(root, textvariable=download_folder_var)
download_folder_entry.place(x=130, y=100)

download_folder_button = Button(root, text="Select Folder", command=on_select_download_folder)
download_folder_button.place(x=300, y=95)

noon_link_page_button = Button(root, text="Noon Link Page", command=on_noon_link_page)
noon_link_page_button.place(x=10, y=130)

noon_link_product_button = Button(root, text="Noon Link Product", command=on_noon_link_product)
noon_link_product_button.place(x=130, y=130)

# Run the Tkinter main loop
root.mainloop()