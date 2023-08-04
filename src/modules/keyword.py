import nltk
nltk.download('punkt', quiet=True)
from .token_freq import token_frequency_ratio


def _make_token_to_frequency_ratio(texts: list[str]) -> dict[str, float]:
    all_text: str = " ".join(texts)
    return token_frequency_ratio(all_text)


def _is_keyword(all_ratio: float, author_ratio: float) -> bool:
    """Return True if the given author's token frequency ratio is 10% or more different from the average of all authors."""
    diff: float = abs(all_ratio - author_ratio)
    return diff >= 0.05


def extract_keywords(author_to_texts: dict[str, list[str]], author: str) -> list[str]:
    """Extract keywords from the given author's texts."""

    # すべてのテキストのトークンの出現率
    all_texts: list[str] = [text for texts in list(author_to_texts.values()) for text in texts]
    all_token_to_ratio: dict[str, float] = _make_token_to_frequency_ratio(all_texts)

    texts: list[str] = author_to_texts[author]

    # この著者のテキストのトークンの出現率
    author_token_to_ratio: dict[str, float] = _make_token_to_frequency_ratio(texts)

    keywords: list[str] = []

    # keywordを抽出
    for token in author_token_to_ratio.keys():
        if _is_keyword(all_token_to_ratio[token], author_token_to_ratio[token]):
            keywords.append(token)

    return keywords


if __name__ == '__main__':
    author_to_texts: dict[str, list[str]] = {
        "hoge": [
            "I am hoge.",
            "Nice to meet you.",
            "keyword  keyword",
        ],
        "fuga": [
            "I am fuga.",
            "Nice to meet you.",
            "keyword keyword keyword keyword keyword keyword",
        ],
    }

    keywords = extract_keywords(author_to_texts, "hoge")

    print("keywords:", keywords)
