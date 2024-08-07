import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


athlete=pd.read_csv('athlete_events.csv')
noc=pd.read_csv('noc_regions.csv')

df=preprocessor.preprocess(athlete,noc)

st.sidebar.header('Olympics Data Analyzer')
st.sidebar.image('sochi-2014-g8880ee89a_640-e1645698211307.jpg')
select=st.sidebar.radio('Select an option',('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis'))

if select=='Medal Tally':
    st.sidebar.header('Medal Tally')
    years,country=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox('Select Year',years)
    selected_country=st.sidebar.selectbox('Select Country',country)
    a=helper.fetch_medal(df,selected_year,selected_country)
    if selected_year=='Overall' and selected_country=='Overall':
        st.title('Medal Tally')
        st.table(a)
    elif selected_year!='Overall' and selected_country =='Overall':
        st.title('Medal tally of '+str(selected_year))
        st.table(a)
    elif selected_year=='Overall' and selected_country!='Overall':
        st.title('Medal tally of'+str(selected_country))
        st.table(a)
    else:
        st.title('Medal tally of '+str(selected_country)+' in '+str(selected_year))
        st.table(a)


elif select=='Overall Analysis':
    editions=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    athlete=df['Name'].unique().shape[0]
    host=df['region'].unique().shape[0]
    
    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    
    with col2:
        st.header('Cities')
        st.title(cities)
      
    with col3:
        st.header('Events')
        st.title(events)

    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Sport')
        st.title(sports)
    
    with col2:
        st.header('Athletes')
        st.title(athlete)
    
    with col3:
        st.header('Host')
        st.title(host)
    nations_with_time=helper.data_with_time(df,'region')
    fig=px.line(nations_with_time,x='Edition',y='region')
    st.title('Participating Nations over the years')
    st.plotly_chart(fig)
    
    events_with_time=helper.data_with_time(df,'Event')
    fig=px.line(events_with_time,x='Edition',y='Event')
    st.title('Events over the years')
    st.plotly_chart(fig)

    athletes_with_time=helper.data_with_time(df,'Name')
    fig=px.line(athletes_with_time,x='Edition',y='Name')
    st.title('No of athletes over the years')
    st.plotly_chart(fig)

    st.title('No of Events over time')
    fig=plt.figure(figsize=(20,20))
    x=df.drop_duplicates(['Year','Sport','Event'])
    y=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype(int),annot=True)
    st.pyplot(fig)

    st.title('Most Succesful Athletes')
    sports_list=df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,'Overall')
    selected_sports=st.selectbox('Select a Sport',sports_list)
    x=helper.most_succesful(df,selected_sports)
    st.table(x)
elif select=='Country-wise Analysis':
    selected=df['region'].dropna().unique().tolist()
    selected.sort()
    selected2=st.sidebar.selectbox('Select a Country',selected)

    new_select=helper.yearwise_medal_tally(df,selected2)
    fig=px.line(new_select,x='Year',y='Medal')
    st.title(selected2+' Medal Tally Over the Years')
    st.plotly_chart(fig)

    st.title(selected2+' excels in following sports')
    pt=helper.country_wise_heatmap(df,selected2)
    fig=plt.figure(figsize=(20,20))
    y=sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title(selected2+' top performing players')
    players=helper.most_successful2(df,selected2)
    st.table(players)

elif select=='Athlete-wise Analysis':
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    x1=athlete_df['Age'].dropna()
    x2=athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3=athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4=athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()
    fig=ff.create_distplot([x1,x2,x3,x4],['Overall age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_rug=False,show_hist=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    x=[]
    name=[]
    for i in famous_sports:
        temp_df=df[df['Sport']==i]
        x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
        name.append(i)
    fig=ff.create_distplot(x,name,show_rug=False,show_hist=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution of Age with Sports(Gold Medal) ')
    st.plotly_chart(fig)

    sports_list=df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,'Overall')

    sports=st.selectbox('Select a Sport',sports_list)
    plot=helper.weight_v_height(df,sports)
    fig=plt.figure(figsize=(10,10))
    sns.scatterplot(data=plot,x='Weight',y='Height',hue='Medal',style='Sex',s=100)
    st.pyplot(fig)

    st.title('Men Vs Women participation overtime')
    data=helper.men_women_overtime(df)
    fig=px.line(data,x='Year',y=['Men','Women'])
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)








else:
    st.dataframe(df)