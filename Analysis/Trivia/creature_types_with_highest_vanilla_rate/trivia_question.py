# Question: Which creature types have the highest rate of being vanilla creatures?


import pandasql

from Conn import conn_mtg
from Utilities.reddit_markdown import reddit_table_markdown


query = """
SELECT
    cards.name,
    cards.subtypes,
    (LENGTH(text) IS NULL) AS vanilla
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

df_cards = conn_mtg.request(query)
df_cards["subtypes"] = df_cards["subtypes"].apply(lambda x: x.split(",") if x else [])
df_cards = df_cards.explode("subtypes", ignore_index=True)
df_cards = df_cards.rename({"subtypes": "subtype"}, axis=1)

query_vanilla = """
SELECT
    subtype,
    COUNT(*) AS count,
    AVG(vanilla) AS frac_vanilla
FROM
    df_cards
GROUP BY
    subtype
HAVING
    AVG(vanilla) > 0
ORDER BY
    AVG(vanilla)
DESC
"""
df_vanilla = pandasql.sqldf(query=query_vanilla, env=locals())
df_vanilla["frac_vanilla"] = df_vanilla["frac_vanilla"].round(4)

print(reddit_table_markdown(df_vanilla))
