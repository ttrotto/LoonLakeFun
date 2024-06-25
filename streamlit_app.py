import streamlit as st
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt
import time


# <-- Functions --> #
def fetch():
    conn = st.connection("gsheets",
                         type=GSheetsConnection,
                         ttl=15)
    df = conn.read(ttl=15)
    return df


# <-- Init page --> #
st.write("""
# Live Dashboard
Pick attribute of interest:
""")

# options
option = st.selectbox(
    "Attribute",
    ("height", "dbh", "count")
)

# container
placeholder = st.empty()

# refresh data
if st.button('Refresh'):
    df = fetch()
    with placeholder.container():
        fig, ax = plt.subplots()
        ax.hist(df[option])
        st.pyplot(fig)
        time.sleep(15)
