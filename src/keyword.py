import nltk
nltk.download('punkt', quiet=True)


def _make_token_to_frequency_ratio(texts: list[str]) -> dict[str, float]:
    token_to_frequency_ratio: dict[str, float] = {}

    # すべてのテキストのトークンの出現頻度を数える
    for text in texts:
        tokens = nltk.word_tokenize(text)

        for token in tokens:
            if token not in token_to_frequency_ratio:
                token_to_frequency_ratio[token] = 0

            token_to_frequency_ratio[token] += 1

    # すべてのテキストのトークンの出現頻度をトークンの数で割る
    token_count = len(token_to_frequency_ratio.keys())

    for token in token_to_frequency_ratio.keys():
        token_to_frequency_ratio[token] = token_to_frequency_ratio[token] / token_count

    return token_to_frequency_ratio


def _is_keyword(all_ratio: float, author_ratio: float) -> bool:
    """Return True if the given author's token frequency ratio is 10% or more different from the average of all authors."""
    diff: float = abs(all_ratio - author_ratio)
    return diff >= 0.1


def extract_keywords(author_to_texts: dict[str, list[str]], author: str) -> list[str]:
    """Extract keywords from the given author's texts."""

    # すべてのテキストのトークンの出現率
    all_token_to_ratio: dict[str, float] = _make_token_to_frequency_ratio(author_to_texts.values())

    texts: list[str] = author_to_texts[author]

    # この著者のテキストのトークンの出現率
    author_token_to_ratio: dict[str, float] = _make_token_to_frequency_ratio(texts)

    keywords: list[str] = []

    # keywordを抽出
    for token in author_token_to_ratio.keys():
        if _is_keyword(all_token_to_ratio[token], author_token_to_ratio[token]):
            keywords.append(token)

    return keywords
