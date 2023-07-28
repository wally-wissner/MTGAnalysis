# Question: How many turns, on average, do planeswalkers take to ultimate?


import numpy as np
import re

from Conn import conn_mtg
from Utilities.reddit_markdown import to_reddit_markdown


query = """
SELECT
    cards.name,
    cards.subtypes,
    cards.loyalty,
    cards.text
FROM
    cards
LEFT JOIN
    sets
ON
    sets.code = cards.setCode
WHERE
    cards.borderColor IN ('black', 'white')
    AND sets.type NOT IN ('funny', 'memorabilia', 'promo', 'token')
    AND cards.types = "Planeswalker"
    AND manaCost IS NOT NULL
GROUP BY
    cards.name
"""
df = conn_mtg.request(query)


def to_int(text):
    try:
        return int(text)
    except ValueError:
        return None


def ability_cost(text):
    costs = re.findall("\[[+−]*[X0-9]+\]", text)
    costs = [cost.strip("[]").replace("−", "-") for cost in costs]
    costs = [to_int(cost) for cost in costs]
    return costs


df["loyalty"] = df["loyalty"].apply(to_int)

df["ability_costs"] = df["text"].apply(ability_cost)
df["has_ultimate"] = df.apply(lambda row: -row["ability_costs"][-1] > row["loyalty"] if row["ability_costs"][-1] else None, axis=1)
df["ultimate_cost"] = df.apply(lambda row: row["ability_costs"][-1] if row["has_ultimate"] else None, axis=1)
df["max_uptick"] = df["ability_costs"].apply(lambda x: max(i for i in x if i) if len([i for i in x if i]) > 0 else None)
df["turns_to_ultimate"] = np.ceil((df["ultimate_cost"].abs() - df["loyalty"]) / df["max_uptick"]) + 1

print("mean turns to ultimate:", df["turns_to_ultimate"].mean())
print("median_turns_to_ultimate:", df["turns_to_ultimate"].median())

df_planeswalker = df.groupby("subtypes")[["subtypes", "turns_to_ultimate"]].mean().sort_values("turns_to_ultimate")

df_planeswalker.to_markdown("result.md")
to_reddit_markdown(df_planeswalker, "result.reddit")
