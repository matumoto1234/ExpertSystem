import nltk
nltk.download('punkt', quiet=True)


def _count_token(tokens: list[str]) -> dict[str, int]:
    token_count: dict[str, int] = {}

    for token in tokens:
        token_count[token] = 0

    for token in tokens:
        token_count[token] = token_count[token] + 1

    return token_count


def token_frequency_ratio(text: str) -> dict[str, float]:
    token_count: dict[str, int] = _count_token(nltk.word_tokenize(text))

    token_frequency = {}
    for token, count in token_count.items():
        token_frequency[token] = count / len(token_count)

    return token_frequency
