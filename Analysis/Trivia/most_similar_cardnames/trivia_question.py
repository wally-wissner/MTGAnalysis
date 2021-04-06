# Question: Which card names are the most similar (by Levenshtein distance)?


import Levenshtein
from tqdm import tqdm

from Conn import conn_mtg


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

for i in matches:
    print(i)

print(len(matches))
