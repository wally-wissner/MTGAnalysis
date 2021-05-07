# Question: Which card names are the most similar (by Levenshtein distance)?


import Levenshtein
import pandas as pd
from tqdm import tqdm

from Conn import conn_mtg
from Utilities.reddit_markdown import to_reddit_markdown


query = """
SELECT DISTINCT
    cards.name
FROM
    cards
"""
df = conn_mtg.request(query)

matches = []
for card_a in tqdm(df["name"]):
    for card_b in df["name"]:
        if card_a < card_b and Levenshtein.distance(card_a, card_b) == 1:
            matches.append([card_a, card_b])

df = pd.DataFrame(matches, columns=["card_a", "card_b"])

df.to_markdown("result.md")
to_reddit_markdown(df, "result.reddit")
