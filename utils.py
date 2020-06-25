import pandas as pd


target='Mustafa'

cols = [
    'Unnamed: 1',
    'Morning 9m-1pm EST',
    'Unnamed: 6',
    'Afternoon 2pm-6pm EST',
    'Unnamed: 8',
    '6pm-10pm EST\n10am-6pm EST',
    'Evening / Satursday',
    'Morning 9m-1pm EST.1', 'Unnamed: 14',
    'Afternoon 2pm-6pm EST.1', 'Unnamed: 16',
    'Morning 9m-1pm EST.2',
    'Unnamed: 20',
    'Afternoon 2pm-6pm EST.2',
    'Unnamed: 22',
    '6pm-10pm EST\n10am-6pm EST.1',
    'Evening / Satursday.1'
]

mapper = {
    'Unnamed: 1':'date',
    'Morning 9m-1pm EST':'G1/9:00-13:00 EST',
    'Unnamed: 6':'G1/A/teacher',
    'Afternoon 2pm-6pm EST':'G1/14:00-18:00 EST',
    'Unnamed: 8':'G1/B/teacher',
    '6pm-10pm EST\n10am-6pm EST':'G2/18:00-22:00 EST',
    'Evening / Satursday':'G2/A/teacher',
    'Morning 9m-1pm EST.1':'G3/09:00-13:00',
    'Unnamed: 14':'G3/A/teacher',
    'Afternoon 2pm-6pm EST.1':'G3/14:00-18:00 EST',
    'Unnamed: 16':'G3/B/teacher',
    'Morning 9m-1pm EST.2':'G4/09:00-13:00',
    'Unnamed: 20':'G4/A/teacher',
    'Afternoon 2pm-6pm EST.2':'G4/14:00-18:00',
    'Unnamed: 22':'G4/A/teacher',
    '6pm-10pm EST\n10am-6pm EST.1':'G5/18:00-22:00',
    'Evening / Satursday.1':'G5/A/teacher'
}

df = pd.read_csv('timetable.csv', skiprows=1)

df = df[cols]

df = df.rename(columns=mapper)

df['date'] = df['date'].str.strip()

df['date'] = pd.to_datetime(df['date'], format='%m/%d')
df['date'] = df['date'].apply(lambda dt: dt.replace(year=2020))

df = df.set_index('date')
ret = pd.DataFrame()
ret['date'] = df.index
ret = ret.set_index('date')

teacher_columns = [x for x in df.columns if 'teacher' in x]


def processor(r):

    for c in teacher_columns:

        if type(r[c]) is str and target in r[c]:

            return True
    
    return False


df = df[df.apply(processor, axis=1)]

a = [
    'G1/9:00-13:00 EST',
    'G3/09:00-13:00',
    'G4/09:00-13:00'
]

b = [
    'G1/14:00-18:00 EST',
    'G3/14:00-18:00 EST',
    'G4/14:00-18:00'
]

c = [
    'G2/18:00-22:00 EST',
    'G5/18:00-22:00'
]

df['days'] = pd.to_datetime(df.index)
df['days'] = df['days'].apply(lambda x: x.weekday())

ret['09:00-13:00 EST'] = ''
ret['14:00-18:00 EST'] = ''
ret['18:00-22:00 EST'] = ''
ret['10:00-18:00 EST'] = ''

cols = list(df.columns)

for idx in range(len(df.index)):

    for col in teacher_columns:

        column_idx = cols.index(col)

        if type(df.iloc[idx, column_idx]) is str and target in df.iloc[idx, column_idx]:

            if cols[column_idx-1] in a:
                ret.iloc[idx, 0] = df.iloc[idx, column_idx-1]
            
            if cols[column_idx-1] in b:
                ret.iloc[idx, 1] = df.iloc[idx, column_idx-1]
            
            if cols[column_idx-1] in c:
                if df.days.iloc[idx] == 5:
                    ret.iloc[idx, 3] = df.iloc[idx, column_idx-1]    
                else:
                    ret.iloc[idx, 2] = df.iloc[idx, column_idx-1]


ret.to_csv(target+'.csv')