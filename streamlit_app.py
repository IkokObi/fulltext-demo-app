import logging
import os
import tempfile
import traceback
from typing import Optional

import fulltext
import streamlit as st

import src

st.set_page_config(page_title="fulltext-demo", page_icon=":snake:")

logger = src.setup_logger(name=__name__, level=logging.INFO)
MAX_WRITE = 30

# ページ設定
st.title("文書ファイル読み取りのデモ")

# ファイルのアップロード
uploaded_file = st.file_uploader("アップロードするファイルを選んでください")
st.caption("ファイルはアップロード後に削除されますが、一切の責任は負いません")
if uploaded_file is not None:
    # fulltextで文字列として読み取る
    result: Optional[str] = None
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
    # - 冒頭部分
    # - ワードクラウド
    # - データ全文（選択形式）
    if result:
        st.success("データの読み取りに成功しました")
        st.subheader(f"データの内訳（冒頭{MAX_WRITE}文字が表示されます）")
        st.text(result[:MAX_WRITE] + (" ...(略)..." if len(result) > MAX_WRITE else ""))

        st.subheader("ワードクラウド")
        st.pyplot(src.SudachiWordCloud().create_word_cloud_image(texts=result.split()))

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
