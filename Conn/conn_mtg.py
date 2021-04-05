import pandas as pd
import sqlite3
import sys


def connection():
    db_path = sys.path[1] + "/Data/AllPrintings.sqlite"
    return sqlite3.connect(db_path)


def request(query):
    conn = connection()
    return pd.read_sql_query(query, conn)


def open_query(path):
    with open(path, 'r') as f:
        query = f.read()
    return query


if __name__ == "__main__":
    # q = open_query("../Queries/cards.sql")
    # df = request(q)
    # print(df.head().to_string())
    # print(df.columns)


    q = """
    SELECT
        cards.name,
        cards.colors,
        cards.convertedManaCost,
        COALESCE(LENGTH(cards.manaCost) - LENGTH(REPLACE(cards.manaCost, 'W', '')), 0) AS cost_W,
        COALESCE(LENGTH(cards.manaCost) - LENGTH(REPLACE(cards.manaCost, 'U', '')), 0) AS cost_U,
        COALESCE(LENGTH(cards.manaCost) - LENGTH(REPLACE(cards.manaCost, 'B', '')), 0) AS cost_B,
        COALESCE(LENGTH(cards.manaCost) - LENGTH(REPLACE(cards.manaCost, 'R', '')), 0) AS cost_R,
        COALESCE(LENGTH(cards.manaCost) - LENGTH(REPLACE(cards.manaCost, 'G', '')), 0) AS cost_G,
        COALESCE(LENGTH(cards.manaCost) - LENGTH(REPLACE(cards.manaCost, 'C', '')), 0) AS cost_C,
        COALESCE(LENGTH(cards.manaCost) - LENGTH(REPLACE(cards.manaCost, 'X', '')), 0) AS cost_X,
        MIN(sets.releaseDate) AS releaseDate,
        cards.rarity,
        cards.supertypes,
        cards.types,
        cards.subtypes,
        cards.power,
        cards.toughness,
        cards.loyalty,
        cards.text
    FROM
        cards
    LEFT JOIN
        sets
    ON
        sets.code = cards.setCode
    WHERE
        -- Cards only.
        cards.borderColor IN ('black', 'white')
        AND sets.type NOT IN ('funny', 'memorabilia', 'promo', 'token')
        AND (
            cards.type LIKE "%Artifact%"
            OR cards.type LIKE "%Creature%"
            OR cards.type LIKE "%Enchantment%"
            OR cards.type LIKE "%Instant%"
            OR cards.type LIKE "%Land%"
            OR cards.type LIKE "%Planeswalker%"
            OR cards.type LIKE "%Sorcery%"
            OR cards.type LIKE "%Tribal%"
        )
        -- No double sided cards.
        AND cards.side IS NULL
        -- No lands.
        AND cards.types NOT LIKE "%Land%"
        AND cards.name = "Aboroth"
    GROUP BY
        cards.name
    """
    df = request(q)
    print(df)
