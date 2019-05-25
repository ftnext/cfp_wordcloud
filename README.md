# CFP WordCloud

トークのプロポーザルが第三者から見るとどう見えるかの参考にWordCloudで可視化してみた  
（CFP以外の用途にも利用可能）

## 開発環境

- macOS 10.14.4
- Python 3.7.3

## 準備

```shell
git clone https://github.com/ftnext/cfp_wordcloud.git
cd cfp_wordcloud
pip install -r requirements.txt
```

## フォルダ構成

```shell
cfp_wordcloud
├── SourceHanCodeJP-Regular.otf  # WordCloud日本語表示用フォントファイル
├── draw_cloud.py
├── images  # WordCloud画像用フォルダ
├── requirements.txt
└── wakati  # 分かち書き日本語ファイル用フォルダ
```

## 使い方

対応言語

- 日本語
- 英語

### 日本語

`python draw_cloud.py sample_file.txt`

→ imagesフォルダに画像`sample_file.png`ができる。  
また、助詞と助動詞を除いて単語の原形を半角スペースで区切ったファイル`sample_file.txt`がwakatiフォルダにできる。

対象のファイルはパスで指定可能（リポジトリのフォルダの外のファイルも対象にできる）

### 英語

`python draw_cloud.py sample_english_file.txt --english`

※**english**オプションを指定する（指定し忘れると英語のストップワードが効かない）

→ imagesフォルダに画像`sample_english_file.png`ができる。  
wakatiフォルダには何もできない（分かち書きしないため）

## その他

フォントは[adobe-fonts/source-han-code-jp](https://github.com/adobe-fonts/source-han-code-jp)より
