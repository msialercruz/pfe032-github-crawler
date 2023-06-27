#!/usr/bin/env python3

import os
from utils import run_sh, time_decorator

@time_decorator
def analyze_nb(nb_path, report_path):
    nb_name = run_sh("upload", nb_path).decode('utf-8')
    run_sh("analyze", nb_name, report_path).decode('utf-8')

# call analyze.sh
# calc time 
# save html
# check what nb has leakages (scrap report)
def analyze_all():
    sizes = ["small", "medium", "large"]
    for sz in sizes:
        for nb_name in os.listdir(f"notebooks/{sz}"):
            nb_path = f"notebooks/{sz}/{nb_name}"
            report_path = f"reports/{sz}/{nb_name[:-6]}.html"
            print(nb_path, report_path)
            # _, t = analyze_nb(nb_path, report_path)

analyze_all()