#!/usr/bin/env python3
import csv, os, math
from bs4 import BeautifulSoup
from utils import run_sh, time_decorator
# from concurrent.futures import ThreadPoolExecutor

@time_decorator
def analyze_nb(nb_path, report_path):
    nb_name = run_sh("upload", nb_path)
    return run_sh("analyze", nb_name, report_path)

# taken from: https://gist.github.com/cbwar/d2dfbc19b140bd599daccbe0fe925597
def sizeof_fmt(num, suffix='B'):
    magnitude = int(math.floor(math.log(num, 1024)))
    val = num / math.pow(1024, magnitude)
    if magnitude > 7:
        return '{:.1f}{}{}'.format(val, 'Yi', suffix)
    return '{:3.1f}{}{}'.format(val, ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi'][magnitude], suffix)

def analyze_all():
    sizes = ["sm", "md", "lg"]
    prefix_nb = "notebooks/valid"
    results = []
    for sz in sizes:
        for nb_name in os.listdir(f"{prefix_nb}/{sz}/py"):
            nb_path = f"{prefix_nb}/{sz}/py/{nb_name}"
            nb_size = sizeof_fmt(int(os.path.getsize(nb_path)))
            report_path = f"reports/{sz}/{nb_name[:-3]}.html"
            print(f"analyzing {nb_path}...")
            httpcode, t = analyze_nb(nb_path, report_path)
            httpcode = float(httpcode)
            status = "Success"
            if (httpcode != 200):
                if (t >= 300 and httpcode == 500):
                    status = "Timeout!"
                else:
                    with open(report_path, "r") as f:
                        status = f.read()
            leakages = extract_leakages(report_path)
            results.append((nb_name, nb_size, status, t) + leakages)
    return results

def extract_leakages(report_path):
    with open(report_path, "r") as f:
        try:
            html_doc = f.read()
            soup = BeautifulSoup(html_doc, 'html.parser')
            table = soup.select_one("table.sum")
            if (not table):
                raise Exception("No table found")
            pre_processing_leakages = int(table.select_one("tr:nth-child(2) td:nth-child(2)").get_text())
            overlap_leakages = int(table.select_one("tr:nth-child(3) td:nth-child(2)").get_text())
            no_independence_test_data = int(table.select_one("tr:nth-child(4) td:nth-child(2)").get_text())
            return (pre_processing_leakages,
                    overlap_leakages,
                    no_independence_test_data)
        except Exception as e:
            print(str(e))
            return (0, 0, 0)

def save_results(results):
    with open("./reports/analyze_report.csv", "w+") as f:
        writer = csv.writer(f)
        writer.writerow(("Notebook", "Notebook size", "Analysis status", "Analyze time", "Pre-processing leakages", "Overlap leakages", "No independence test data"))
        [writer.writerow(result) for result in results]

results = analyze_all()
save_results(results)
