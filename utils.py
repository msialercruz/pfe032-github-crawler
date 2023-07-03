import subprocess, time, math

def run_sh(filename, *args):
    # print(["sh", f"scripts/{filename}.sh"] + list(args))
    return subprocess.check_output(["sh", f"scripts/{filename}.sh"] + list(args)).decode("utf-8")

def time_decorator(func):
    def inner(*args, **kwargs):
        st = time.time()
        ret = func(*args,  **kwargs)
        ed = time.time()
        return ret, ed - st
    return inner

# taken from: https://gist.github.com/cbwar/d2dfbc19b140bd599daccbe0fe925597
def sizeof_fmt(num, suffix='B'):
    magnitude = int(math.floor(math.log(num, 1024)))
    val = num / math.pow(1024, magnitude)
    if magnitude > 7:
        return '{:.1f}{}{}'.format(val, 'Yi', suffix)
    return '{:3.1f}{}{}'.format(val, ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi'][magnitude], suffix)
