from bs4 import BeautifulSoup
import requests
import io



respone = requests.get("https://www.empireonline.com/movies/features/best-movies-2/")
soup = BeautifulSoup(respone.text, "html.parser")
page_encode = soup.encode("utf-8")

titles = soup.find_all(name="h3", class_ = "title")

titles_texts = [title.getText().encode("utf-8") for title in titles]

titles_texts[-1] = "1) The Godfather"
movies = titles_texts[::-1]




with open("100Movies", "w") as file:
    for movie in movies:
        file.write(f"{movie}\n")