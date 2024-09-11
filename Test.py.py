# Import the necessary modules
import os
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Change the current working directory
os.chdir('C:/WORK/IPC-HQ/Evidence Comparison Analysis')

# Reading the AP Evidence Comparison data for use
cols = ['Upload', 'Total_number_of_evidence', 'country', 'analysis_time', 'analysis_type']
evidence_data = pd.read_excel('AP_evidence_comparison_08sep2024.xlsx', usecols=cols)

upload_method = evidence_data['Upload'].unique()
country = evidence_data['country'].unique()
analysis_type = evidence_data['analysis_type'].unique()
analysis_time = evidence_data['analysis_time'].unique()


import logging
logging.getLogger('streamlit.runtime.scriptrunner_utils').setLevel(logging.ERROR)

# Streamlit app layout
st.title('Analysis Platform')
st.header('Evidence Comparison for Different Countries Across Different Periods')

# Country selection
selected_country = st.multiselect('Select Country', options=country, default=['Myanmar'])

# Update graph based on selected country
if selected_country:
    evidence_data1 = evidence_data[evidence_data['country'].isin(selected_country)]
    evidence_data2 = pd.DataFrame(evidence_data1.groupby(['Upload', 'analysis_time'])['Total_number_of_evidence'].sum()).reset_index()

    evidence_number = go.Figure()
    for analysis_time in evidence_data2['analysis_time'].unique():
        upload_type_data = evidence_data2[evidence_data2['analysis_time'] == analysis_time]
        evidence_number.add_trace(go.Bar(
            x=upload_type_data['Upload'],
            y=upload_type_data['Total_number_of_evidence'],
            name=str(analysis_time)
        ))

    evidence_number.update_xaxes(title_text='Upload Methods')
    evidence_number.update_yaxes(title_text='Number of pieces of evidence')
    evidence_number.update_layout(
        title='Grouped Bar Chart of IPC AP number of evidence across the period',
        barmode='group',
        width=600,  # For width of the chart
        height=400,  # For height of the chart
    )

    st.plotly_chart(evidence_number)

