from datetime import datetime
import sqlite3
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import streamlit as st

db_file = 'Data/Daily_Measures.db'

conn = sqlite3.connect(db_file)

cur = conn.cursor()

sqlite_insert_with_param = """INSERT INTO MEASUREVALUES
                            (Date,
                            TOD,
                            Measure,
                            Value)
                            VALUES (?, ?, ?, ?);"""

sqlite_select_query1 = """SELECT * FROM MEASUREVALUES ORDER BY ROWID DESC LIMIT 5;"""


TODs = ("Morning", "Midday", "Night")
measures = ('Glucose', 'Keytones', 'Weight', 'BP-S', 'BP-D', 'Uric Acid')
currentDateTime = datetime.datetime.now()


def analytics(page):
    st.subheader("Analytics")

    query = """SELECT * FROM MEASUREVALUES;"""
    conn = sqlite3.connect(db_file)
    df = pd.read_sql(query, con=conn)

    measure_options = df['Measure'].unique().tolist()
    TOD_options = df['TOD'].unique().tolist()

    measures_selected = st.multiselect("Select a Measure", measure_options)
    TODs_selected = st.multiselect("Select TODs", TOD_options)

    df = df[df["Measure"].isin(measures_selected)]
    df = df[df["TOD"].isin(TODs_selected)]

    with st.expander("Pretty Table 1"):
        st.dataframe(df)

    conn.close()

def about(page):
    st.subheader("About")


def data_entry(page):
    st.subheader("Data Entry")
    insert_query = """INSERT INTO MEASUREVALUES
                            (Date,
                            TOD,
                            Measure,
                            Value)
                            VALUES (?, ?, ?, ?);"""

    select_query = """SELECT * FROM MEASUREVALUES;"""

    col1, col2 = st.columns([1, 2])

    with col1:
        with st.form(key='query_form'):
            date = st.date_input(
                'Enter Date', value=currentDateTime)
            TOD = st.selectbox("Select Time of Day", TODs, index=0 )
            measure = st.selectbox("Select Data Point", measures, index=0)

            value = st.number_input(
                'Enter Data Value', step=1e-1, format="%.1f")

            data_tuple = (date,
                          TOD,
                          measure,
                          value)

            submit_data = st.form_submit_button("Submit Data")

    with col2:
        if submit_data:
            st.info("Data Submitted")
            st.info(insert_query)

            conn = sqlite3.connect(db_file)
            cur = conn.cursor()

            cur.execute(insert_query, data_tuple)
            conn.commit()

            df = pd.read_sql(select_query, con=conn)

            with st.expander("Pretty Table"):
                st.write(df)

            conn.commit()
            conn.close()


def main():
    st.title("Health Data Tracker")

    menu = ["Data Entry", "Analytics", "About"]

    page = st.sidebar.selectbox("Menu", menu)
    
    actions = {'Data Entry': data_entry,
               'About': about, 'Analytics': analytics}

    action = actions.get(page)

    action('page')

if __name__ == '__main__':
    main()
