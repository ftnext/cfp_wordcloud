import argparse
from pathlib import Path
import re

from janome.tokenizer import Tokenizer
from wordcloud import WordCloud


BG_COLOR = 'white'
FONT_FILE = 'SourceHanCodeJP-Regular.otf'
RANDOM_SEED = 2019
JA_STOPWORDS = [
    'ある', 'いる', 'する', 'できる', 'てる', 'なる', 'られる', 'れる',
    'よう', 'こと', 'もの', 'ところ', 'ため', 'さん', 'ちゃん', 'くん', 'そう',
    'これ', 'それ', 'あれ', 'どれ', 'こちら', 'そちら', 'あちら', 'どちら',
    'こんな', 'そんな', 'あんな', 'どんな', 'ここ', 'そこ', 'あそこ', 'どこ',
    'くれる', 'やる', 'くださる', '思う', 'いただく', 'せる', 'みる', 'くる', 'いく',
    'いただける', 'ない', 'やすい', 'いい', 'of', 'in', 'by'
]


def ja_tokenize(line, tokenizer):
    """1行を形態素解析して、助詞、助動詞以外の原形を入れたリストを返す"""
    res = []
    malist = tokenizer.tokenize(line)
    for tok in malist:
        ps = tok.part_of_speech.split(",")[0]
        if ps not in ["形容詞", "動詞", "名詞", "形容動詞", "副詞"]:
            continue
        w = tok.base_form
        if w == "*" or w == "":
            w = tok.surface
        if w == "" or w == "\n":
            continue
        res.append(w)
    return res


def ja_tokenize_file(input_file, output_file=None):
    """日本語のテキストを分かち書きにしたファイルを作成する

    Parameters
    ----------
    input_file: Path
        分かち書きしたい日本語テキストファイル
    output_file: Path (Optional)
        分かち書きにした後の日本語テキストファイル
        指定しない場合は`<input_file>-wakati.txt`というファイル名とする

    Returns
    -------
    文字列
        分かち書きした日本語テキストのファイル名
    """
    if output_file is None:
        input_file_name = input_file.name.rsplit('.', 1)[0]
        output_file = input_file_name + '_wakati.txt'
    JA_TOKENIZER = Tokenizer()
    with open(input_file, 'r', encoding='utf-8') as fin,\
            open(output_file, 'w', encoding='utf-8') as fout:
        text = fin.read()
        square_bracket_removed = re.sub(r'\[.+?\]', '', text)  # はてな記法の[]を削除
        uri_removed = re.sub(  # リンクのURIを削除
            r'https?://[\w/:%#$&?~.=+-]+', '', square_bracket_removed)
        # code_block_pattern = '```.*```'
        # prog = re.compile(code_block_pattern, re.MULTILINE | re.DOTALL)
        # code_block_removed = prog.sub('', uri_removed)
        # <div>や</blockquote>などのHTMLタグを削除
        html_tags_removed = re.sub('</?.+?>', '', uri_removed)
        lines = html_tags_removed.split('\n')
        for line in lines:
            tokenized = ja_tokenize(line, JA_TOKENIZER)
            tokenized_line = ' '.join(tokenized)
            fout.write(tokenized_line + '\n')
    return output_file


if __name__ == '__main__':
    work_dir_po = Path(__file__).parent
    wakati_dir_po = work_dir_po / 'wakati'
    image_dir_po = work_dir_po / 'images'

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_file', help='target text file'
    )
    parser.add_argument(
        '--english', help='specify if target is written in English',
        action='store_true'
    )

    args = parser.parse_args()
    input_file = args.input_file
    is_english = args.english

    input_path = Path(input_file)
    tokenized_path = input_path
    if not is_english:
        tokenized_path = wakati_dir_po / input_path.name
        ja_tokenize_file(input_path, tokenized_path)
    with open(tokenized_path, 'r', encoding='utf-8') as f:
        text = f.read()
        if is_english:
            wc = WordCloud(
                font_path=FONT_FILE, background_color=BG_COLOR,
                random_state=RANDOM_SEED
            )
        else:
            wc = WordCloud(
                font_path=FONT_FILE, background_color=BG_COLOR,
                stopwords=JA_STOPWORDS, random_state=RANDOM_SEED,
                width=800, height=400, collocations=False
            )
        wordcloud = wc.generate(text)
        image = wordcloud.to_image()
        image_file_name = input_path.name.rsplit('.', 1)[0] + '.png'
        image_file_path = image_dir_po / image_file_name
        image.save(image_file_path)
