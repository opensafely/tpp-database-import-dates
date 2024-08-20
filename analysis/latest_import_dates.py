"""Get the latest import dates of the data sources."""

import pandas

from analysis import utils


def main():
    f_in = utils.OUTPUT_DIR / "query" / "rows.csv.gz"
    latest_import_dates = get_latest_import_dates(f_in)

    f_out = utils.OUTPUT_DIR / "latest_import_dates" / "latest_import_dates.csv"
    utils.makedirs(f_out.parent)
    latest_import_dates.to_csv(f_out)


def get_latest_import_dates(f_in):
    build_desc = "build_desc"
    build_date = "build_date"
    return (
        pandas.read_csv(f_in, index_col=build_desc, parse_dates=[build_date])
        .loc[:, build_date]  # to series
        .groupby(build_desc)
        .max()
    )


if __name__ == "__main__":
    main()
