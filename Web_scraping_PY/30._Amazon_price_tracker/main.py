from bs4 import BeautifulSoup
import requests
import smtplib


# Use http://myhttpheader.com/ to find headers !

headers = {
    "User-Agent": "XXXXXXXXXXXXXXX",
    "Accept-Language": "XXXXXXXXXXXX"
}

response = requests.get("https://www.amazon.com/Creality-Printing-Certified-MKK-220x220x250mm/dp/B085XZHGYM/ref=sr_1_10?dchild=1&keywords=amazon+sapphire+pro+3d+printer&qid=1608933804&sr=8-10", headers=headers)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")

price_tag = soup.find(name="span", id="priceblock_saleprice")
price_text = price_tag.getText()
price_float = float(price_text[1:])


if price_float <= 236:

    my_email = "EMAIL"
    password = "PASSWORD"


    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user = my_email, password=password)
        connection.sendmail(
            from_addr = my_email,
            to_addrs= "RECIEVER ADRESS",
            msg = f"Subject:Price Alert!\n\nPrice of product that you are looking for is very low ----> {price_text}."
        )
    
