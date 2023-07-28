import nltk
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)


def _count_token(tokens: list[str]) -> dict[str, int]:
    token_count: dict[str, int] = {}

    for token in tokens:
        token_count[token] = 0

    for token in tokens:
        token_count[token] = token_count[token] + 1

    return token_count


def _find_word(word: str, tokens: list[str]) -> list[int]:
    found_index = []
    for i in range(len(tokens)):
        if tokens[i] == word:
            found_index.append(i)
    return found_index


def get_following_pos_tags(word: str, length: int, text: str) -> list[list[str]]:
    tokens: list[str] = nltk.word_tokenize(text)
    tagged_tokens: list[tuple[str, str]] = nltk.pos_tag(tokens)

    following_pos_tags = []

    for i in _find_word(word, tokens):
        following_pos_tag = []
        for k in range(length):
            _, tag = tagged_tokens[i + k + 1]
            following_pos_tag.append(tag)
        following_pos_tags.append(following_pos_tag)

    return following_pos_tags


if __name__ == '__main__':
    text: str = "I am hoge. I got it."

    result = get_following_pos_tags("I", 2, text)

    print(result)
