#!/bin/python3
import os, subprocess
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from utils import run_sh

def file_count(directory):
    return len(os.listdir(directory))

def get_repos():
    max_page = 15
    if (file_count("html/repos/") == 0):
        run_sh("getrepos", str(max_page))
    repos = []
    for i in range(1, max_page + 1):
        with open(f"html/repos/page_{i}.html", "r") as f:
            html_doc = f.read()
            soup = BeautifulSoup(html_doc, 'html.parser')
            for repo_link in soup.select(".Text-sc-17v1xeu-0.qaOIC.search-match"):
                repos.append(repo_link.get_text().split("/"))
    return repos

def get_notebooks(repos):
    if (file_count("html/notebooks/") == 0):
        for owner, repo in repos:
            run_sh("getnb", owner, repo)
    notebooks = []
    for nb_html_filename in os.listdir("html/notebooks/"):
        with open(f"html/notebooks/{nb_html_filename}", "r") as f:
            html_doc = f.read()
            soup = BeautifulSoup(html_doc, 'html.parser')
            for nb_link in soup.select(".Link__StyledLink-sc-14289xe-0.faoOkb"):
                url = urlparse(f"https://github.com{nb_link['href']}")
                if (url.path != ""):
                    notebooks.append(url.path.replace('/blob', ''))
    return notebooks

def dl_notebooks(notebooks):
    for nb_path in notebooks:
        run_sh("dlnb", nb_path)

repos = get_repos()
notebooks = get_notebooks(repos)
dl_notebooks(notebooks)