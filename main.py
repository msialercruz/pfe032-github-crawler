#!/bin/python3
import os, subprocess, csv
import db
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, unquote
from bs4 import BeautifulSoup
from utils import run_sh

SEARCH_REPOS_BASE_URL = "https://github.com/search?q=created%3A%3E2023-05-01+created%3A%3C2023-05-31+language%3A%22Jupyter+Notebook%22+license%3Amit+machine+learning&type=repositories&ref=advsearch"

def file_count(directory, ext=None):
    files = os.listdir(directory) if not ext else [f for f in os.listdir() if f.endswith(ext)]
    return len(files)

def get_max_page():
    if (not os.path.isfile("html/max_page.html")):
        run_sh("getmaxpage", SEARCH_REPOS_BASE_URL)
    with open("html/max_page.html", "r") as f:
        html_doc = f.read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        pages = soup.select(".Pagination__Page-sc-cp45c9-0")
        if (len(pages) > 0):
            max_page = pages[-2].get_text()
            return int(max_page)
        else:
            raise Exception(f"no pages displayed, check url {SEARCH_REPOS_BASE_URL}")

def get_repos(html_path):
    if (file_count("html/repos") == 0):
        run_sh("getrepos", SEARCH_REPOS_BASE_URL, str(max_page))
    repos = []
    for i in range(1, max_page + 1):
        filepath = f"html/repos/page_{i}.html"
        with open(filepath, "r") as f:
            html_doc = f.read()
            soup = BeautifulSoup(html_doc, 'html.parser')
            links = soup.select(".Text-sc-17v1xeu-0.qaOIC.search-match")
            if (len(links) > 0):
                for repo_link in links:
                    repos.append(repo_link.get_text().split("/"))
            else:
                print(f"No links found in {filepath}")
    return repos

def get_notebooks(repos):
    repo_infos = []
    if (file_count("html/notebooks/", "ipynb") == 0):
        for owner, repo in repos:
            info = run_sh("getnb", owner, repo).strip().split("\n")
            if len(info) == 3:
                repo_infos.append(info)
            else:
                print(info)
    notebooks = []
    for filepath, owner, repo in repo_infos:
        with open(filepath, "r") as f:
            html_doc = f.read()
            soup = BeautifulSoup(html_doc, 'html.parser')
            links = soup.select(".Link__StyledLink-sc-14289xe-0.faoOkb")
            if (len(links) > 0):
                for nb_link in links:
                    url = urlparse(f"https://github.com{nb_link['href']}")
                    if (url.path != ""):
                        repo_url = f"https://github.com/{owner}/{repo}"
                        notebooks.append((url.path.replace('/blob', ''), url.path))
            else:
                print(f"No links found in {filepath}")
    return notebooks

def dl_notebooks(notebooks):

    with ThreadPoolExecutor() as executor:
        executor.map(run_sh,
                     ["dlnb" for _ in notebooks],
                     [nb_raw_url for nb_raw_url, _ in notebooks])

    db.clear_notebooks()
    notebooks = [(f"https://github.com{nb_url}", unquote(f"./notebooks/{nb_url.split('/')[-1]}")) for nb_raw_url, nb_url in notebooks]
    db.insert_notebooks(notebooks)

    # moving notebooks in folders
    run_sh("mv_invalid")
    run_sh("mv_valid")

max_page = get_max_page()
repos = get_repos(max_page)
notebooks = get_notebooks(repos)
dl_notebooks(notebooks)
