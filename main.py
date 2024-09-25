import requests
from bs4 import BeautifulSoup
import smtplib
from dotenv import load_dotenv
import os

PRODUCT_URL = "https://www.amazon.com/Monopoly-Sparkle-Glittery-Pearlescent-Exclusive/dp/B09R41HWR6/ref=pd_rhf_se_s_pd_sbs_rvi_d_sccl_1_2/133-7160771-6099207?pd_rd_w=6wMgv&content-id=amzn1.sym.46e2be74-be72-4d3f-86e1-1de279690c4e&pf_rd_p=46e2be74-be72-4d3f-86e1-1de279690c4e&pf_rd_r=NK2PMK36TYDXVRNEQN0W&pd_rd_wg=EMSLL&pd_rd_r=c8db78fd-a129-4c00-acc9-071a2e2bfe07&pd_rd_i=B09R41HWR6&psc=1"
TARGET_PRICE = 15

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept-Language": "en_US"}
product_html = requests.get(PRODUCT_URL, headers=headers).text

soup = BeautifulSoup(product_html, "html.parser")
try:
    price_whole_tag = soup.select(selector="span.a-price-whole")[1]
    price_fraction_tag = soup.select(selector="span.a-price-fraction")[1]
    product_price = float(f"{price_whole_tag.getText()}{price_fraction_tag.getText()}")
    print(product_price)
except IndexError:
    print("error")
    exit(0)

if product_price <= 30:
    load_dotenv()
    user_email = os.getenv("EMAIL")
    user_password = os.getenv("EMAIL_PASSWORD")
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=user_email, password=user_password)
    connection.sendmail(from_addr=user_email, to_addrs=user_email,
                        msg=f"Subject:Amazon Alert\n\nHurry up! The price of {PRODUCT_URL} is {product_price}!!!")
    connection.close()
