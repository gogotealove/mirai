import os

import dotenv
import streamlit as st

dotenv.load_dotenv()
st.write("TEST")
st.write(os.environ["OPENAI_API_KEY"])
