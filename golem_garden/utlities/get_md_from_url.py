import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://github.com/Textualize/textual/tree/main/docs/widgets"

def read_markdown_files(url: str) -> str:
    response = requests.get(url)
    if response.status_code != 200:
        print("Error: Failed to fetch the URL.")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a", href=True)

    markdown_content = []

    for link in links:
        if link["href"].endswith(".md"):
            raw_url = link["href"].replace("blob", "raw")
            file_url = urljoin(url, raw_url)
            file_response = requests.get(file_url)
            if file_response.status_code == 200:
                markdown_content.append(file_response.text)

    return "\n".join(markdown_content)

if __name__ == "__main__":
    content = read_markdown_files(url)
    print(content)
