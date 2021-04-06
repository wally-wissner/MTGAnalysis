"""
Preprocessing to create a dataframe of columns the bot can use to generate its questions.
"""


from Conn import conn_mtg
from Utilities.tokenize_cardtext import tokenize


def get_df():
    df = conn_mtg.request(conn_mtg.open_query("Queries/card_properties.sql"))

    df = df.astype({
        "convertedManaCost": int,
    })

    # Can only process subtypes after types are processed.
    for col in ["supertypes", "types", "subtypes"]:
        df[col] = df[col].apply(lambda row: row.split(",") if row else [])
        values = sorted(list({i for entry in df[col] for i in entry}))
        for value in values:
            df[f"{col}_{value}"] = df[col].apply(lambda x: any(i in value for i in x)).astype(int)
        df = df.drop(col, axis=1)


    df["hashed_name"] = df["name"].apply(hash)

    df["text"] = df.apply(
        lambda row: tokenize(row["text"], row["name"], atomic_mana_symbols=True, atomic_power_toughness=True), axis=1
    )

    return df


if __name__ == "__main__":
    df = get_df()
    print(df.head(5).to_string())
