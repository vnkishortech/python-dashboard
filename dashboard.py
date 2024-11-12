import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import os 
import warnings
import array

warnings.filterwarnings('ignore')

st.set_page_config(
    layout='wide',
    page_title="Dashboard!"
)

# st.markdown(
#     """
#     <style>
#         footer {display: none}
#         [data-testid="stHeader"] {display: none}
#     </style>
#     """, unsafe_allow_html= True
# )

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html= True)

title_col, emp_col, btc_col, eth_col, xmr_col, sol_col, xrp_col = st.columns([1,0.2,1,1,1,1,1])

with title_col:
    st.markdown('<p class="dashboard_title">Utilization <br> Dashboard', unsafe_allow_html=True)

with btc_col:
    with st.container():
        st.markdown(f'<p class="btc_text">Total Availability<br></p><p class="price_details">450</p>', unsafe_allow_html=True)

with eth_col:
    with st.container():
        st.markdown(f'<p class="eth_text">Total Allocations<br></p><p class="price_details">200</p>', unsafe_allow_html = True)

with xmr_col:
    with st.container():
         st.markdown(f'<p class="xmr_text">XMR / USDT<br></p><p class="price_details">250</p>', unsafe_allow_html = True)
       # st.markdown(f'<p calss="xmr_text">Avilability<br></p><p class="price_details">250</p>', unsafe_allow_html=True)

with sol_col:
    with st.container():
        st.markdown(f'<p class="sol_text">SOL / USDT<br></p><p class="price_details">0</p>', unsafe_allow_html = True)

with xrp_col:
    with st.container():
         st.markdown(f'<p class="xrp_text">XRP / USDT<br></p><p class="price_details">0</p>', unsafe_allow_html = True)



#tab1, tab2 =st.tabs(["weekly data","availability"])

fileupload_col1, fileupload_col2 = st.columns(2)

with fileupload_col1:
    # File uploader
    weekly_fl = st.file_uploader(":file_folder upload weekly data file", type=(["csv","txt","xlsx","xls"]),key="weekly_fl")
    if weekly_fl is not None:
        filename = weekly_fl.name
        st.write(filename)
        weekly_df=pd.read_csv(filename, encoding="ISO-8859-1")
    else:
        os.chdir(r"/Users/nanda/Desktop/python_streamlit")
        weekly_df=pd.read_csv("data/weeklydata.csv", encoding="ISO-8859-1")
with fileupload_col2:
     # File uploader
    avail_fl = st.file_uploader(":file_folder upload availability data file", type=(["csv","txt","xlsx","xls"]),key="avail_fl")
    if avail_fl is not None:
        filename = avail_fl.name
        st.write(filename)
        avail_df=pd.read_csv(filename, encoding="ISO-8859-1")
    else:
        os.chdir(r"/Users/nanda/Desktop/python_streamlit")
        avail_df=pd.read_csv("data/availability.csv", encoding="ISO-8859-1")


groupby_df = weekly_df.groupby(by="Resource", as_index= False).sum()


#Resource availability
st.subheader("Resource availability by weekly")
st.write(avail_df)

#df['total']=df.loc[:,1].sum(axis=1)

avail_total_df=avail_df.copy().set_index('Resource')
avail_total_df['TotalAvailability']= avail_total_df[avail_total_df.columns[1:]].sum(axis=1)
st.write(avail_total_df)

#Resource allocation
st.subheader("Resource allocation by weekly with project details")
st.write(groupby_df)

cols = [col for col in groupby_df.columns if col not in ['ProjectId', 'Project Description','Investment Manager']]
allocation_df = groupby_df[cols]

#st.write(groupby_df)
st.subheader("Resource allocation by weekly")
st.write(allocation_df)

allocation_total_df = allocation_df.copy().set_index('Resource')
allocation_total_df['TotalAllocation'] = allocation_total_df[allocation_total_df.columns[1:]].sum(axis=1)
st.write(allocation_total_df)


#Resource availability after alloation
availafter_df = avail_df.set_index('Resource').subtract(allocation_df.set_index('Resource'), fill_value=0) #.reset_index();
#availafter1_df=availafter_df.reset_index(drop=True)
#availafter_df = avail_df.sub(allocation_df)
st.subheader("Resource availability after allocation by weekly")
st.write(availafter_df)

availafter_total_df = availafter_df.copy()
availafter_total_df['TotalAvailabilityAfter'] = availafter_total_df[availafter_total_df.columns[1:]].sum(axis=1)
st.write(availafter_total_df)

st.write()

st.subheader("Resource total availability after allocation")
#result = pd.merge(avail_total_df.filter(['Resource','TotalAvailability']),allocation_total_df.filter(['Resource','TotalAllocation']), on ="Resource")
Totals_df = pd.merge(allocation_total_df.filter(['Resource','TotalAllocation']),availafter_total_df.filter(['Resource','TotalAvailabilityAfter']),on="Resource")
st.write(Totals_df)



#st.write(allocation_df[allocation_df.columns[~allocation_df.columns.isin(['Resource'])]])

#st.write(allocation_df.columns[1:])
# st.write(allocation_df.columns[~allocation_df.columns.isin(['Resource'])])

#st.write(allocation_df[allocation_df.columns[1:]])
#st.write(allocation_df[allocation_df.columns[:1]])


#pd.options.plotting.backend = 'plotly'

#st.plotly_chart(allocation_df.plot.barh(x=allocation_df.columns[:1]))

#len(allocation_df)
cols= st.columns(3)

#st.write(allocation_df.set_index('Resource'))

#st.write(Totals_df.columns[0:])

st.write(Totals_df.columns[0:].to_list())
#st.subheader("Bar")
counter = 0
for index,row in allocation_df.set_index('Resource').iterrows():
    # st.write(index)
    # st.write(row[allocation_df.columns[1:]].tolist())
    #st.write(allocation_df.columns[1:].tolist())
    #st.write(availafter_df.loc[index].tolist())
    #availbafter_list = availafter_df.loc[index].tolist()
    # st.write(allocation_df.columns[1:].tolist())
    # st.write(availafter_df.columns[0:].tolist())
    with cols[counter]:
        st.subheader(index)
        data =[
            go.Bar(name=index, x=allocation_df.columns[1:].tolist(), y=row[allocation_df.columns[1:]].tolist(),showlegend=False, marker_color='#0D98BA'),
            go.Bar(name=index, x=availafter_df.columns[0:].tolist(), y=availafter_df.loc[index].tolist(),showlegend=False,marker_color='#50C878')
            ]
        fig = go.Figure(data)
        fig.update_layout(barmode='stack')
        st.plotly_chart(fig,use_container_width=True, height=100,key=index)
        counter+=1
for index, row in Totals_df.iterrows():
    #st.subheader(index)
    #st.write(row[Totals_df.columns[0:]].tolist())
    labls=Totals_df.columns[0:].tolist()
    vals = row[Totals_df.columns[0:]].tolist()
    data=[
        go.Pie(labels=labls, values=vals, showlegend=False, hole=0.5, marker_colors=['#0D98BA','#50C878'] )
    ]
    fig = go.Figure(data)
    fig.update_traces(textinfo='value')
    st.plotly_chart(fig, use_container_width=True, height=100, key=index + "pie")





    #fig = px.bar(allocation_df, y=allocation_df.columns[1:], x="Resource", template="seaborn", barmode="group")
    # fig = go.Figure(data =[go.Bar(
    #     name='Allocation', x=allocation_df[allocation_df.columns[:1]], y=allocation_df[allocation_df.columns[1:]]) 
        
    # ])
    #fig.update_yaxes(range=[0,40])
    #fig.update_layout(barmode='stack')
    #st.plotly_chart(fig,use_container_width=True, height=200)
#with col2:
    # st.subheader("pie")
    # fig = px.pie(groupby_df, values=select_dates, names=select_dates, hole=0.5 )
    # st.plotly_chart(fig, use_container_width=True)


# data = [go.Bar(name=group, x=dfg['name'], y=dfg['%']) for group, dfg in df.groupby(by='week')]


# plot = px.Figure(data=[go.Bar(
#     name = 'Data 1',
#     x = x,
#     y = [100, 200, 500, 673]
#    ),
#                        go.Bar(
#     name = 'Data 2',
#     x = x,
#     y = [56, 123, 982, 213]
#    )
# ])





# Group by
select_groupby = st.sidebar.multiselect("select group by field", weekly_df.columns.unique())

if select_groupby:  
    groupby_df = weekly_df.groupby(by=select_groupby, as_index= False).sum()
else:
    groupby_df = weekly_df.copy()

# select resource
select_resources = st.sidebar.multiselect("select resources", weekly_df["Resource"].unique())

if select_resources:
    filtered_df=groupby_df[groupby_df["Resource"].isin(select_resources)]
else: 
    filtered_df= groupby_df.copy()

select_dates = st.sidebar.multiselect("select dates", weekly_df.columns[3:].unique() )

if not select_dates:
    select_dates = weekly_df.columns[4:].unique()




# #select_columns.append("Resource")

# selected_df = groupby_df.copy() #[select_columns]

# st.write(selected_df)


# new_df = selected_df.T.copy()
# st.write(new_df)
#df = new_df.set_index('col1').unstack().unstack()




#new_df.columns =['week']

# st.write(new_df)
# st.write(new_df.columns)


# col1, col2 = st.columns(2)

# with col1:
#     st.subheader("Bar")
#     fig = px.bar(groupby_df, y=select_dates, x="Resource", template="seaborn", barmode="group")
#     fig.update_yaxes(range=[0,40])
#     st.plotly_chart(fig,use_container_width=True, height=200)
# with col2:
#     st.subheader("pie")
#     fig = px.pie(groupby_df, values=select_dates, names=select_dates, hole=0.5 )
#     st.plotly_chart(fig, use_container_width=True)