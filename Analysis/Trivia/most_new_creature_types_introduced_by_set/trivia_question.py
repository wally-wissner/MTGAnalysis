# Question: Which sets introduced the most new creature types (according to modern errata)?


import pandasql

from Conn import conn_mtg
from Utilities.reddit_markdown import reddit_table_markdown


query = """
SELECT 
    cards.name,
    cards.setCode,
    cards.subtypes,
    sets.name AS setName,
    sets.releaseDate
FROM
    cards
LEFT JOIN
    sets
ON
    sets.code = cards.setCode
WHERE
    cards.borderColor IN ('black', 'white')
    AND cards.type LIKE '%creature%'
    AND sets.type NOT IN ('funny', 'promo', 'token')
ORDER BY
    cards.name, sets.releaseDate
"""
df = conn_mtg.request(query)

df["subtypes"] = df["subtypes"].apply(lambda x: x.split(",") if x else [])
df = df.explode("subtypes", ignore_index=True)
df = df.rename({"subtypes": "subtype"}, axis=1)

query = """
WITH first_subtype_print AS (
SELECT
    subtype,
    setName,
    setCode,
    releaseDate,
    MIN(releaseDate || '--' || setCode) AS dateSet
FROM
    df
WHERE
    subtype IS NOT NULL
GROUP BY
    subtype
)
SELECT
    setName AS set_name,
    setCode AS set_code,
    releaseDate AS release_date,
    COUNT(DISTINCT subtype) AS subtype_origination_count,
    GROUP_CONCAT(subtype) AS subtypes_originated
FROM
    first_subtype_print
GROUP BY
    dateSet
ORDER BY
    subtype_origination_count
DESC
"""
df = pandasql.sqldf(query, locals())

df.to_markdown("result.md")
