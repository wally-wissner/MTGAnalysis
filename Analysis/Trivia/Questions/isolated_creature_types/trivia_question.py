# Question: What creature types never appear alongside another creature type on a card?


import pandasql

from Conn import conn_mtg
from Utilities.reddit_markdown import to_reddit_markdown


query = """
SELECT
    cards.name,
    cards.subtypes
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
df["subtype_count"] = df["subtype_list"].apply(len)
df = df.explode("subtype_list", ignore_index=True)
df = df.rename({"subtype_list": "subtype"}, axis=1)

query = """
SELECT
    subtype,
    COUNT(DISTINCT name) AS card_count
FROM
    df
GROUP BY
    subtype
HAVING
    MAX(subtype_count) = 1
ORDER BY
    card_count
DESC
"""
df = pandasql.sqldf(query, locals())

df.to_markdown("result.md")
to_reddit_markdown(df, "result.reddit")
