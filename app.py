import streamlit as st
import pandas as pd
import numpy as np
import zipfile
import os
from pypdf import PdfReader
import re
from pathlib import Path
import shutil

st.title('Luxmii Order Extractor - PDF Rename')

with st.form(key='my_form'):
    file_uploaded = st.file_uploader("Upload")
    submit_button=st.form_submit_button('Submit')



if submit_button:
    with zipfile.ZipFile(file_uploaded, 'r') as zip_ref:
        zip_ref.extractall("extracted")

    files=os.listdir('extracted')
    for i in files:
        inp=f"extracted/{i}"
        
        reader = PdfReader(inp)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        out=re.findall('Order No.:\n\#(\d+)',text)[0]
        os.rename(inp, f'extracted/{out}.pdf')


    fp_zip = Path("output.zip")
    path_to_archive = Path("./extracted")

    with zipfile.ZipFile(fp_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for fp in path_to_archive.glob("**/*"):
            zipf.write(fp, arcname=fp.relative_to(path_to_archive))

    shutil.rmtree('extracted')

    with open("output.zip", "rb") as fp:
        btn = st.download_button(
            label="Download ZIP",
            data=fp,
            file_name="output.zip",
            mime="application/zip"
        )

        
