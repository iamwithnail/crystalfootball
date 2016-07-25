def open_file_and_retrieve_data(filename):
    import pandas as pd
    data = pd.read_csv(filename)
    return data

def convert_frame_dates(data_frame):
    import pandas as pd
    #converts string dates to dates and indexes df by Date
    #replaces old data frame
    data_frame['Date']= pd.to_datetime(data_frame['Date'], dayfirst=True)
    indexed = data_frame.set_index(['Date'])
    return indexed


def slice_by_date(frame, start, end):
    return frame.ix[start:end]

def team_averages_by_date(frame, to_date):
    #wrap this in a date procession.
    from datetime import datetime
    start = datetime(2015,8,8)
    mean_df = slice_by_date(frame, start, to_date)
    means_output = mean_df.groupby('HomeTeam')[['FTHG', 'FTAG', 'HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR']]
    means_output.append(mean_df['AwayTeam','FTR','HTR'])
    return means_output



def preprocess(df):
    from sklearn import preprocessing
    processed_df = df.copy()
    le = preprocessing.LabelEncoder()
    processed_df.FTR = le.fit_transform(processed_df.FTR)
    processed_df.HTR = le.fit_transform(processed_df.HTR)
    processed_df = processed_df.drop(['Referee',
                                      'B365H','B365D','B365A',
                                      'BWH','BWD','BWA',
                                      'IWH','IWD','IWA',
                                      'LBH','LBD','LBA',
                                      'PSH','PSD','PSA',
                                      'WHH','WHD','WHA',
                                      'VCH','VCD','VCA',
                                      'Bb1X2','BbMxH','BbAvH','BbMxD','BbAvD','BbMxA','BbAvA','BbOU',
                                      'BbMx>2.5','BbAv>2.5','BbMx<2.5','BbAv<2.5',
                                      'BbAH','BbAHh','BbMxAHH','BbAvAHH','BbMxAHA','BbAvAHA'],
                                     axis=1)
    return processed_df

