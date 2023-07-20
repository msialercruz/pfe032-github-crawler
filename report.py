#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor
import csv, os, time, json, requests
import matplotlib.pyplot as plt
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
def get_results():
    def get_result(notebook):
        nb_url, nb_path = notebook
        print(f"analyzing {nb_path}...")
        nb_size = int(os.path.getsize(nb_path))
        nb_size_fmt = sizeof_fmt(nb_size)
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

    with ThreadPoolExecutor(max_workers=2) as ex:
        return ex.map(get_result, notebooks)


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
        print(e)
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


def save_results():
    with open(results_filepath, "w+", encoding="utf-8") as f:
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
        for row in results:
            writer.writerow(row)


def generate_plots():
    with open(results_filepath, "r", encoding="utf-8") as f:
        _results = list(csv.reader(f))[1:]
    generate_exec_times_per_lines_plot(_results)
    generate_percentage_each_analysis_status_plot(_results)
    generate_percentage_each_leakage_type_plot(_results)
    generate_notebooks_by_leakages_quantity_plot(_results)


def generate_exec_times_per_lines_plot(_results):
    lines = [int(r[5]) for r in _results]
    exec_times = [float(r[7]) for r in _results]
    plt.xlabel("lines")
    plt.ylabel("execution time")
    plt.scatter(lines, exec_times)
    plt.title("Execution time per lines")
    plt.savefig(f"{plots_prefix}/01_exec_times_per_lines.png")


def generate_percentage_each_analysis_status_plot(_results):
    status_count = {}
    for r in _results:
        status_count[r[6]] = status_count[r[6]] + 1 if r[6] in status_count else 1
    labels = []
    sizes = []
    for k, v in status_count.items():
        labels.append(k)
        sizes.append(v)
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%")
    plt.title("Percentage of each analysis status")
    plt.savefig(f"{plots_prefix}/02_percentage_each_analysis_status.png")


def generate_percentage_each_leakage_type_plot(_results):
    leakages_count = {
        "Pre-processing leakages": 0,
        "Overlap leakages": 0,
        "No independence test data": 0,
    }
    notebooks_with_leakages = 0
    for r in _results:
        leakages_count["Pre-processing leakages"] += int(r[8])
        leakages_count["Overlap leakages"] += int(r[9])
        leakages_count["No independence test data"] += int(r[10])
        if int(r[8]) > 0 or int(r[9]) > 0 or int(r[10]) > 0:
            notebooks_with_leakages += 1
    labels = []
    sizes = []
    for k, v in leakages_count.items():
        labels.append(k)
        sizes.append(v)
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%")
    plt.title(
        f"Percentage of each leakage type (found in {notebooks_with_leakages} notebooks)"
    )
    plt.savefig(f"{plots_prefix}/03_percentage_each_leakage_type.png")


def generate_notebooks_by_leakages_quantity_plot(_results):
    notebooks_qt_leakages = {}
    notebooks_count = 0
    for r in _results:
        leakages = sum((int(l) for l in r[8:11]))
        if leakages > 0:
            notebooks_qt_leakages[leakages] = (
                notebooks_qt_leakages[leakages] + 1
                if leakages in notebooks_qt_leakages
                else 1
            )
            notebooks_count += 1
    labels = []
    sizes = []
    for k, v in notebooks_qt_leakages.items():
        labels.append(k)
        sizes.append(v)
    fig, ax = plt.subplots()
    ax.bar(labels, sizes)
    ax.set_ylabel("notebooks")
    ax.set_title(
        f"Notebooks by quantity of leakages (total of {notebooks_count} notebooks)"
    )
    plt.savefig(f"{plots_prefix}/04_notebooks_by_quantity_leakages.png")


timestamp = int(time.time())
results = get_results()
results_filepath = f"./notebooks/nb_results_{timestamp}.csv"
save_results()
plots_prefix = f"plots/{timestamp}"
os.makedirs(plots_prefix, exist_ok=True)
generate_plots()
