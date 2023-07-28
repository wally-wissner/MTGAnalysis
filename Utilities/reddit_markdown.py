import pandas as pd


def reddit_table_markdown(df: pd.DataFrame, index=True) -> str:
    markdown = df.to_markdown(index=index)
    lines = markdown.split("\n")

    # Remove colons from markdown.
    lines[1] = lines[1].replace(":", "-")
    markdown = "\n".join(lines)

    return markdown


def to_reddit_markdown(df: pd.DataFrame, filename: str, *args, **kwargs) -> None:
    with open(filename, "w+") as f:
        f.write(reddit_table_markdown(df, *args, **kwargs))
