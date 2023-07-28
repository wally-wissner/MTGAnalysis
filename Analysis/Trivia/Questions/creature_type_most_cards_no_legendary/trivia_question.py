# Question: Which creature types that have never had a legendary creature have the most creature cards?


import pandasql

from Conn import conn_mtg
from Utilities.reddit_markdown import to_reddit_markdown


query_cards = """
SELECT
    cards.name,
    cards.supertypes LIKE '%legendary%' AS legendary,
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

df_cards = conn_mtg.request(query_cards)
df_cards["subtypes"] = df_cards["subtypes"].apply(lambda x: [i.strip() for i in x.split(",")] if x else [])
df_cards = df_cards.explode("subtypes", ignore_index=True)
df_cards = df_cards.rename({"subtypes": "subtype"}, axis=1)

query_count = """
SELECT
    subtype,
    COUNT(*) AS count
FROM
    df_cards
GROUP BY
    subtype
HAVING
    SUM(legendary) = 0
ORDER BY
    COUNT(*)
DESC
"""
df_count = pandasql.sqldf(query=query_count, env=locals())

df_count.to_markdown("result.md")
to_reddit_markdown(df_count, "result.reddit")
