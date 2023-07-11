#!/bin/python3
import db, requests
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, unquote
from bs4 import BeautifulSoup

SEARCH_REPOS_BASE_URL = "https://github.com/search?q=created%3A%3E2023-05-01+created%3A%3C2023-05-31+language%3A%22Jupyter+Notebook%22+license%3Amit+machine+learning&type=repositories&ref=advsearch"

def get_cookies():
    with open("cookies.txt", "r") as f:
        return f.read()

def get_headers():
    return {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': cookies
    }

def get_max_page():
    res = requests.get(SEARCH_REPOS_BASE_URL, headers=get_headers())
    soup = BeautifulSoup(res.text, 'html.parser')
    pages = soup.select(".Pagination__Page-sc-cp45c9-0")
    if (len(pages) > 0):
        max_page = pages[-2].get_text()
        return int(max_page)
    else:
        raise Exception(f"no pages displayed, check url {SEARCH_REPOS_BASE_URL}")

def get_repos():
    repos = []
    for i in range(1, max_page + 1):
        url = f"{SEARCH_REPOS_BASE_URL}&p={i}"
        res = requests.get(url, headers=get_headers())
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select(".Text-sc-17v1xeu-0.qaOIC.search-match")
        if (len(links) > 0):
            for repo_link in links:
                repos.append(repo_link.get_text().split("/"))
        else:
            print(f"No links found in {url}")
    return repos

def get_notebooks():
    notebooks = []
    for owner, repo in repos:
        url = f"https://github.com/search?q=repo%3A{owner}%2F{repo}+path%3A*.ipynb+fit&type=code"
        res = requests.get(url, headers=get_headers())
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select(".Link__StyledLink-sc-14289xe-0.faoOkb")
        if (len(links) == 0):
            print(f"No links found in {url}")
            continue
        for nb_link in links:
            url = urlparse(f"https://github.com{nb_link['href']}")
            if (url.path != ""):
                notebooks.append((f"https://raw.githubusercontent.com{url.path.replace('/blob', '')}",
                                  f"https://github.com{url.path}"))
    return notebooks


def dl_notebooks():
    def dl_notebook(notebook):
        nb_raw_url, _ = notebook 
        res = requests.get(nb_raw_url, headers=get_headers())
        filepath = f"./notebooks/{urlparse(unquote(nb_raw_url)).path.split('/')[-1]}"
        with open(filepath, "w+") as f:
            f.write(res.text)

    with ThreadPoolExecutor() as ex:
        ex.map(dl_notebook, notebooks)

    # db.clear_notebooks()
    # TODO: change this
    # notebooks = [(f"https://github.com{nb_url}", unquote(f"./notebooks/{nb_url.split('/')[-1]}")) for nb_raw_url, nb_url in notebooks]
    # db.insert_notebooks(notebooks)
    # moving notebooks in folders
    # TODO: implement python equivalent
    # run_sh("mv_invalid")
    # TODO: implement python equivalent
    # run_sh("mv_valid")

cookies = get_cookies()
max_page = get_max_page()
print("getting repos...")
repos = get_repos()
print("getting notebooks...")
notebooks = get_notebooks()
print("downloading notebooks...")
dl_notebooks()
