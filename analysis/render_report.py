"""Render the report as an HTML file using the Jinja templating engine.

For more information about Jinja, see:
<https://jinja.palletsprojects.com/en/2.11.x/>
"""

import base64
import csv
import datetime
import mimetypes

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from analysis import ANALYSIS_DIR, utils

ENVIRONMENT = Environment(
    loader=FileSystemLoader(ANALYSIS_DIR),
    undefined=StrictUndefined,
)


def main():
    f_out = utils.OUTPUT_DIR / "render_report" / "report.html"
    utils.makedirs(f_out.parent)
    rendered_report = render_report(
        {
            "run_date": utils.get_run_date(),
            "latest_import_dates": get_latest_import_dates(
                utils.OUTPUT_DIR / "latest_import_dates" / "latest_import_dates.csv"
            ),
            "plot": utils.OUTPUT_DIR / "plot" / "plot.png",
        }
    )
    f_out.write_text(rendered_report, encoding="utf-8")


def b64encode(path):
    """Encodes the file at the given path using Base64.

    Returns a string for use as the src attribute of an img tag. If we use this string,
    then we embed the file within the HTML file. This means we don't have to include the
    file in the list of outputs in project.yaml.
    """
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    mtype, _ = mimetypes.guess_type(path)
    return f"data:{mtype};base64, {encoded}"


def date_format(date):
    """Formats the given date as, for example, "1 January 2023"."""
    return f"{date:%-d %B %Y}"  # the - removes the leading zero, but not on Windows


# register template filters
ENVIRONMENT.filters["b64encode"] = b64encode
ENVIRONMENT.filters["date_format"] = date_format


def render_report(data):
    template = ENVIRONMENT.get_template("report_template.html")
    return template.render(data)


def get_latest_import_dates(f_in):
    with f_in.open(newline="") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            yield {
                "build_desc": row[0],
                "build_date": datetime.date.fromisoformat(row[1]),
            }


if __name__ == "__main__":
    main()
