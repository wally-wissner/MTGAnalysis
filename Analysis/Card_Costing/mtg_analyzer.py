from nltk.corpus import stopwords as english_stopwords
from nltk.stem.snowball import SnowballStemmer


mtg_stopwords = set(english_stopwords.words("english")) - {"any", "both", "each", "you", "your"}
_english_stemmer = SnowballStemmer(language='english')


def _analyze_string(doc, ngram_range):
    words = [
        _english_stemmer.stem(w) if all(ch.isalpha() or ch == "'" for ch in w) else w
        for w in doc.split()
        if w not in mtg_stopwords and _english_stemmer.stem(w) not in mtg_stopwords
    ]
    grams = []
    for n in (ngram_range[0], ngram_range[1] + 1):
        for word_index in range(len(words) - n):
            grams.append(" ".join(words[word_index: word_index + n - 1]))
    return grams


def make_mtg_analyzer(ngram_range):
    def mtg_analyzer(doc):
        return _analyze_string(doc, ngram_range)
    return mtg_analyzer
