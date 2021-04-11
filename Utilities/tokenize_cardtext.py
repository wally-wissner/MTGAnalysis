import re


def tokenize(text, cardname, reminder_text=False, atomic_mana_symbols=False, atomic_power_toughness=False, include_end_token=False):
    cardname_token = "~"
    newline_token = "&"
    end_token = "$"

    if not text:
        return ""

    # Create a token for card self-referencing.
    text = text.replace(cardname, cardname_token)
    # Handle legend epithets.
    for epithet_delimiter in [
        ",",
        " of the ",
        " the ",
    ]:
        legendname = cardname.split(epithet_delimiter)[0]
        text = text.replace(legendname, cardname_token)

    text = text.lower()

    if not reminder_text:
        # Remove reminder text.
        text = re.sub(r"\([^)]*\)", "", text)

    # Create newline character.
    text = text.replace("\n", newline_token)

    # Separate mana symbols.
    text = text.replace("}{", "} {")
    text = text.replace("][", "] [")

    semantic_chars = r".:()+-/{}[]" + cardname_token + newline_token + end_token
    padding_chars = r".:()" \
        + newline_token \
        + ("" if atomic_power_toughness else r"+-/") \
        + ("" if atomic_mana_symbols else "{}[]")

    for ch in padding_chars:
        text = text.replace(ch, f" {ch} ")

    if include_end_token:
        text = text + f" {end_token}"

    # Remove non-semantic characters.
    text = "".join(ch for ch in text if ch.isalnum() or ch in " '" + semantic_chars)

    # Remove duplicated whitespace.
    text = re.sub(r'\s+', ' ', text)

    text = text.strip()

    return text
