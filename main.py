import time
import os
import sqlite3
from datetime import datetime
import streamlit as st
import pandas as pd

DB_PATH = "data/hives.db"
os.makedirs("data", exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS hives
                 (hive_id INTEGER PRIMARY KEY,
                  weight_kg REAL,
                  level INTEGER,
                  extracting BOOLEAN DEFAULT 0,
                  last_update TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Mock data for testing (remove later)
if 'mock_added' not in st.session_state:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO hives VALUES (1, 8.5, 71, 0, ?)", (datetime.now().isoformat(),))
    conn.commit()
    conn.close()
    st.session_state.mock_added = True

# Dashboard
st.set_page_config(page_title="SMART NYUKI", layout="wide")
st.title("🐝 SMART NYUKI - Live Dashboard")

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM hives", conn)
conn.close()

if df.empty:
    st.info("Waiting for data from hives...")
else:
    for _, row in df.iterrows():
        hive_id = row['hive_id']
        weight = row['weight_kg']
        level = row['level']
        extracting = row['extracting']

        with st.container(border=True):
            st.subheader(f"Hive {hive_id}")
            col1, col2 = st.columns([3, 1])
            with col1:
                st.metric("Weight", f"{weight:.2f} kg")
                st.progress(level / 100)
                st.caption(f"{level}% full • Last update: {row['last_update']}")
            with col2:
                if level >= 50:
                    if st.button("HARVEST HONEY", key=f"btn_{hive_id}", type="primary"):
                        conn = sqlite3.connect(DB_PATH)
                        c = conn.cursor()
                        c.execute("UPDATE hives SET extracting = 1 WHERE hive_id = ?", (hive_id,))
                        conn.commit()
                        conn.close()
                        st.success(f"Harvest command sent to Hive {hive_id}!")
                else:
                    st.button("Not Ready", disabled=True)

# Auto-refresh every 10 seconds
time.sleep(10)
st.rerun()
