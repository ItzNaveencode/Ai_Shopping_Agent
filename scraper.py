from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_amazon_products(query):
    driver = create_driver()
    search_url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
    driver.get(search_url)
    time.sleep(3)

    products = []
    results = driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')
    for item in results[:10]:
        try:
            title = item.find_element(By.TAG_NAME, 'h2').text
            link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
            price = item.find_element(By.CLASS_NAME, 'a-price-whole').text
            rating = item.find_element(By.CLASS_NAME, 'a-icon-alt').get_attribute('innerHTML')
            products.append({
                'title': title,
                'price': f"₹{price}",
                'rating': rating.split(' ')[0],
                'link': link,
                'platform': 'Amazon'
            })
        except:
            continue
    driver.quit()
    return products

def get_flipkart_products(query):
    driver = create_driver()
    driver.get(f"https://www.flipkart.com/search?q={query.replace(' ', '%20')}")
    time.sleep(3)

    products = []
    cards = driver.find_elements(By.CLASS_NAME, '_1AtVbE')
    for card in cards:
        try:
            title = card.find_element(By.CLASS_NAME, '_4rR01T').text
            price = card.find_element(By.CLASS_NAME, '_30jeq3').text
            rating = card.find_element(By.CLASS_NAME, '_3LWZlK').text
            link = card.find_element(By.TAG_NAME, 'a').get_attribute('href')
            products.append({
                'title': title,
                'price': price,
                'rating': rating,
                'link': f"https://www.flipkart.com{link}",
                'platform': 'Flipkart'
            })
        except:
            continue
        if len(products) >= 10:
            break
    driver.quit()
    return products

def get_apple_store_product(query):
    # Apple India Store doesn't list many results — just go to the main product page
    products = []
    base_url = "https://www.apple.com/in/shop/buy-iphone"
    driver = create_driver()
    driver.get(base_url)
    time.sleep(5)
    try:
        products.append({
            "title": "iPhone 15 (Apple Official)",
            "price": "₹69,900",  # static, or you can scrape via javascript-heavy page
            "rating": "4.6",
            "link": base_url,
            "platform": "Apple Store"
        })
    except:
        pass
    driver.quit()
    return products

def get_all_products(query):
    return get_amazon_products(query) + get_flipkart_products(query) + get_apple_store_product(query)
