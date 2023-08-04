from modules import keyword, keyword_pos, token_freq
import matplotlib.pyplot as plt


def _read_file(path: str) -> str:
    with open(path) as f:
        return f.read()


def _read_dataset() -> dict[str, list[str]]:
    author_to_lines: dict[str, list[str]] = {}

    author_to_lines["K1-dataset.txt"] = [
        _read_file("../dataset/K1-dataset.txt")
    ]

    author_to_lines["K2-dataset.txt"] = [
        _read_file("../dataset/K2-dataset.txt")
    ]

    author_to_lines["Q-dataset.txt"] = [
        _read_file("../dataset/Q-dataset.txt")
    ]

    return author_to_lines


def _count_same_elements(a: list, b: list) -> int:
    count = 0
    for v in a:
        if v in b:
            count += 1

    return count


def max_n_elements(d: dict, n: int) -> dict:
    key_values = list(d.items())
    key_values.sort(reverse=True, key=lambda x: x[1])

    result: dict = {}

    for i in range(n):
        key, value = key_values[i]
        result[key] = value

    return result


def plot_result(estimated_author_token_to_freq_ratio: dict[str, float], questioned_token_to_freq_ratio: dict[str, float]):
    # 推定した著者のトークンの出現頻度とQuestionedテキストのトークンの出現頻度を出力
    plt.xlabel("token")
    plt.ylabel("frequency ratio")
    plt.ylim(0, 1)
    plt.title(
        "token frequency ratio of estimated author texts(red) and Questioned text(blue)"
    )

    max10_estimated = max_n_elements(estimated_author_token_to_freq_ratio, 10)

    plt.bar(
        list(max10_estimated.keys()),
        list(max10_estimated.values()),
        width=0.3,
        align='center',
        color='red'
    )

    max10_questioned_token = max_n_elements(questioned_token_to_freq_ratio, 10)

    plt.bar(
        list(max10_questioned_token.keys()),
        list(max10_questioned_token.values()),
        width=0.3,
        align='edge',
        color='blue'
    )

    plt.show()


def main():
    author_to_texts: dict[str, list[str]] = _read_dataset()

    # 各著者のkeywordを検出
    author_to_keywords: dict[str, list[str]] = {}
    author_to_keywords["K1-dataset.txt"] = keyword.extract_keywords(
        author_to_texts,
        "K1-dataset.txt"
    )
    author_to_keywords["K2-dataset.txt"] = keyword.extract_keywords(
        author_to_texts,
        "K2-dataset.txt"
    )
    author_to_keywords["Q-dataset.txt"] = keyword.extract_keywords(
        author_to_texts,
        "Q-dataset.txt"
    )

    # その著者の全てのテキストからkeywordに続くパターンを検出
    author_to_pos_tags: dict[str, list[list[str]]] = {}
    for author, keywords in author_to_keywords.items():
        author_all_texts: list[str] = [
            text for text in author_to_texts[author]
        ]
        author_all_text: str = "\n".join(author_all_texts)

        # keywordsが空
        if not keywords:
            author_to_pos_tags[author] = []
            continue

        # keywordに続くパターンを検出し、その著者のパターンとして追加していく
        for key in keywords:
            pos_tags: list[list[str]] = keyword_pos.get_following_pos_tags(
                key,
                2,
                author_all_text
            )

            if author not in author_to_pos_tags:
                author_to_pos_tags[author] = pos_tags
            elif not pos_tags:
                author_to_pos_tags[author].append(*pos_tags)

    # 全てのテキストからトークンと出現頻度を検出
    # TODO: Questioned含んで処理してるけど、含まないほうが良い？
    all_texts: list[str] = [text for texts in list(
        author_to_texts.values()) for text in texts]
    all_text: str = "\n".join(all_texts)
    all_token_to_freq_ratio: dict[str, float] = token_freq.token_frequency_ratio(
        all_text
    )

    # Questionedなテキストのkeywordを検出
    questioned_keywords: list[str] = author_to_keywords["Q-dataset.txt"]

    # Questionedなテキストのpos_tagを検出
    questioned_pos_tags: list[list[str]] = author_to_pos_tags["Q-dataset.txt"]

    # Questionedなテキストの各トークンの出現頻度
    questioned_all_texts: list[str] = [
        text for text in author_to_texts["Q-dataset.txt"]
    ]
    questioned_all_text: str = "\n".join(questioned_all_texts)
    questioned_token_to_freq_ratio: dict[str, float] = token_freq.token_frequency_ratio(
        questioned_all_text
    )

    # Questionedなテキストのキーワードと全ての著者のキーワードの類似度を見る
    author_to_same_keywords_count: dict[str, int] = {}
    for author, keywords in author_to_keywords.items():
        same_count: int = _count_same_elements(questioned_keywords, keywords)
        author_to_same_keywords_count[author] = same_count

    # Questionedなテキストのpos_tagと全ての著者のpos_tagの類似度を見る
    author_to_same_pos_tags_count: dict[str, int] = {}
    for author, pos_tags in author_to_pos_tags.items():
        same_count: int = _count_same_elements(questioned_pos_tags, pos_tags)
        author_to_same_pos_tags_count[author] = same_count

    # Questionedなテキストの各トークンの出現頻度と、全てのテキストの各トークンの出現頻度の差を見る
    author_to_token_to_freq_ratio: dict[str, dict[str, float]] = {}
    for author, texts in author_to_texts.items():
        text = "\n".join(texts)
        author_to_token_to_freq_ratio[author] = token_freq.token_frequency_ratio(
            text
        )

    authors = ["K1-dataset.txt", "K2-dataset.txt"]

    author_to_diff_sum: dict[str, float] = {}
    for author in authors:
        diff_sum = 0
        for token, ratio in questioned_token_to_freq_ratio.items():
            if token not in author_to_token_to_freq_ratio[author]:
                diff_sum += ratio
            else:
                diff_sum += ratio - \
                    author_to_token_to_freq_ratio[author][token]

        author_to_diff_sum[author] = diff_sum

    # 類似度が最も高い著者を出力
    count_sums: list[tuple[tuple[int, int, float], str]] = []
    for author in authors:
        # 20 は評価用の係数。用調整
        diff = 0 if author_to_diff_sum[author] == 0 else 20 / \
            author_to_diff_sum[author]
        count_sum: tuple[int, int, float] = (
            author_to_same_keywords_count[author],
            author_to_same_pos_tags_count[author],
            diff
        )

        count_sums.append((count_sum, author))

    count_sums.sort(reverse=True, key=lambda x: x[0])

    estimated_author: str = count_sums[0][1]

    print("Questioned author:", estimated_author)

    estimated_author_token_to_freq_ratio: dict[str, float] = token_freq.token_frequency_ratio(
        author_to_texts[estimated_author][0]
    )

    plot_result(estimated_author_token_to_freq_ratio,
                questioned_token_to_freq_ratio)


if __name__ == '__main__':
    main()
