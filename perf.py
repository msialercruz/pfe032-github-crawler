#!/usr/bin/env python3
import csv, os, json
import db
from pathlib import Path
from bs4 import BeautifulSoup
from utils import run_sh, time_decorator, sizeof_fmt

@time_decorator
def analyze_nb(nb_path, report_path):
    nb_name = run_sh("upload", nb_path)
    return run_sh("analyze", nb_name, report_path)


def analyze_all():
    valid_notebooks = db.get_valid_notebooks()
    for notebook in valid_notebooks:
        nb_path = notebook[2]
        print(f"analyzing {nb_path}...")
        nb_id = notebook[0]
        category_sz = nb_path.split("/")[2]
        report_path = f"./reports/{category_sz}/{Path(nb_path).stem}.json"
        nb_size = sizeof_fmt(int(os.path.getsize(nb_path)))
        httpcode, analysis_time = analyze_nb(nb_path, report_path)
        json_body = read_report(report_path)
        leakages = extract_leakages(json_body)
        httpcode = float(httpcode)
        analysis_status = "Success"
        if (httpcode != 200):
            if (analysis_time >= 300 and httpcode == 500):
                analysis_status = "Timeout"
            else:
                analysis_status = json_body
        db.update_nb_analysis_data(nb_id, nb_size, analysis_status, analysis_time, *leakages)


def read_report(report_path):
    with open(report_path, "r") as f:
        return f.read()


# {
#   "pre-processing leakage": {
#     "# detected": 0,
#     "location": []
#   },
#   "overlap leakage": {
#     "# detected": 0,
#     "location": []
#   },
#   "no independence test data": {
#     "# detected": 0,
#     "location": []
#   }
# }
def extract_leakages(json_body):
    try:
        _json = json.loads(json_body)
        overlap_leakages = int(_json["overlap leakage"]["# detected"])
        pre_processing_leakages = int(_json["pre-processing leakage"]["# detected"])
        no_independence_test_data = int(_json["no independence test data"]["# detected"])
        return (pre_processing_leakages, overlap_leakages, no_independence_test_data)
    except Exception as e:
        return (0, 0, 0)


def save_as_csv():
    valid_notebooks = db.get_valid_notebooks()
    with open("./reports/notebook_analysis.csv", "w+") as f:
        writer = csv.writer(f)
        writer.writerow(["Url", "Location", "File size", "Analysis status", "Analysis time", "Pre-processing leakages", "Overlap leakages", "No independence test data"])
        for notebook in valid_notebooks:
            writer.writerow(notebook[1:])


analyze_all()
save_as_csv()
