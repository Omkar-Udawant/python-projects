import os
import smtplib
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# ====================== CONFIGURATION ======================

load_dotenv()

URL = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
BUY_PRICE = 70

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/84.0.4147.125 Safari/537.36"
    ),
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

SMTP_ADDRESS = os.environ["SMTP_ADDRESS"]
EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

# ====================== FUNCTIONS ======================

def get_product_page(url: str) -> BeautifulSoup:
    """Fetch Amazon product page and return parsed HTML."""
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")


def get_price_and_title(soup: BeautifulSoup) -> tuple[float, str, str]:
    """Extract product price, numeric price, and title."""
    price_text = soup.find(class_="a-offscreen").get_text()
    price_value = float(price_text.replace("$", ""))
    title = soup.find(id="productTitle").get_text().strip()
    return price_text, price_value, title


def send_email_alert(title: str, price: str):
    """Send email notification when price drops."""
    message = f"{title} is now available for {price}!\n\n{URL}"

    with smtplib.SMTP(SMTP_ADDRESS, 587) as connection:
        connection.starttls()
        connection.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        connection.sendmail(
            from_addr=EMAIL_ADDRESS,
            to_addrs=EMAIL_ADDRESS,
            msg=f"Subject:Amazon Price Alert!\n\n{message}".encode("utf-8")
        )


# ====================== MAIN LOGIC ======================

def main():
    soup = get_product_page(URL)

    price_text, price_value, title = get_price_and_title(soup)

    print(f"Product: {title}")
    print(f"Current Price: {price_value}")

    if price_value < BUY_PRICE:
        send_email_alert(title, price_text)


if __name__ == "__main__":
    main()
