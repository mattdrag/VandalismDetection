import pandas
from glob import glob

_CSV_COLUMNS = [
    'rev_id', 'is_anon', 'user_name', 'user_id', 'user_ip_1', 'user_ip_2', 'user_ip_3', 'user_ip_4',
    'revision_session_id', 'user_country_code', 'user_continent_code', 'user_time_zone', 'user_region_code',
    'user_city_name', 'user_county_name', 'revision_tags', 'rollback_reverted',
    'undo_restore_reverted'
]

df = pandas.read_csv('./Train/wdvc16_train.csv', names=_CSV_COLUMNS )

for column in _CSV_COLUMNS:
	print(len(df[column].unique()))
