from datetime import datetime
import sqlite3
import streamlit as st
import pandas as pd
from bisect import bisect
from st_aggrid import  GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode
import base64

db_file = 'Data/Daily_Measures.db'

conn = sqlite3.connect(db_file)
cur = conn.cursor()

TODs = ("Morning", "Midday", "Night")
measures = ('Glucose', 'Keytones', 'Weight', 'BP-S', 'BP-D', 'Uric Acid')

#==========================================================================================
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    ) 

#==========================================================================================
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://cdn.pixabay.com/photo/2019/04/24/11/27/flowers-4151900_960_720.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

#==========================================================================================
def Create(DB):
    st.subheader("Create Records")

    # select_query = """SELECT * FROM MEASUREVALUES ORDER BY ROWID DESC LIMIT 5;"""

    # create_query = """INSERT INTO MEASUREVALUES
    #                         (Date,
    #                         TOD,
    #                         Measure,
    #                         Value)
    #                         VALUES (?, ?, ?, ?);"""

    # currentDateTime = datetime.now()
    # tods = ("Night","Morning","Midday","Night",)
    # tod_breaks = (0, 6, 12, 20, 24)
    # tod_index = bisect(tod_breaks,currentDateTime.hour)-1
    # tod = tods[tod_index]

    # with st.form(key='query_form'):
    #         date = st.date_input(
    #             'Enter Date', value=currentDateTime.date())
    #         TOD = st.selectbox("Select Time of Day", TODs, index=TODs.index(tod) )
    #         measure = st.selectbox("Select Data Point", measures, index=0 )

    #         value = st.number_input('Enter Data Value', step=1e-1, format="%.1f")

    #         data_tuple = (date,
    #                       TOD,
    #                       measure,
    #                       value)

    #         submit_data = st.form_submit_button("Submit Data")

    # if submit_data:
                

    #             conn = sqlite3.connect(db_file)
    #             cur = conn.cursor()
    #             try:
    #                 cur.execute(create_query, data_tuple)
    #                 st.info("Data Submitted Successfully")
    #                 conn.commit()
    #             except sqlite3.Error as er:
    #                 st.info("Error Submitting Record: " + str(er))

    #             df = pd.read_sql(select_query, con=conn)

                # try:
                #     cur.execute(select_query)
                #     df = pd.DataFrame(cur.fetchall())
                # except sqlite3.Error as er:
                #     st.info("Error Reading Records: " + str(er))

                # with st.expander("Pretty Table"):
                #     st.write(df)
               
                # conn.commit()
                # conn.close()
#==========================================================================================                
def Read(page):
    st.subheader("Read Records")

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    select_query = """SELECT * FROM MEASUREVALUES ORDER BY ROWID DESC LIMIT 6;"""
    data = pd.read_sql(select_query, con=conn)
    
    with st.form('AgGrid inside a form') as f:
        gb = GridOptionsBuilder.from_dataframe(data)
        gb.configure_auto_height(autoHeight=True)
        gb.configure_pagination(paginationPageSize=6) 
        gb.configure_side_bar() 
        gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") 
        gb.configure_column("Date", header_name="Date", editable=True)
        gb.configure_column("TOD",
            header_name="TOD",
            cellEditor='agRichSelectCellEditor',
            cellEditorParams={'values':TODs},
            cellEditorPopup=True,
            editable=True)
        gb.configure_column("Measure",
            header_name="Measure",
            cellEditor='agRichSelectCellEditor',
            cellEditorParams={'values':measures},
            cellEditorPopup=True,
            editable=True)
        gridOptions = gb.build()
        gb.configure_grid_options(enableRangeSelection=True)

        grid_response = AgGrid(
            data,
            autoHeight=True,
            gridOptions=gridOptions,
            data_return_mode='AS_INPUT', 
            update_mode='MODEL_CHANGED', 
            fit_columns_on_grid_load=False,
            enable_enterprise_modules=True,
            height=350, 
            width='100%',
            theme = "streamlit",
            editable=True,
            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
        )

        submit_data = st.form_submit_button()

    if submit_data:
        data = grid_response['data']
        selected = grid_response['selected_rows'] 
        new_frame = pd.DataFrame(selected)

        grid_response = AgGrid(
            new_frame,
            gridOptions=gridOptions,
            data_return_mode='AS_INPUT', 
            update_mode='MODEL_CHANGED', 
            fit_columns_on_grid_load=False,
            enable_enterprise_modules=True,
            height=350, 
            width='100%',
            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
            )
    conn.close()
   
#==========================================================================================    
def Update(DB):
    st.subheader("Update Records")
#==========================================================================================
def Delete(DB):
    st.subheader("Delete Records")
#==========================================================================================
def analytics(page):
    st.subheader("Analytics")

    # query = """SELECT * FROM MEASUREVALUES;"""
    # conn = sqlite3.connect(db_file)
    # df = pd.read_sql(query, con=conn)

    # measure_options = df['Measure'].unique().tolist()
    # TOD_options = df['TOD'].unique().tolist()

    # measures_selected = st.multiselect("Select a Measure", measure_options)
    # TODs_selected = st.multiselect("Select TODs", TOD_options)

    # df = df[df["Measure"].isin(measures_selected)]
    # df = df[df["TOD"].isin(TODs_selected)]

    # with st.expander("Pretty Table 1"):
    #     st.dataframe(df)

    # conn.close()
#==========================================================================================
def about(page):
    st.subheader("About")

#==========================================================================================
def data_entry(page):
    st.subheader("Data Entry")
    # insert_query = """INSERT INTO MEASUREVALUES
    #                         (Date,
    #                         TOD,
    #                         Measure,
    #                         Value)
    #                         VALUES (?, ?, ?, ?);"""

    # select_query = """SELECT * FROM MEASUREVALUES;"""

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

#==========================================================================================
def main():
    image_file = "BH_Sunset_001.png"
    add_bg_from_local(image_file)

    st.title("Health Database Management")

    menu = ["Create Records", "Read Records", "Update Records", "Delete Records"]

    page = st.sidebar.selectbox("Menu", menu)
    
    actions = {'Create Records': Create,
               'Read Records': Read, 'Update Records': Update,'Delete Records': Delete}

    action = actions.get(page)

    action('page')
#==========================================================================================
if __name__ == '__main__':
    main()
