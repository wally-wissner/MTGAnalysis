# Question: Which sets have the most colored pips by card on average?


import pandasql

from Conn import conn_mtg
from Utilities.reddit_markdown import to_reddit_markdown


query = """
SELECT 
    cards.name,
    cards.manaCost,
    cards.setCode,
    sets.name AS setName
FROM
    cards
LEFT JOIN
    sets
ON
    sets.code = cards.setCode
WHERE
    cards.borderColor IN ('black', 'white')
    AND sets.type IN ('core', 'expansion')
    AND cards.type NOT LIKE 'Land'
ORDER BY
    cards.name, sets.releaseDate
"""
df = conn_mtg.request(query)

df["coloredPips"] = df["manaCost"].apply(
    lambda x: len([i for i in x.split("}{") if any(c in i for c in "WUBRG")]) if x else 0
)

df = df.groupby("setCode")["coloredPips"].mean().reset_index()
df = df.sort_values("coloredPips")

df.to_markdown("result.md")
to_reddit_markdown(df, "result.reddit")
