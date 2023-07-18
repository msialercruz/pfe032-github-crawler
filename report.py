#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor
import csv, os, json, requests
from utils import time_decorator, sizeof_fmt


# pylint: disable=consider-using-with
@time_decorator
def analyze_nb(nb_path):
    files = {"file": open(nb_path, "rb")}
    res = requests.post("http://localhost:5000/upload", files=files)
    nb_name = res.text
    res = requests.get(f"http://localhost:5000/analyze/{nb_name}")
    return res


# pylint: disable=too-many-locals
def analyze_all():
    def get_analysis_result(notebook):
        nb_url, nb_path = notebook
        print(f"analyzing {nb_path}...")
        category_sz = nb_path.split("/")[1]
        nb_size = int(os.path.getsize(nb_path))
        nb_size_fmt = sizeof_fmt(int(os.path.getsize(nb_path)))
        res, analysis_time = analyze_nb(nb_path)
        text = res.text
        status_code = res.status_code
        with open(nb_path, "r", encoding="utf-8") as f:
            nb_content = f.read()
        _cells_info = cells_info(nb_content)
        leakages = extract_leakages(text)
        analysis_status = "Success"
        if status_code != 200:
            if analysis_time >= 300 and status_code == 500:
                analysis_status = "Timeout"
            else:
                analysis_status = text
        return (
            nb_url,
            nb_path,
            nb_size,
            nb_size_fmt,
            *_cells_info,
            analysis_status,
            analysis_time,
            *leakages,
        )

    with open("./notebooks/nb_locations.json", "r", encoding="utf-8") as f:
        notebooks = json.loads(f.read())

    with ThreadPoolExecutor(2) as ex:
        return ex.map(get_analysis_result, notebooks)


def extract_leakages(res_json):
    try:
        _json = json.loads(res_json)
        overlap_leakages = int(_json["overlap leakage"]["# detected"])
        pre_processing_leakages = int(_json["pre-processing leakage"]["# detected"])
        no_independence_test_data = int(
            _json["no independence test data"]["# detected"]
        )
        return (pre_processing_leakages, overlap_leakages, no_independence_test_data)
    except Exception as e:
        return (0, 0, 0)


def cells_info(nb_json):
    try:
        _json = json.loads(nb_json)
        codecells = [cell for cell in _json["cells"] if cell["cell_type"] == "code"]
        codelines = sum(
            (
                len([line for line in cell["source"] if not line.startswith("#")])
                for cell in codecells
            )
        )
        return (len(codecells), codelines)
    except Exception as e:
        print(e)
        return (0, 0)


def save_as_csv():
    with open("./notebooks/nb_report.csv", "w+", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Url",
                "Location",
                "File size",
                "File size formatted",
                "Code cells",
                "Code lines",
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
