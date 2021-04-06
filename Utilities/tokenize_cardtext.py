import re


def tokenize(text, cardname, reminder_text=False, atomic_mana_symbols=False, atomic_power_toughness=False):
    if not text:
        return ""

    # Create a token for card self-reference: cardname.
    legendname = cardname.split(",")[0]
    text = text.replace(cardname, "cardname")
    text = text.replace(legendname, "cardname")

    text = text.lower()

    if not reminder_text:
        # Remove reminder text.
        text = re.sub("\([^)]*\)", "", text)

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