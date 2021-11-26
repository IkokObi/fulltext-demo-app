import logging
import os
import tempfile
import traceback
from typing import Optional

import fulltext
import streamlit as st

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

# ページ設定
st.set_page_config(page_title="fulltext-demo", page_icon=":snake:")
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
        st.subheader("データの内訳")
        st.text(result[:max_write] + (" ...(略)..." if len(result) > max_write else ""))
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
