SELECT
    BuildDesc AS build_desc,
    CONVERT(DATE, BuildDate) AS build_date
FROM BuildInfo ORDER BY build_desc, build_date
