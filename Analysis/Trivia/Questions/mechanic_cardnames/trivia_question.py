# Question: What cards have the same name as a mechanic?


import pandasql

from Conn import conn_mtg
from Utilities.reddit_markdown import to_reddit_markdown


query = """
SELECT
    DISTINCT cards_a.name
FROM
    cards AS cards_a
JOIN
    cards AS cards_b
WHERE
    cards_a.name != cards_b.name
    AND cards_a.supertypes NOT LIKE '%Basic%'
    AND LOWER(cards_b.text) NOT LIKE '%named%'
    AND INSTR(LOWER(cards_b.text), LOWER(cards_a.name))
"""
df = conn_mtg.request(query)

print(df.to_string())
