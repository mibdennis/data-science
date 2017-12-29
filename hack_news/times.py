import read
from dateutil.parser import parse
data = read.load_data()

def time_ext(t):
    dt_obj = parse(t)
    return dt_obj.month

h_series = data.submission_time.apply(time_ext)
print(h_series.value_counts())
