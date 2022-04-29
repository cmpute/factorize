#!/usr/bin/env python3

from time import time
from random import randrange
from subprocess import check_call, DEVNULL
from addict import Dict
from os.path import expanduser
from os import remove
from matplotlib import pyplot as plt
from tempfile import gettempdir
import numpy as np

# path to various factorization utilities
# comment out the corresponding line if you don't want to run it
PATH = Dict({
    "factor": "/usr/bin/factor", # GNU coreutils/factor
    "factorize": "~/.cargo/bin/factorize", # Rust factorize
    "uu_factor": "~/.cargo/bin/factor", # uutils/factor
    #"gp": "gp", # Pari/GP
    #"primefac": ["python3", "-m", "primefac"], # Python primefac
})

# some other settings
BITSIZE_LIMIT = 100 # maximum bit size of the number to be tested
NTESTS = 10000 # maximum count of numbers to be factorized in a row
NREPEATS = 12 # number of repeats in each bitsize range
SHOW_AREA = True # show IQR area on the plot

def randbits(lowbits, hibits):
    n = int(NTESTS / hibits**1.5)
    return [randrange(2**lowbits, 2**hibits) for _ in range(n)]

def test_bin(path_args, nums):
    if not isinstance(path_args, list):
        path_args = [expanduser(path_args)]
    else:
        path_args[0] = expanduser(path_args[0])

    tstart = time()
    check_call(path_args + [str(n) for n in nums], stdout=DEVNULL)
    tend = time()
    return (tend - tstart) / len(nums)

def main(limit):
    stats = Dict()
    targets = list(PATH.keys())
    bits = list(range(4, (limit+1), 4))
    for b in bits:
        for e in targets:
            stats[e][b] = []

        for r in range(NREPEATS):
            num_list = randbits(b-4, b)
            print("test %d numbers in %d to %d bits (repeat %d)" % (len(num_list), b-4, b, r))

            if PATH.factor:
                stats.factor[b].append(test_bin(PATH.factor, num_list))

            if PATH.factorize:
                stats.factorize[b].append(test_bin(PATH.factorize, num_list))

            if PATH.uu_factor:
                if b > 64: # uu_factor doesn't support integers larger than 64bits
                    stats.uu_factor[b].append(float('nan'))
                else:
                    stats.uu_factor[b].append(test_bin(PATH.uu_factor, num_list))

            if PATH.primefac:
                stats.primefac[b].append(test_bin(PATH.primefac, num_list))

            if PATH.gp:
                task_path = gettempdir() + "/bench_task_%d.gp" % (b*r)
                with open(task_path, "wb") as task:
                    for n in num_list:
                        task.write(b"factor(%d);\n" % n)
                    task.write(b"\\q")

                tstart = time()
                check_call([expanduser(PATH.gp), task_path], stdout=DEVNULL, stderr=DEVNULL)
                tend = time()
                stats.gp[b].append((tend - tstart) / len(num_list))
                remove(task_path)


    time_array = {e: np.array([stats[e][b] for b in bits]) for e in targets}
    time_mean = {e: np.median(time_array[e], axis=1) for e in targets}
    time_p75 = {e: np.percentile(time_array[e], 75, axis=1) for e in targets}
    time_p25 = {e: np.percentile(time_array[e], 25, axis=1) for e in targets}

    fig, ax = plt.subplots()
    for e in targets:
        ax.plot(bits, time_mean[e], label=e)
        if SHOW_AREA:
            ax.fill_between(bits, time_p25[e], time_p75[e], alpha=0.5)
    ax.set_yscale("log")
    ax.set_ylabel("Median time per number (s)")
    ax.set_xlabel("Bit size of numbers")
    ax.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main(BITSIZE_LIMIT)
