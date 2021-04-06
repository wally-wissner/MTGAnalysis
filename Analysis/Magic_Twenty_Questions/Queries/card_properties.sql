SELECT
    cards.name,
    cards.convertedManaCost,
    cards.manaCost,
    cards.colors,
    cards.supertypes,
    cards.types,
    cards.subtypes,
    cards.power,
    cards.toughness,
    cards.loyalty,
    cards.text,
    sets.name AS setName
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