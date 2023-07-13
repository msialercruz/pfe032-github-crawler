#!/usr/bin/env python3
import csv, os, json
import requests
from utils import time_decorator, sizeof_fmt


# pylint: disable=consider-using-with
@time_decorator
def analyze_nb(nb_path):
    files = {"file": open(nb_path, "rb")}
    res = requests.post("http://localhost:5000/upload", files=files)
    nb_name = res.text
    res = requests.post(f"http://localhost:5000/analyze/{nb_name}")
    return res


def analyze_all():
    with open("./notebooks/nb_locations.json", "r", encoding="utf-8") as f:
        notebooks = json.loads(f.read())
    _results = []
    for nb_url, nb_path in notebooks:
        print(f"analyzing {nb_path}...")
        category_sz = nb_path.split("/")[1]
        nb_size = int(os.path.getsize(nb_path))
        nb_size_fmt = sizeof_fmt(int(os.path.getsize(nb_path)))
        res, analysis_time = analyze_nb(nb_path)
        text = res.text
        status_code = res.status_code
        leakages = extract_leakages(text)
        analysis_status = "Success"
        if status_code != 200:
            if analysis_time >= 300 and status_code == 500:
                analysis_status = "Timeout"
            else:
                analysis_status = text
        _results.append(
            (
                nb_url,
                nb_path,
                nb_size,
                nb_size_fmt,
                analysis_status,
                analysis_time,
                *leakages,
            )
        )
    return _results


def extract_leakages(nb_json):
    try:
        _json = json.loads(nb_json)
        overlap_leakages = int(_json["overlap leakage"]["# detected"])
        pre_processing_leakages = int(_json["pre-processing leakage"]["# detected"])
        no_independence_test_data = int(
            _json["no independence test data"]["# detected"]
        )
        return (pre_processing_leakages, overlap_leakages, no_independence_test_data)
    except Exception as e:
        return (0, 0, 0)


def save_as_csv():
    with open("./notebooks/notebook_analysis.csv", "w+", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Url",
                "Location",
                "File size",
                "File size formatted",
                "Analysis status",
                "Analysis time",
                "Pre-processing leakages",
                "Overlap leakages",
                "No independence test data",
            ]
        )
        for result in results:
            writer.writerow(result)


results = analyze_all()
save_as_csv()
