def load_data():
    import pandas as pd
    hn = pd.read_csv("hn_stories.csv")
    hn.columns=['submission_time','upvote','url','headline']
    hn=hn.dropna(axis=0,how='all')
    return hn

hn = load_data()
#print(hn.head())
