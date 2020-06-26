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
    'Morning 8m-12pm EST',
    'Unnamed: 20',
    'Afternoon 1pm-5pm EST',
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
    'Morning 8m-12pm EST':'G4/08:00-12:00',
    'Unnamed: 20':'G4/A/teacher',
    'Afternoon 1pm-5pm EST':'G4/13:00-17:00',
    'Unnamed: 22':'G4/B/teacher',
    '6pm-10pm EST\n10am-6pm EST.1':'G5/18:00-22:00',
    'Evening / Satursday.1':'G5/A/teacher'
}

df = pd.read_csv('timetable.csv', skiprows=1)
print(df.columns)


df = df[cols]

df = df.rename(columns=mapper)

df['date'] = df['date'].str.strip()

df['date'] = pd.to_datetime(df['date'], format='%m/%d')
df['date'] = df['date'].apply(lambda dt: dt.replace(year=2020))

df.index = df.date
ret = pd.DataFrame()
ret['Date'] = df.date

teacher_columns = [x for x in df.columns if 'teacher' in x]

a = [
    'G1/9:00-13:00 EST',
    'G3/09:00-13:00'
]

b = [
    'G1/14:00-18:00 EST',
    'G3/14:00-18:00 EST'
]

c = [
    'G2/18:00-22:00 EST',
    'G5/18:00-22:00'
]

d = ['G4/08:00-12:00']
e = ['G4/13:00-17:00']

df['days'] = pd.to_datetime(df.index)
df['days'] = df['days'].apply(lambda x: x.weekday())
ret['Days'] = df.days


ret['TimeA'] = ''
ret['Morning'] = ''
ret['TimeB'] = ''
ret['Afternoon'] = ''
ret['TimeC'] = ''
ret['Evening'] = ''
ret['TimeD'] = ''
ret['Saturdays'] = ''


print('*'*10)
for cc in teacher_columns:

    results = df[cc]

    if 'Mustafa' not in results:
        print(cc)


cols = list(df.columns)

for idx in range(len(df.index)):

    for col in teacher_columns:

        column_idx = cols.index(col)

        if type(df.iloc[idx, column_idx]) is str and target == str(df.iloc[idx, column_idx]):

            # morning
            if cols[column_idx-1] in a:
                ret['TimeA'].iloc[idx] = '9:00-13:00 EST'
                ret.iloc[idx, 3] = df.iloc[idx, column_idx-1]
            
            # afternoon
            if cols[column_idx-1] in b:
                ret['TimeB'].iloc[idx] = '14:00-18:00 EST'
                ret.iloc[idx, 5] = df.iloc[idx, column_idx-1]
            
            if cols[column_idx-1] in c:
                if df.days.iloc[idx] == 5:
                    # saturdays
                    ret['TimeD'].iloc[idx] = '10:00-18:00 EST'
                    ret.iloc[idx, 9] = df.iloc[idx, column_idx-1]    
                else:
                    # evenings
                    ret['TimeC'].iloc[idx] = '18:00-22:00 EST'
                    ret.iloc[idx, 7] = df.iloc[idx, column_idx-1]
            
            if cols[column_idx-1] in d:
                ret['TimeA'].iloc[idx] = '08:00-12:00'
                ret.iloc[idx, 3] = df.iloc[idx, column_idx-1]
            
            if 'G4/13:00-17:00' == cols[column_idx-1]:
                print(cols[column_idx-1], cols[column_idx-1] in e)

            if cols[column_idx-1] in e:
                print(cols[column_idx-1], df.iloc[idx, column_idx-1])
                ret['TimeB'].iloc[idx] = '13:00-17:00'
                ret.iloc[idx, 5] = df.iloc[idx, column_idx-1]


days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
def namify(x):
    return days[x]
    
ret['Days'] = ret['Days'].apply(lambda x: namify(x))

ret.to_csv(target+'.csv', index=False)