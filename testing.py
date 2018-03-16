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

print(df.shape[0])

#REVISION_ID,IS_ANON,USER_NAME,USER_ID,USER_IP_1,USER_IP_2,USER_IP_3,USER_IP_4,REVISION_SESSION_ID,USER_COUNTRY_CODE,USER_CONTINENT_CODE,USER_TIME_ZONE,USER_REGION_CODE,USER_CITY_NAME,USER_COUNTY_NAME,REVISION_TAGS,ROLLBACK_REVERTED,UNDO_RESTORE_REVERTED