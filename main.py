#!/bin/python3
import os, subprocess
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def run_sh(filename, args):
    if (len(args) == 0):
        args = []
    res = subprocess.check_output(["sh", filename] + args)

def file_count(directory):
    return len(os.listdir(directory))

def get_repos():
    if (file_count("html/repos/") == 0):
        run_sh("getrepos.sh")
    repos = []
    for i in range(1, 8):
        with open(f"html/repos/page_{i}.html", "r") as f:
            html_doc = f.read()
            soup = BeautifulSoup(html_doc, 'html.parser')
            for repo in soup.select(".Text-sc-17v1xeu-0.qaOIC.search-match"):
                repos.append(repo.get_text().split("/"))
    return repos

def get_notebooks(repos):
    if (file_count("html/notebooks/") == 0):
        for owner, repo in repos:
            run_sh("getnb.sh", [owner, repo])
    notebooks = []
    for nb_html_filename in os.listdir("html/notebooks/"):
        with open(f"html/notebooks/{nb_html_filename}", "r") as f:
            html_doc = f.read()
            soup = BeautifulSoup(html_doc, 'html.parser')
            for nb in soup.select(".Link__StyledLink-sc-14289xe-0.faoOkb"):
                url = urlparse(f"https://github.com{nb['href']}")
                if (url.path != ""):
                    notebooks.append(url.path)
    return notebooks

def dl_notebooks(notebooks):
    for nb_path in notebooks:
        run_sh("dlnb.sh", [nb_path])

repos = get_repos()
notebooks = get_notebooks(repos)
dl_notebooks(notebooks)
