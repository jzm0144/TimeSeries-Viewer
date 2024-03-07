# ------------------------------ Libraries ------------------------------ #
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
from datetime import date, datetime, timedelta
import time, os, pickle
import numpy as np
from utils import *
from io import StringIO

# ------------------------------ Configuration ------------------------------ #

st.set_page_config(page_title='TS Viewer', page_icon=':rocket:', layout='wide')

# ------------------------------ File Uploader ------------------------------ #

uploaded_file = st.file_uploader("Choose a file")

placeholderTable0 = st.empty()
placeholderFilter0 = st.empty()
placeholderTable1 = st.empty()
placeholderFilterKPIs = st.empty()
placeholderAxisFilters = st.empty()
placeholderFig1 = st.empty()



if uploaded_file is not None:
    # read the csv file:
    df = pd.read_csv(uploaded_file)
    with placeholderTable0.container():
        st.write(df, use_container_width=True)
    with placeholderFilter0.container():
        TimeAxis_KPIs = st.multiselect(label='**Pick one for more time axis fields in correct order**',
                                       options=df.columns.tolist())
    with placeholderTable1.container():
            if len(TimeAxis_KPIs) > 1:
                df2 = df
                df2["ds"] = df2[TimeAxis_KPIs[0]].astype(str) + " " + df2[TimeAxis_KPIs[1]].astype(str)
                df2['ds'] = pd.to_datetime(df2['ds'], format='%m/%d/%Y %I:%M:%S %p')
                df2 = df2.sort_values(['ds'], ascending=[True]).reset_index(drop=True)
                st.write(df2, use_container_width=True)
                st.divider()
            else:
                None
    with placeholderFilterKPIs.container():
        primaryAxis, secondaryAxis = st.columns(2)
        with primaryAxis:
            pri_options_KPIs = st.multiselect(label='**Primary fields to visualize against DateTime Axis (only numeric/float columns)**',
                                        options=df2.columns.tolist())
        with secondaryAxis:
            sec_options_KPIs = st.multiselect(label='**Secondary fields to visualize against DateTime Axis (only numeric/float columns)**',
                                        options=df2.columns.tolist())
    with placeholderAxisFilters.container():
        cc1, cc2, cc3 , cc4, cc5 = st.columns(5)
        with cc1:
            option_Y1Range0 = st.selectbox(label='**Left Y Axis**', options=np.arange(-100,5000))
        with cc2:
            option_Y1Range1 = st.selectbox(label='**Left Y Axis**', options=np.arange(5000,-100,-1))
        with cc3:
            option_Y2Range0 = st.selectbox(label='**Right Y Axis**', options=np.arange(-100, 5000))
        with cc4:
            option_Y2Range1 = st.selectbox(label='**Right Y Axis**', options=np.arange(5000,-100,-1))
        with cc5:
            option_categ_or_cont = st.radio(label="**Categorical**", horizontal=True, options=['Yes', 'No'])
    
    with placeholderFig1.container():
        fig = sp.make_subplots(specs=[[{"secondary_y": True}]])
        df3 = df2
        # Primary
        for col_p in pri_options_KPIs:
            fig.add_trace(go.Line(x=df3.ds,
                                y=df3[col_p],
                                name=col_p,
                                line=dict(width=4)
                                ),
                         secondary_y=False)
            
        for col_s in sec_options_KPIs:
            fig.add_trace(go.Line(x=df3.ds,
                                y=df3[col_s],
                                name=col_s,
                                line=dict(width=4)
                                ),
                         secondary_y=True)
        fig.update_yaxes(color='#000000', 
                         title_text="<b>Primary Axis </b> (units)",
                         range=[option_Y1Range0, option_Y1Range1],
                         gridcolor="#ffffff",
                         tickfont={"color":"#000000", "family":"sans serif", "size":14},
                         zeroline=False,
                         secondary_y=False)
        fig.update_yaxes(color='#000000',
                                title_text="<b>Secondary Axis</b> (units)",
                                range=[option_Y2Range0, option_Y2Range1],
                                gridcolor="#ffffff",
                                tickfont={"color":"#000000", "family":"sans serif", "size":14},
                                zeroline=False,
                                secondary_y=True)

        if option_categ_or_cont == 'Yes':
            option_categ_or_cont = 'category'
        if option_categ_or_cont == 'No':
            option_categ_or_cont = '-'
        fig.update_xaxes(type=option_categ_or_cont,
                            color='#000000',
                            gridcolor="#ffffff",
                            tickfont={"color":"#000000", "family":"sans serif", "size":11},
                            automargin=True,
                            rangeslider_visible=False)






        fig.update_layout(width=1770,
                            height=700,
                            margin={"r":0, "l":85, "b":150},
                            font_family="sans serif",
                            font_color='#000000',
                            legend=dict(yanchor="top",
                                        orientation="h",
                                        y=1.25,
                                        xanchor="left",
                                        x=0.3,
                                        bgcolor="#ffffff",
                                        bordercolor="#000000",
                                        borderwidth=1,
                                        font={"color":"#000000", "family":"sans serif", "size":18}
                                        ),
                            paper_bgcolor="#d7dde0",
                            plot_bgcolor="#ffffff"
                            )
        fig.update_layout(xaxis=dict(rangeslider=dict(visible=True)))
        st.plotly_chart(fig, use_contrainer_width=True, theme=None)
