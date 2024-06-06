import streamlit as st
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt
import time


# <-- Functions --> #
def fetch():
    conn = st.connection("gsheets",
                         type=GSheetsConnection,
                         ttl=5)
    df = conn.read(ttl=5)
    return df


st.write("""
# Live Dashboard
Pick attribute of interest:
""")

# options
option = st.selectbox(
    "Attribute",
    ("height", "dbh")
)

# container
placeholder = st.empty()

# refresh data
while True:
    df = fetch()
    print(df)
    with placeholder.container():
        fig, ax = plt.subplots()
        ax.hist(df[option])
        st.pyplot(fig)
        time.sleep(5)
