import os
import tempfile

import fulltext
import streamlit as st

# File upload
uploaded_file = st.file_uploader("アップロードするファイルを選んでください")

if uploaded_file is not None:
    result: str = ""

    file_name = uploaded_file.name
    extension = file_name.rsplit(".")[-1] if len(file_name.rsplit(".")) > 1 else None

    # Read data with fulltext
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        result = fulltext.get(file_path)

    # Data presentation
    max_write = 30
    if result:
        st.success("ファイルの読み取りに成功しました")
        st.subheader("ファイルの内訳")
        st.write(result[:max_write] + (" ...(略)..." if len(result) > max_write else ""))
        with st.expander("データを全て表示する"):
            st.write(result)
    else:
        st.error("ファイルの読み取りに失敗しました")
