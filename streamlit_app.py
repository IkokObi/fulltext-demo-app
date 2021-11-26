import os
import tempfile
import traceback
from typing import Optional

import fulltext
import streamlit as st

st.title("文書ファイル読み取りのデモアプリ")

# File upload
uploaded_file = st.file_uploader("アップロードするファイルを選んでください")

if uploaded_file is not None:
    result: Optional[str] = None

    file_name = uploaded_file.name
    extension = file_name.rsplit(".")[-1] if len(file_name.rsplit(".")) > 1 else None

    # Read data with fulltext
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, uploaded_file.name)
        try:
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            result = fulltext.get(file_path)
            print("Success", repr(result))
        except Exception:
            tb = traceback.format_exc()
            print("Error!")

    # Data presentation
    max_write = 30
    if result:
        st.success("データの読み取りに成功しました")
        st.subheader("データの内訳")
        st.text(result[:max_write] + (" ...(略)..." if len(result) > max_write else ""))
        with st.expander("データを全て表示する"):
            st.text(result)
    else:
        st.error("ファイルの読み取りに失敗しました")
        st.markdown("以下のような原因が考えられます\n- ファイル形式に対応していない\n- 空のファイル\n- 文字列が含まれていない")
