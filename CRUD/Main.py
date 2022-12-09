import datetime
import sqlite3
import streamlit as st
import pandas as pd

db_file = 'Data/Daily_Measures.db'

conn = sqlite3.connect(db_file)

cur = conn.cursor()





TODs = ("Morning", "Midday", "Night")
measures = ('Glucose', 'Keytones', 'Weight', 'BP-S', 'BP-D', 'Uric Acid')
currentDateTime = datetime.datetime.now()


def Create(DB):
    st.subheader("Create Records")

    select_query = """SELECT * FROM MEASUREVALUES ORDER BY ROWID DESC LIMIT 5;"""

    create_query = """INSERT INTO MEASUREVALUES
                            (Date,
                            TOD,
                            Measure,
                            Value)
                            VALUES (?, ?, ?, ?);"""

    with st.form(key='query_form'):
            date = st.date_input(
                'Enter Date', value=currentDateTime)
            TOD = st.selectbox("Select Time of Day", TODs, index=0 )
            measure = st.selectbox("Select Data Point", measures, index=0)

            value = st.number_input('Enter Data Value', step=1e-1, format="%.1f")

            data_tuple = (date,
                          TOD,
                          measure,
                          value)

            submit_data = st.form_submit_button("Submit Data")

    if submit_data:
                

                conn = sqlite3.connect(db_file)
                cur = conn.cursor()
                try:
                    cur.execute(create_query, data_tuple)
                    st.info("Data Submitted Successfully")
                    conn.commit()
                except sqlite3.Error as er:
                    st.info("Error Submitting Record: " + str(er))

                # df = pd.read_sql(select_query, con=conn)   OR 

                try:
                    cur.execute(select_query)
                    df = pd.DataFrame(cur.fetchall())
                except sqlite3.Error as er:
                    st.info("Error Reading Records: " + str(er))

                with st.expander("Pretty Table"):
                    st.write(df)

                conn.commit()
                conn.close()
def Read(DB):
    st.subheader("Read Records")

def Update(DB):
    st.subheader("Update Records")

def Delete(DB):
    st.subheader("Delete Records")

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

            # if submit_data:
            #     st.info("Data Submitted")
            #     st.info(insert_query)

            #     conn = sqlite3.connect(db_file)
            #     cur = conn.cursor()

            #     cur.execute(insert_query, data_tuple)
            #     conn.commit()

            #     df = pd.read_sql(select_query, con=conn)

            #     with st.expander("Pretty Table"):
            #         st.write(df)

            #     conn.commit()
            #     conn.close()


def main():
    st.title("Health Database Management")

    menu = ["Create Records", "Read Records", "Update Records", "Delete Records"]

    page = st.sidebar.selectbox("Menu", menu)
    
    actions = {'Create Records': Create,
               'Read Records': Read, 'Update Records': Update,'Delete Records': Delete}

    action = actions.get(page)

    action('page')

if __name__ == '__main__':
    main()
