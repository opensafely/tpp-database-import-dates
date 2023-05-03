"""Plot the import dates of the data sources.
"""
import pandas
from matplotlib import pyplot
from matplotlib.dates import num2date

from analysis import utils


def main():
    f_in = utils.OUTPUT_DIR / "query" / "rows.csv.gz"
    rows = read(f_in)
    fig = plot(rows)

    f_out = utils.OUTPUT_DIR / "plot" / "plot.png"
    utils.makedirs(f_out.parent)
    fig.savefig(f_out)


def read(f_in):
    return pandas.read_csv(f_in, parse_dates=["build_date"])


def plot(rows):
    fig, ax = pyplot.subplots(figsize=(15, 7))

    fig.suptitle("OpenSAFELY-TPP Import Dates", fontsize="x-large")

    for name, group in rows.groupby("build_desc"):
        ax.scatter(group["build_date"], group["build_desc"], marker=".")

    ax.invert_yaxis()  # As at the top, Zs at the bottom
    ax.grid(True, axis="x")
    ax.margins(x=0)
    min_ts, max_ts = [num2date(x) for x in ax.get_xlim()]
    ax.set_title(f"From {min_ts:%Y-%m-%d} to {max_ts:%Y-%m-%d}", fontsize="medium")

    return fig


if __name__ == "__main__":
    main()
