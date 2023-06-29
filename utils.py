import subprocess, time

def run_sh(filename, *args):
    # print(["sh", f"scripts/{filename}.sh"] + list(args))
    return subprocess.check_output(["sh", f"scripts/{filename}.sh"] + list(args))

def time_decorator(func):
    def inner(*args, **kwargs):
        st = time.time()
        ret = func(*args,  **kwargs)
        ed = time.time()
        return ret, ed - st
    return inner
