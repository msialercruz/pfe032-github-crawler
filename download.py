#!/bin/python3
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, unquote
import json, os, requests
from bs4 import BeautifulSoup

SEARCH_URL = "https://github.com/search?q=created%3A%3E2023-05-01+created%3A%3C2023-05-31+language%3A%22Jupyter+Notebook%22+license%3Amit+machine+learning&type=repositories&ref=advsearch"


def get_cookies():
    with open("cookies.txt", "r", encoding="utf-8") as f:
        return f.read().strip()


def get_headers():
    return {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": cookies,
    }


def get_max_page():
    res = requests.get(SEARCH_URL, headers=get_headers())
    soup = BeautifulSoup(res.text, "html.parser")
    pages = soup.select(".Pagination__Page-sc-cp45c9-0")
    if len(pages) == 0:
        raise Exception(f"no pages displayed, check url {SEARCH_URL}")
    _max_page = pages[-2].get_text()
    return int(_max_page)


def get_repos():
    _repos = []
    for page in range(1, max_page + 1):
        url = f"{SEARCH_URL}&p={page}"
        res = requests.get(url, headers=get_headers())
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.select(".Text-sc-17v1xeu-0.qaOIC.search-match")
        print(f"[{page:03d}/{max_page}] {len(links)} links found in {url}")
        for repo_link in links:
            _repos.append(repo_link.get_text().split("/"))
    return _repos


def get_notebooks():
    _notebooks = []
    _total = len(repos)
    for i, _repo in enumerate(repos):
        owner, repo = _repo
        url = f"https://github.com/search?q=repo%3A{owner}%2F{repo}+path%3A*.ipynb+fit&type=code"
        res = requests.get(url, headers=get_headers())
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.select(".Link__StyledLink-sc-14289xe-0.faoOkb")
        print(f"[{(i+1):03d}/{_total}] {len(links)} links found in {url}")
        for nb_link in links:
            url = urlparse(f"https://github.com{nb_link['href']}")
            if url.path != "":
                _notebooks.append(
                    (
                        f"https://raw.githubusercontent.com{url.path.replace('/blob', '')}",
                        f"https://github.com{url.path}",
                    )
                )
    return _notebooks


def download_notebooks():
    def _download_notebook(notebook):
        nb_raw_url, nb_url = notebook
        res = requests.get(nb_raw_url, headers=get_headers())
        text = res.text
        try:
            _json = json.loads(text)
        except ValueError:
            return

        # invalid
        if "cells" not in _json:
            return None
        _code_cells = (cell for cell in _json["cells"] if cell["cell_type"] == "code")
        if (
            len(list(_code_cells)) == 0
            or len(
                [cell for cell in _code_cells if "import tensorflow" in cell["source"]]
            )
            > 0
        ):
            return

        # valid
        filename = unquote(urlparse(nb_raw_url).path.split("/")[-1])
        size = len(text.encode("utf-8"))
        if size <= 10240:
            prefix = "./notebooks/sm"
        elif size <= 102400:
            prefix = "./notebooks/md"
        elif size > 102400:
            prefix = "./notebooks/lg"
        filepath = f"{prefix}/{filename}"
        with open(filepath, "w+", encoding="utf-8") as f:
            f.write(text)
        return (nb_url, filepath)

    os.makedirs("./notebooks/sm", exist_ok=True)
    os.makedirs("./notebooks/md", exist_ok=True)
    os.makedirs("./notebooks/lg", exist_ok=True)

    if len(notebooks) == 0:
        raise Exception("No notebooks found")

    with ThreadPoolExecutor() as ex:
        nb_locations = ex.map(_download_notebook, notebooks)

    with open("./notebooks/nb_locations.json", "w+", encoding="utf-8") as f:
        json.dump(
            [nb_location for nb_location in nb_locations if nb_location is not None], f
        )


cookies = get_cookies()
max_page = get_max_page()
print("getting repos...")
repos = get_repos()
print("\ngetting notebooks...")
notebooks = get_notebooks()
print("\ndownloading notebooks...")
download_notebooks()
