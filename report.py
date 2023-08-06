#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor
import csv, os, time, json, requests
import matplotlib.pyplot as plt
from utils import time_decorator, sizeof_fmt


# pylint: disable=consider-using-with
@time_decorator
def analyze_nb(nb_path):
    files = {"file": open(nb_path, "rb")}
    return requests.post("http://localhost:5000/analyze", files=files)


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
        # is an error
        if status_code == 200:
            content_infos = extract_content_infos(nb_path)
            analysis_status = "Success"
            leakages = extract_leakages(text)
        else:
            content_infos = (0, 0)
            analysis_status = (
                "Timeout" if analysis_time >= 300 else extract_err_msg(text)
            )
            leakages = (0, 0, 0)
        return (
            nb_url,
            nb_path,
            nb_size,
            nb_size_fmt,
            *content_infos,
            analysis_status,
            analysis_time,
            *leakages,
        )

    with open("./notebooks/nb_locations.json", "r", encoding="utf-8") as f:
        notebooks = json.loads(f.read())

    with ThreadPoolExecutor(max_workers=4) as ex:
        return ex.map(get_result, notebooks[0:4])


def extract_err_msg(res_json):
    try:
        _json = json.loads(res_json)
        return _json["message"]
    except Exception as e:
        print("err extracting err message: ", e)
        return "ukwnokn"


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
        print("err extracting leakages: ", e)
        return (0, 0, 0)


def extract_content_infos(nb_path):
    try:
        with open(nb_path, "r", encoding="utf-8") as f:
            nb_content = f.read()
        _json = json.loads(nb_content)
        codecells = [cell for cell in _json["cells"] if cell["cell_type"] == "code"]
        codelines = sum(
            (
                len([line for line in cell["source"] if not line.startswith("#")])
                for cell in codecells
            )
        )
        return (len(codecells), codelines)
    except Exception as e:
        print("err extracting content infos: ", e)
        return (0, 0)


def save_results():
    with open(results_filepath, "w+", newline="", encoding="utf-8") as f:
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
    generate_percentage_each_analysis_status_plot(_results)
    generate_exec_times_per_lines_plot(_results)
    generate_exec_times_per_cells_plot(_results)
    generate_percentage_each_leakage_type_plot(_results)
    generate_notebooks_by_leakages_quantity_plot(_results)


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
    patches = ax.pie(sizes, labels=labels, autopct="%1.1f%%")
    for text in patches[1]:
        text.set_wrap(True)
    plt.title("Percentage of each analysis status")
    plt.savefig(f"{plots_prefix}/01_percentage_each_analysis_status.png")
    plt.close()


def generate_exec_times_per_lines_plot(_results):
    _results = [r for r in _results if r[6] != "Timeout"]
    lines = [int(r[5]) for r in _results]
    exec_times = [float(r[7]) for r in _results]
    plt.xlabel("# Lines")
    plt.ylabel("Execution time (seconds)")
    plt.scatter(lines, exec_times)
    plt.title("Execution time per lines")
    plt.savefig(f"{plots_prefix}/02_exec_times_per_lines.png")
    plt.close()


def generate_exec_times_per_cells_plot(_results):
    _results = [r for r in _results if r[6] != "Timeout"]
    cells = [int(r[4]) for r in _results]
    exec_times = [float(r[7]) for r in _results]
    plt.xlabel("# Cells")
    plt.ylabel("Execution time (seconds)")
    plt.scatter(cells, exec_times)
    plt.title("Execution time per cells")
    plt.savefig(f"{plots_prefix}/03_exec_times_per_cells.png")
    plt.close()


def generate_percentage_each_leakage_type_plot(_results):
    leakages_count = {
        "Pre-processing leakages": 0,
        "Overlap leakages": 0,
        "No independence test data": 0,
    }
    notebooks_count = len(_results)
    notebooks_with_leakages_count = 0
    for r in _results:
        leakages_count["Pre-processing leakages"] += int(r[8])
        leakages_count["Overlap leakages"] += int(r[9])
        leakages_count["No independence test data"] += int(r[10])
        if int(r[8]) > 0 or int(r[9]) > 0 or int(r[10]) > 0:
            notebooks_with_leakages_count += 1
    labels = []
    sizes = []
    for k, v in leakages_count.items():
        labels.append(k)
        sizes.append(v)
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%")
    plt.title(
        f"Percentage of each leakage type (found in {notebooks_with_leakages_count} out of {notebooks_count} notebooks)"
    )
    plt.savefig(f"{plots_prefix}/04_percentage_each_leakage_type.png")
    plt.close()


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
    ax.set_ylabel("# Notebooks")
    ax.set_title(
        f"Notebooks by quantity of leakages (total of {notebooks_count} notebooks)"
    )

    # inspired by: https://sharkcoder.com/data-visualization/mpl-bar-chart
    for rect in ax.patches:
        y = rect.get_height()
        x = rect.get_x() + rect.get_width() / 2
        ax.annotate(
            y, (x, y), xytext=(0, 10), textcoords="offset points", ha="center", va="top"
        )
    plt.savefig(f"{plots_prefix}/05_notebooks_by_quantity_leakages.png")
    plt.close()


timestamp = int(time.time())
results = get_results()
results_filepath = f"./notebooks/nb_results_{timestamp}.csv"
save_results()
plots_prefix = f"plots/{timestamp}"
os.makedirs(plots_prefix, exist_ok=True)
generate_plots()
