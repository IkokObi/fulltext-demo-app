import logging
import os
import tempfile
import traceback
from typing import Optional

import fulltext
import japanize_matplotlib  # For plot with japanese
import streamlit as st
from matplotlib import font_manager
from matplotlib import pyplot as plt

from src.wordcloud import SudachiWordCloud

st.set_page_config(page_title="fulltext-demo", page_icon=":snake:")

# loggerの設定
level = logging.INFO
logger = logging.getLogger(__name__)
if len(logger.handlers) == 0:
    """ レンダリングの関係で複数回実行されるため、初回のみhandlerを設定する """
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler_format = logging.Formatter(
        fmt="%(levelname)s %(asctime)s: %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z",
    )
    handler.setFormatter(handler_format)
    logger.addHandler(handler)
    logger.propagate = False


# 日本語フォントパスの取得
japanese_font_path = None
for f in font_manager.fontManager.ttflist:
    if f.name == "IPAexGothic":
        japanese_font_path = f.fname


# ページ設定
st.title("文書ファイル読み取りのデモ")

# ファイルのアップロード
uploaded_file = st.file_uploader("アップロードするファイルを選んでください")

if uploaded_file is not None:
    result: Optional[str] = None

    file_name = uploaded_file.name
    extension = file_name.rsplit(".")[-1] if len(file_name.rsplit(".")) > 1 else None

    # fulltextで文字列として読み取る
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, uploaded_file.name)
        try:
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            result = fulltext.get(file_path)
            logger.info("Reading data succeeded")
        except Exception:
            logger.error("Reading data failed")
            tb = traceback.format_exc()
            logger.error(tb)

    # データの表示
    max_write = 30
    if result:
        st.success("データの読み取りに成功しました")
        st.subheader(f"データの内訳（冒頭{max_write}文字が表示されます）")
        st.text(result[:max_write] + (" ...(略)..." if len(result) > max_write else ""))

        st.subheader("ワードクラウド")
        wordcloud = SudachiWordCloud()
        tokens = wordcloud.tokenize(texts=result.split())
        wc = wordcloud.create_word_cloud(tokens=tokens, font_path=japanese_font_path)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

        with st.expander("データを全て表示する"):
            st.text(result)
    else:
        st.error("ファイルの読み取りに失敗しました")
        reasons = [
            "\n- 対応していないファイル形式である",
            "\n- ファイルの中身が空である",
            "\n- ファイルに文字列が含まれていない",
            "\n- ファイルサイズが大きすぎる",
        ]
        st.markdown("以下のような原因が考えられます" + "".join(reasons))
