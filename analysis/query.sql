-- We don't query either patient-level or event-level data, so we need not
-- exclude T1OOs using the AllowedPatientsWithTypeOneDissent table.
SELECT
    BuildDesc AS build_desc,
    CONVERT(DATE, BuildDate) AS build_date
FROM BuildInfo ORDER BY build_desc, build_date
