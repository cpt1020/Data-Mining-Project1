import argparse

def parse_args():
    p = argparse.ArgumentParser()

    def a(*args, **kwargs):
        p.add_argument(*args, **kwargs)

    a('--min_sup', type=float, default=0.02, help='Minimum support')
    a('--min_conf', type=float, default=0.05, help='Minimum confidence')
    a('--dataset', type=str, default='ibm-2022.txt', help='Dataset to use, please include the extension')

    return p.parse_args()