# Question: What cards have their name equal to their creature types?


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

df["subtypes"] = df["subtypes"].apply(lambda x: x.split(",") if x else [])
df["subtypes"] = df["subtypes"].apply(lambda x: " ".join(x))
df = df[
    df["name"].apply(lambda x: sorted(list(x.split()))) ==
    df["subtypes"].apply(lambda x: sorted(list(x.split())))
]
df["same_order"] = (df["name"] == df["subtypes"])

df = df[["name", "subtypes", "same_order"]]

print(df.shape)
print(df[~df["same_order"]].shape)

df.to_markdown("result.md")
to_reddit_markdown(df, "result.reddit")
