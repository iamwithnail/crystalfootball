from pandas import Timedelta
previous_day = Timedelta('-1 days')
next_week = Timedelta('7 days')
import pandas as pd

def open_file_and_retrieve_data(filename):

    data = pd.read_csv(filename)
    return data

def convert_frame_dates(data_frame):
    import pandas as pd
    #converts string dates to dates and indexes df by Date
    #replaces old data frame
    data_frame['Date']= pd.to_datetime(data_frame['Date'], dayfirst=True)
    #indexed = data_frame.set_index(['Date'])
    return data_frame


def slice_by_date(frame, start, end):
    return frame.ix[start:end]

def team_averages_by_date(frame, to_date):
    #wrap this in a date procession.
    from datetime import datetime
    start = datetime(2015,8,8)
    from pandas import Timedelta
    previous_day = Timedelta('-1 days')
    next_week = Timedelta('7 days')
    current = slice_by_date(frame, start, to_date)
    mean_slice = slice_by_date(current, start, to_date+previous_day)
    means_output = mean_slice.groupby('HomeTeam')[['FTHG', 'FTAG', 'HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR']].mean()
    return means_output

def create_drop_list(df):
    main_drop_list = ['Referee',
                                      'B365H','B365D','B365A',
                                      'BWH','BWD','BWA',
                                      'IWH','IWD','IWA',
                                      'LBH','LBD','LBA',
                                      'PSH','PSD','PSA',
                                      'WHH','WHD','WHA',
                                      'VCH','VCD','VCA',
                                      'Bb1X2','BbMxH','BbAvH','BbMxD','BbAvD','BbMxA','BbAvA','BbOU',
                                      'BbMx>2.5','BbAv>2.5','BbMx<2.5','BbAv<2.5',
                                      'BbAH','BbAHh','BbMxAHH','BbAvAHH','BbMxAHA','BbAvAHA']
    output = [item for item in main_drop_list if item in df.column.values]
    return None

def preprocess(df):
    from sklearn import preprocessing
    processed_df = df.copy()
    le = preprocessing.LabelEncoder()
    # probably do this as 'did the home team win or not, so either 0 or 1 -
    # do a manual transformation after = Home win = 1, draw or home loss=0
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

def create_matchday(dataframe, to_date):
    from datetime import datetime
    start = datetime(2015,8,8)
    matches = slice_by_date(dataframe, start, to_date)
    mean_slice = slice_by_date(dataframe, to_date, to_date)
    return matches, mean_slice



def open_all_files():
    import pandas as pd
    base_address = "../static/data/2015-16/"
    master_list = []
    league_list = ['B1', 'D1', 'D2', 'E0', 'E1', 'E2', 'E3', 'F1', 'I1', 'SC0', 'SP1']
    for league in league_list:
        try:
            master_list.append(pd.read_csv(base_address + league + ".csv", error_bad_lines=False))
        except IOError:
            print "File " + base_address  + "/" + league + ".csv does not exist"

    print "Ending league teams"
    print master_list
    return master_list

def setup():
    data = pd.concat(open_all_files())
    processed = preprocess(convert_frame_dates(data))
    return processed

"""
from pandas import Timedelta
previous_day = Timedelta('-1 days')
next_week = Timedelta('7 days')

date_list = []
cut the frame to dates
for current object in df.iterrows():
    if current_object[0] not in date_list:
        do the average using this timestamp - 1 day (to exclude that day's figures)
        replace the relevant columns in the df
    else:
        pass #we've already done it

"""

def build_data(first_matchdate):
    from core.datamanager import create_matchday, setup
    processed = setup()
    processed.sort_index()
    from datetime import datetime
    start = datetime(2015,8,8)

    matchday = first_matchdate

    from pandas import Timedelta
    previous_day = Timedelta('-1 days')
    next_week = Timedelta('7 days')

    indexed = processed.set_index(['Date']).sort_index()
    season_end_date = indexed.index.max()
    frames_list = []
    while matchday < season_end_date:
        matches = processed[processed['Date'].isin([matchday])]
        means_slice = indexed.ix[start:matchday+previous_day]
        keylist = ['FTHG', 'FTAG', 'HTHG', 'HTAG', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']
        home_means_output = means_slice.groupby('HomeTeam')[keylist].mean()
        away_means_output = means_slice.groupby('AwayTeam')[keylist].mean()
        out = home_means_output[home_means_output.index.isin(matches['HomeTeam'])]
        matchcopy = matches.set_index('HomeTeam')
        matchcopy[keylist]=out[keylist]
        frames_list.append(matchcopy)
        matchday+=next_week
        print "Currently on:", matchday

    return frames_list


# J Richard's paste example of reindexing it http://pastebin.com/70vCsNHa

def process_for_ml(dataframe):
    from sklearn import datasets, svm, cross_validation, tree, preprocessing, metrics
    x = dataframe.drop(['FTR', 'HTR', 'Date','Div', 'AwayTeam'], axis=1).values
    y = dataframe['FTR'].values
    x_train, x_test, y_train, y_test = cross_validation.train_test_split(x, y, test_size=0.2)
    clf_dt = tree.DecisionTreeClassifier(max_depth=10)
    clf_dt.fit(x_train, y_train)
    clf_dt.score(x_test, y_test)
    return clf_dt.score(x_test, y_test)

def run_it():
    from datetime import datetime
    import pandas as pd
    start_date = datetime(2015, 9, 12)
    data = pd.concat(build_data(start_date)).sort_index()

    return data