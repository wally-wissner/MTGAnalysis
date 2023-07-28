# Question: What creature type had the longest gap between printings of new cards with that creature type?


import pandasql

from Conn import conn_mtg
from Utilities.reddit_markdown import to_reddit_markdown


query = """
SELECT
    cards.name,
    cards.subtypes,
    MIN(sets.releaseDate) AS releaseDate
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
GROUP BY
    cards.name
"""
df = conn_mtg.request(query)

df["subtype_list"] = df["subtypes"].apply(lambda x: x.split(",") if x else [])
df = df.explode("subtype_list", ignore_index=True)
df = df.rename({"subtype_list": "subtype"}, axis=1)
df = df[["subtype", "releaseDate"]]

df = df.drop_duplicates()
df = df.sort_values(["subtype", "releaseDate"]).reset_index(drop=True)
df["i"] = df.index

query = """
WITH gaps AS (
SELECT
    a.subtype,
    (JULIANDAY(b.releaseDate) - JULIANDAY(a.releaseDate)) / 365 AS release_gap_years
FROM
    df AS a
JOIN
    df as b
ON
    a.subtype = b.subtype
WHERE
    b.i = a.i + 1
)
SELECT
    subtype,
    ROUND(MAX(release_gap_years),2) AS new_release_gap_years
FROM
    gaps
GROUP BY
    subtype
ORDER BY
    MAX(release_gap_years)
DESC
"""
df = pandasql.sqldf(query, locals())

df.to_markdown("result.md")
to_reddit_markdown(df, "result.reddit")
