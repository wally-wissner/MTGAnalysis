# Question: What card names are anagrams of other card names?


import pandas as pd
from collections import Counter
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

card_counter = [(card, Counter(ch for ch in card.lower())) for card in df["name"]]

matches = []
for card_a, counter_a in tqdm(card_counter):
    for card_b, counter_b in card_counter:
        if card_a < card_b and counter_a == counter_b:
            matches.append([card_a, card_b])

df = pd.DataFrame(matches, columns=["card_a", "card_b"])

df.to_markdown("result.md")
to_reddit_markdown(df, "result.reddit")
