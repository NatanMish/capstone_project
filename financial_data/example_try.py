import pandas as pd

def work_on_part(df):
    df['TIME_M']=df['TIME_M'].apply(lambda x : x[:-(len(x)-x.rfind(':'))])
    print('sliced the time')
    df["DATETIME"] = df["DATE"].map(str).str.slice(0,10,1) + ' ' + df["TIME_M"].map(str)
    print('created the datetime column')
    df["DATETIME"]=pd.to_datetime(df["DATETIME"])
    print('converted to datetime')
    df.drop(['DATE','TIME_M'],1,inplace=True)
    agg_df=df.groupby(['DATETIME','SYM_ROOT']).sum()
    print('grouped by sum')
    mean_df=df[['DATETIME','SYM_ROOT','PRICE']].groupby(['DATETIME','SYM_ROOT']).mean()
    print('grouped by and averaged')
    agg_df=agg_df.merge(mean_df,on=['DATETIME','SYM_ROOT'],how='inner')
    print('merged the dfs')
    agg_df.drop('PRICE_x',1,inplace=True)
    agg_df.rename(columns={'PRICE_y': 'PRICE'}, inplace=True)
    agg_df.reset_index(level=[0,1], inplace=True)
    print('reseted the index')
    return agg_df
	
def do_it_all(file_name):
    df = pd.read_csv(file_name)
    print(f'length of {file_name}:{len(df)}')
    df.sort_values(by=['DATE','TIME_M'],inplace=True)
    length=len(df)
    results=[]
    results.append(work_on_part(df.loc[:(length//2)]))
    results.append(work_on_part(df.loc[(length//2):]))
    del df
    final=results[0].append(results[1])
    final_agg=final.groupby(['DATETIME','SYM_ROOT']).sum()
    print('grouped by sum')
    final_mean=final[['DATETIME','SYM_ROOT','PRICE']].groupby(['DATETIME','SYM_ROOT']).mean()
    del results
    del final
    print('grouped by and averaged')
    final_agg=final_agg.merge(final_mean,on=['DATETIME','SYM_ROOT'],how='inner')
    print('merged the dfs')
    final_agg.drop('PRICE_x',1,inplace=True)
    final_agg.rename(columns={'PRICE_y': 'PRICE'}, inplace=True)
    final_agg.reset_index(level=[0,1], inplace=True)
    print('reseted the index')
    final_agg.to_csv(f'{file_name[:-4]}_minute.csv')
    print('outputed')
	
do_it_all('SPYDIA_04052009-04052010.csv')