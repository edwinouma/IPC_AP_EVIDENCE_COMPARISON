# Import the necessary modules
import os
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Change the current working directory
os.chdir('C:/WORK/IPC-HQ/Evidence Comparison Analysis/AP_EVIDENCE_COMPARISON')

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
st.set_page_config(layout="wide")  # Set the layout to wide mode

# Set the title with reduced size and centered
st.markdown("<h1 style='font-size: 24px; text-align: center;'>Analysis Platform</h1>", unsafe_allow_html=True)
st.markdown(
    "<h2 style='font-size: 18px; text-align: center;'>Evidence Comparison for Different Countries Across Different Periods</h2>",
    unsafe_allow_html=True
)

# Country selection
selected_country = st.multiselect('Select Country', options=country, default=['Myanmar'])

# Update graph and table based on selected country
if selected_country:
    evidence_data1 = evidence_data[evidence_data['country'].isin(selected_country)]
    evidence_data2 = pd.DataFrame(
        evidence_data1.groupby(['Upload', 'analysis_time'])['Total_number_of_evidence'].sum()).reset_index()

    # Pivot the table to wide format
    evidence_data_wide = evidence_data2.pivot(index='Upload', columns='analysis_time',
                                              values='Total_number_of_evidence').fillna(0).reset_index()

    # Reduce column names to 7 characters
    evidence_data_wide.columns = [str(col)[:7] for col in evidence_data_wide.columns]

    # Calculate percentages
    evidence_data_percentage = evidence_data_wide.copy()
    evidence_data_percentage.iloc[:, 1:] = evidence_data_percentage.iloc[:, 1:].div(
        evidence_data_percentage.iloc[:, 1:].sum(axis=0), axis=1) * 100

    # Create the sum graph
    evidence_number = go.Figure()
    for analysis_time in evidence_data2['analysis_time'].unique():
        upload_type_data = evidence_data2[evidence_data2['analysis_time'] == analysis_time]
        evidence_number.add_trace(go.Bar(
            x=upload_type_data['Upload'],
            y=upload_type_data['Total_number_of_evidence'],
            name=str(analysis_time)[:7]  # Truncate legend text to 7 characters
        ))

    evidence_number.update_xaxes(title_text='Upload Methods')
    evidence_number.update_yaxes(title_text='Number of pieces of evidence')
    evidence_number.update_layout(
        title='Grouped Bar Chart of IPC AP number of evidence across the period',
        barmode='group',
        width=600,  # Adjusted width of the chart to use more of the page
        height=400,  # Adjusted height of the chart
        margin=dict(l=50, r=50, t=50, b=50),  # Add margin to create space for the border
        paper_bgcolor='white',  # Background color of the paper
        plot_bgcolor='white',  # Background color of the plot
        showlegend=True,
        legend=dict(
            bordercolor="Black",
            borderwidth=2
        ),
        shapes=[  # Add a border around the entire graph
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(
                    color="Black",
                    width=2
                )
            )
        ]
    )

    # Create the percentage graph
    evidence_percentage = go.Figure()
    for analysis_time in evidence_data_percentage.columns[1:]:
        evidence_percentage.add_trace(go.Bar(
            x=evidence_data_percentage['Upload'],
            y=evidence_data_percentage[analysis_time],
            name=str(analysis_time)[:7]  # Truncate legend text to 7 characters
        ))

    evidence_percentage.update_xaxes(title_text='Upload Methods')
    evidence_percentage.update_yaxes(title_text='Percentage of pieces of evidence')
    evidence_percentage.update_layout(
        title='Grouped Bar Chart of IPC AP percentage of evidence across the period',
        barmode='group',
        width=600,  # Adjusted width of the chart to use more of the page
        height=400,  # Adjusted height of the chart
        margin=dict(l=50, r=50, t=50, b=50),  # Add margin to create space for the border
        paper_bgcolor='white',  # Background color of the paper
        plot_bgcolor='white',  # Background color of the plot
        showlegend=True,
        legend=dict(
            bordercolor="Black",
            borderwidth=2
        ),
        shapes=[  # Add a border around the entire graph
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(
                    color="Black",
                    width=2
                )
            )
        ]
    )

    # Display the charts and tables side by side
    col1, col2 = st.columns(2)

    with col1:
        with st.expander("Evidence Data Wide Format",expanded=True):
            st.dataframe(evidence_data_wide, width=600, height=400)
        with st.expander("Evidence Data Percentage Format",expanded=True):
            st.dataframe(evidence_data_percentage, width=600, height=400)

    with col2:
        with st.expander("Evidence Number Chart",expanded=True):
            st.plotly_chart(evidence_number, width = 600, height = 400)
        with st.expander("Evidence Percentage Chart",expanded=True):
            st.plotly_chart(evidence_percentage, width = 600, height = 400)