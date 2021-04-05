# Question: What card names are anagrams of other card names?


from collections import Counter
from tqdm import tqdm

from Conn import conn_mtg


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

for i in matches:
    print(i)

print(len(matches))
