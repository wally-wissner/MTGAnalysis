import numpy as np
import pandas as pd
import re
import sys

from Conn import conn_mtg


def to_int(text):
    try:
        return int(text)
    except (TypeError, ValueError):
        return -1


def tokenize(text, cardname, atomic_mana_symbols=False, atomic_power_toughness=False):
    if not text:
        return ""

    # Create a token for card self-reference: cardname.
    legendname = cardname.split(",")[0]
    text = text.replace(cardname, "cardname")
    text = text.replace(legendname, "cardname")

    text = text.lower()

    # Create newline character.
    text = text.replace("\n", "&")

    # Separate mana symbols.
    text = text.replace("}{", "} {")
    text = text.replace("][", "] [")

    # Remove non-semantic characters.
    for ch in "•−—,;":
        text = text.replace(ch, " ")

    semantic_chars = ".:&()+-/{}[]"
    padding_chars = ".:&()" + ("" if atomic_power_toughness else "+-/") + ("" if atomic_mana_symbols else "{}[]")

    for ch in padding_chars:
        text = text.replace(ch, f" {ch} ")

    text = "".join(ch for ch in text if ch.isalnum() or ch in " '" + semantic_chars)
    text = re.sub('\s+', ' ', text)

    return text


def get_df():
    df = conn_mtg.request(conn_mtg.open_query(sys.path[1] + "/Analysis/Card_Costing/Queries/card_properties.sql"))

    df["releaseDate"] = pd.to_datetime(df["releaseDate"])
    df["years"] = (df["releaseDate"] - df["releaseDate"].min()) / np.timedelta64(1, 'Y')
    df = df.drop("releaseDate", axis=1)

    df["n_colors"] = (df[["cost_W", "cost_U", "cost_B", "cost_R", "cost_G"]] > 0).sum(axis=1)
    df["n_colored_symbols"] = df[["cost_W", "cost_U", "cost_B", "cost_R", "cost_G"]].sum(axis=1)

    for col in ["power", "toughness", "loyalty"]:
        df[col] = df[col].apply(to_int)

    # Can only process subtypes after types are processed.
    for col in ["supertypes", "types", "subtypes"]:
        df[col] = df[col].apply(lambda row: row.split(",") if row else [])

        # Don't include creature or planeswalker subtypes.
        if col == "subtypes":
            _df = df[df[["types_Creature", "types_Planeswalker", "types_Tribal"]].sum(axis=1) == 0]
        else:
            _df = df
        values = sorted(list({i for entry in _df[col] for i in entry}))

        for value in values:
            df[f"{col}_{value}"] = df[col].apply(lambda x: any(i in value for i in x)).astype(int)
        df = df.drop(col, axis=1)

    # df["rarity_mythic"] = (df["rarity"] == "mythic")
    # df["rarity_rare"] = (df["rarity"] == "rare") | df["rarity_mythic"]
    # df["rarity_uncommon"] = (df["rarity"] == "uncommon") | df["rarity_rare"]
    # df["rarity_common"] = (df["rarity"] == "common") | df["rarity_uncommon"]
    # for col in df.columns:
    #     if "rarity_" in col:
    #         df[col] = df[col].astype(int)
    df = df.drop("rarity", axis=1)

    df["text"] = df.apply(
        lambda row: tokenize(row["text"], row["name"], atomic_mana_symbols=True, atomic_power_toughness=True), axis=1
    )

    df["n_words"] = df["text"].apply(lambda x: len(x.split()))
    df["n_abilities"] = df["text"].apply(lambda x: len(x.split("&")))

    return df


if __name__ == "__main__":
    df = get_df()
    print(df.head(10).to_string())
    print(df.describe().to_string())
    print(df[["name", "text"]].head(50).to_string())
    # print({ch for row in df["text"].fillna("") for ch in row if not ch.isalnum()})
