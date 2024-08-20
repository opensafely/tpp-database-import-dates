"""Generate dummy rows to match the query in analysis/query.sql.

opensafely exec python:latest python -m analysis.generate_dummy_rows

"""

import pandas

from analysis import utils


def main():
    f_out = utils.OUTPUT_DIR / "generate_dummy_rows" / "dummy_rows.csv.gz"
    table_names = [
        "APCS",
        "CPNS",
        "EC",
        "ECDS",
        "HealthCareWorker",
        "HighCostDrugs",
        "ICNARC",
        "MPI",
        "ONS_CIS",
        "ONS_Deaths",
        "OPA",
        "S1",
        "SGSS_AllTests_Negative",
        "SGSS_AllTests_Positive",
        "SGSS_Negative",
        "SGSS_Positive",
        "Therapeutics",
        "UKRR",
        "UPRN",
    ]
    from_date = "2020-01-01"
    to_date = "2023-01-01"

    utils.makedirs(f_out.parent)
    data_frame = make_dummy_rows(table_names, from_date, to_date)
    data_frame.to_csv(f_out, index=False)


def make_dummy_rows(table_names, from_date, to_date):
    date_range = pandas.date_range(from_date, to_date, freq="W-MON").to_series()
    return (
        # column names and sort order should match the query in analysis/query.sql
        pandas.concat(
            pandas.DataFrame(
                {
                    "build_desc": table_name,
                    "build_date": date_range.sample(frac=0.4, random_state=i),
                }
            )
            for i, table_name in enumerate(table_names)
        )
        .reset_index(drop=True)
        .sort_values(["build_desc", "build_date"])
    )


if __name__ == "__main__":
    main()
