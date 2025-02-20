import os
from io import BytesIO
import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#Setup's App/Page
st.set_page_config(page_title="📁 Data Sweeper",layout="centered")
st.title("📁 Data Sweeper")
st.subheader("Convert your files into CSV or Excel formats with built-in data cleaning and visualization")

#Say Hi!
with st.chat_message("assistant"):
    st.write("Hello 👋")
    

#Upload func
st.subheader("Select a demo dataset")
demo_dataset = st.selectbox(
    "Choose a demo dataset",
    ("None", "Iris", "Diamonds", "Titanic", "Tips"),
    index=0
)

if demo_dataset != "None":
    if demo_dataset == "Iris":
        df = sns.load_dataset("iris")
    elif demo_dataset == "Diamonds":
        df = sns.load_dataset("diamonds")
    elif demo_dataset == "Titanic":
        df = sns.load_dataset("titanic")
    elif demo_dataset == "Tips":
        df = sns.load_dataset("tips")
    
    # Display file's information
    st.subheader(f"Some Information about {demo_dataset}")
    with st.chat_message("assistant"):
        st.write(f"Loaded demo dataset: {demo_dataset}")
        # Display the rows & columns of Data
        st.write("Total Rows: ",df.shape[0])
        st.write("Total Columns: ",df.shape[1])
        # Fieelds of Data
        st.write(df)
        
        # Display colunms name and selected data types
        st.write("Column Nmaes and Data Types", df.dtypes)
    
        
    
    # Data cleaning options
    st.subheader("Data Cleaning Opts")
    with st.chat_message("assistant"):
        opt = st.selectbox(
            "Do want to clean this file?",
            ("yes", "no"),
            index=None,
            placeholder="Select..."
        )
    if opt == "yes":
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"Remove Duplicates from {demo_dataset}"):
                df.drop_duplicates(inplace=True)
                st.write("Duplicates Removed!")
                
        with col2:
            if st.button(f"Fill Missing Values for {demo_dataset}"):
                numeric_cols = df.select_dtypes(include=("number")).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.write("Missing Values have been Filled!")
    elif opt == "no":
        st.warning("Ok its your choice!!")
           
    # Choose specific Columns to Convert or Keep
    st.subheader("Select Columns to Convert!")    
    columns = st.multiselect(f"Choose Columns for {demo_dataset}", df.columns, default=df.columns)
    df = df[columns]
    
    # Visualization
    st.subheader(f"Data Visualization for {demo_dataset}")
    if st.checkbox(f"Show Visualization for {demo_dataset}"):
        st.line_chart(df.select_dtypes(include='number'))
    
    # Convert the file 
    st.subheader("Conversion Opts")
    conversion_type = st.radio(f"Convert {demo_dataset} to:", ["CSV", "Excel", "Json"], key=demo_dataset)
    if st.button(f"Convert {demo_dataset}"):
        buffer = BytesIO()
        if conversion_type == "CSV":
            df.to_csv(buffer, index=False)
            file_name = f"{demo_dataset}.csv"
            mime_type = "text/csv"
            
        elif conversion_type == "Json":
            buffer.write(df.to_json(orient="records").encode())
            file_name = f"{demo_dataset}.json"
            mime_type = "application/json"
            
        elif conversion_type == "Excel":
            df.to_excel(buffer, index=False, engine="openpyxl")
            file_name = f"{demo_dataset}.xlsx"
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        buffer.seek(0)
        
        # Download Button
        st.download_button(
            label=f"Download {demo_dataset} as {conversion_type}",
            data=buffer,
            file_name=file_name,
            mime=mime_type                
        )
        st.success(
            st.balloons()
        )
uploaded_files = st.file_uploader("Upload files here (CSV / XLSX):",type=["csv","xlsx"],accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue
        
        #File Info
        with st.chat_message("assistant"):
            #Display file's information
            st.write(f"Your 📁 File Name is '{file.name}' and Your 📂 File Size is '{file.size/1024}'")
           
        #Show some rows of our data-frame
        st.write("Preview the Head of Data-frame")
        st.dataframe(df)
        
        #Data cleaning options
        st.subheader("Data Cleaning Opts")
        with st.chat_message("assistant"):
            opt = st.selectbox(
                "Do want to clean this file?",
                ("yes","no"),
                index=None,
                placeholder="Select..."
            )
        if opt == "yes":
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")
                    
            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=("number")).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values have been Filled!")
        elif opt == "no":
            st.warning("Ok its your choice!!")
               
        #Choose specific Columns to Convert or Keep
        st.subheader("Select Columns to Convert!")    
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]
        
        #Visualization
        st.subheader(f"Data Visualization for {file.name}")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.line_chart(df.select_dtypes(include='number'))
        
        #Convert the file 
        st.subheader("Conversion Opts")
        conversion_type = st.radio(f"Convert {file.name} to:",["CSV","Excel","Json"],key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
                
            elif conversion_type == "Json":
                buffer.write(df.to_json(orient="records").encode())
                file_name = file.name.replace(file_ext, ".json")
                mime_type = "application/json"
                
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine="openpyxl")
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)
            
            #Download Button
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name = file_name,
                mime=mime_type                
            )
            st.success(
                st.balloons()
            )