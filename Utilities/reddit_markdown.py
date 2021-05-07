import pandas as pd


def reddit_table_markdown(df: pd.DataFrame, index=True) -> str:
    markdown_rows = list()
    markdown_rows.append(f"| {' | '.join(str(col) for col in df.columns)} |\n")
    markdown_rows.append(f"{'--'.join('|' for _ in range(df.shape[1]+1))}\n")
    for _, row in df.iterrows():
        markdown_rows.append(f"| {' | '.join(str(val) for val in row)} |\n")

    if index:
        for i, row in enumerate(markdown_rows):
            if i == 0:
                markdown_rows[i] = "| " + row
            if i == 1:
                markdown_rows[i] = "|--" + row
            if i >= 2:
                markdown_rows[i] = f"| {i-2} " + row

    markdown = "".join(markdown_rows)
    return markdown


def to_reddit_markdown(df: pd.DataFrame, filename: str, *args, **kwargs) -> None:
    with open(filename, "w+") as f:
        f.write(reddit_table_markdown(df, *args, **kwargs))
