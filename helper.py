import numpy as np
def medal_tally(athlete):
    medal_1=athlete.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_1=medal_1.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_1['Total']=medal_1['Gold']+medal_1['Silver']+medal_1['Bronze']

    return medal_1

def country_year_list(athlete):
    years=athlete['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')
    country=np.unique(athlete['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')
    return years,country
    
def fetch_medal(athlete,year,country):
    medal_df=athlete.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag=False
    if year=='Overall' and country=='Overall':
        temp_df=medal_df
    elif year=='Overall' and country!='Overall':
        flag=True
        temp_df=medal_df[medal_df['region']==country]
    elif year!='Overall' and country=='Overall':
        temp_df=medal_df[medal_df['Year']==int(year)]
    else:
        temp_df=medal_df[(medal_df['region']==country) & (medal_df['Year']==int(year))]
    if flag==True:
        v=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year',ascending=True).reset_index()
    else:
        v=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
        
    v['Total']=v['Gold']+v['Silver']+v['Bronze']    
    return v

def data_with_time(athlete,col):
    nations_with_time=athlete.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_with_time.rename(columns={'Year':'Edition','count':col},inplace=True)  
    return nations_with_time  

def most_succesful(players,sport):
    temp_df=players.dropna(subset=['Medal'])
    if sport!='Overall':
        temp_df=temp_df[temp_df['Sport']==sport]
    x=temp_df['Name'].value_counts().reset_index().head(15).rename(columns={'Name':'index','count':'Name'})
    y=x.merge(players,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport','region']].drop_duplicates('index').rename(columns={'index':'Name','Name_x':'Medals'})
    return y
    
def yearwise_medal_tally(players,region):
    temp_df=players.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df=temp_df[temp_df['region']==region]
    final_df=new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_wise_heatmap(players,region):
    temp_df=players.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df=players[players['region']==region]
    pivot=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype(int)
    return pivot

def most_successful2(players,region):
    temp_df=players.dropna(subset=['Medal'])
    
    temp_df=temp_df[temp_df['region']==region]
    x=temp_df['Name'].value_counts().reset_index().head(15).rename(columns={'Name':'index','count':'Name'})
    y=x.merge(players,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport']].drop_duplicates('index').rename(columns={'index':'Name','Name_x':'Medals'})
    return y

def weight_v_height(athlete,sport):
    athlete_df=athlete.drop_duplicates(subset=['Name','region'])
    athlete_df['Medal'].fillna('No Medal',inplace=True)
    if sport!='Overall':
        temp_df=athlete_df[athlete_df['Sport']==sport]
        return temp_df
    else:
        return athlete_df
    
def men_women_overtime(athlete):
    athlete_df=athlete.drop_duplicates(subset=['Name','region'])
    men=athlete_df[athlete_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    women=athlete_df[athlete_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()
    final=men.merge(women,on='Year')
    final.rename(columns={'Name_x':'Men','Name_y':'Women'},inplace=True)
    return final

    
    


