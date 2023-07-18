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
    def _get_repos(page):
        page_repos = []
        url = f"{SEARCH_URL}&p={page}"
        res = requests.get(url, headers=get_headers())
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.select(".Text-sc-17v1xeu-0.qaOIC.search-match")
        if len(links) > 0:
            for repo_link in links:
                page_repos.append(repo_link.get_text().split("/"))
        else:
            print(f"No links found in {url}")
        return page_repos

    with ThreadPoolExecutor() as ex:
        _repos = ex.map(_get_repos, (i for i in range(1, max_page + 1)))
        print(len(_repos))
        return [repo for page_repos in _repos for repo in page_repos]


def get_notebooks():
    def _get_notebooks(_repo):
        repo_notebooks = []
        owner, repo = _repo
        url = f"https://github.com/search?q=repo%3A{owner}%2F{repo}+path%3A*.ipynb+fit&type=code"
        res = requests.get(url, headers=get_headers())
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.select(".Link__StyledLink-sc-14289xe-0.faoOkb")
        if len(links) == 0:
            print(f"no links found in {url}")
        else:
            for nb_link in links:
                url = urlparse(f"https://github.com{nb_link['href']}")
                if url.path != "":
                    repo_notebooks.append(
                        (
                            f"https://raw.githubusercontent.com{url.path.replace('/blob', '')}",
                            f"https://github.com{url.path}",
                        )
                    )
        return repo_notebooks

    with ThreadPoolExecutor() as ex:
        _notebooks = ex.map(_get_notebooks, repos)
        return [
            notebook for repo_notebooks in _notebooks for notebook in repo_notebooks
        ]


def download_notebooks():
    def _download_notebook(notebook):
        nb_raw_url, nb_url = notebook
        res = requests.get(nb_raw_url, headers=get_headers())
        text = res.text
        try:
            _json = json.loads(text)
        except ValueError as e:
            print(f"not json {text}")
            # pass

        # invalid
        if (
            not _json
            or "import tensorflow" in text
            or len([cell for cell in _json["cells"] if cell["cell_type"] == "code"])
            == 0
        ):
            return None

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
print("getting notebooks...")
notebooks = get_notebooks()
print("downloading notebooks...")
download_notebooks()
