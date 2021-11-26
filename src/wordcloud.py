from typing import List

import japanize_matplotlib  # For plot with japanese
from matplotlib import font_manager
from matplotlib import pyplot as plt
from sudachipy import dictionary, tokenizer

from wordcloud import WordCloud


class SudachiWordCloud(object):
    def __init__(self):
        self.tokenizer_obj = dictionary.Dictionary().create()
        self.mode = tokenizer.Tokenizer.SplitMode.C
        self.hinshi = ["名詞"]

        # 日本語フォントパスの取得
        self.japanese_font_path = None
        for f in font_manager.fontManager.ttflist:
            if f.name == "IPAexGothic":
                self.japanese_font_path = f.fname

    def _tokenize(self, texts: List[str]) -> List[str]:
        tokens: List[str] = []
        for t in texts:
            for m in self.tokenizer_obj.tokenize(t, self.mode):
                if m.part_of_speech()[0] in self.hinshi:
                    tokens.append(m.surface())
        return tokens

    def _generate_word_cloud(self, tokens: List[str]):
        wc = WordCloud(
            font_path=self.japanese_font_path,
            background_color="white",
            colormap="rainbow",
            margin=2,
            relative_scaling="auto",
        )
        wc.generate(" ".join(tokens))
        return wc

    def create_word_cloud_image(self, texts: List[str]):
        tokens = self._tokenize(texts)
        wc = self._generate_word_cloud(tokens)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        return fig
