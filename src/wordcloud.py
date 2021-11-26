from typing import List, Optional

from sudachipy import dictionary, tokenizer

from wordcloud import WordCloud


class SudachiWordCloud(object):
    def __init__(self):
        self.tokenizer_obj = dictionary.Dictionary().create()
        self.mode = tokenizer.Tokenizer.SplitMode.C
        self.hinshi = ["名詞", "動詞", "形容詞", "形容動詞"]

    def tokenize(self, texts: List[str]) -> List[str]:
        tokens: List[str] = []
        for t in texts:
            for m in self.tokenizer_obj.tokenize(t, self.mode):
                if m.part_of_speech()[0] in self.hinshi:
                    tokens.append(m.surface())
        return tokens

    def create_word_cloud(self, tokens: List[str], font_path: Optional[str] = None):
        wc = WordCloud(
            font_path=font_path,
            background_color="white",
            colormap="rainbow",
            margin=2,
            relative_scaling="auto",
        )
        wc.generate(" ".join(tokens))
        return wc
