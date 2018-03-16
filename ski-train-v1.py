"""
Page Feature.
	from revision: TITLE
User Features:
	from revision: REVISION_ID,TIME,REVISION_PARENT_ID,USER_NAME+USER_ID,
		IP_ADDRESS, COMMENT, JSON_CONTENT
	from metafile: REVISION_SESSION_ID,COUNTRY,CONTINENT,TIME_ZONE,REGION,
		CITY_NAME, COUNTY_NAME,REVISION_TAGS,ROLLBACK_REVERTED,
		UNDO_RESTORE_REVERTED
"""

"""
Features Used:
	TITLE,TIME,USER_NAME,USER_ID,IP_ADDRESS
	REVISION_SESSION_ID,COUNTRY,CONTINENT,TIME_ZONE,REGION,
	CITY_NAME, COUNTY_NAME
"""
import pandas as pd
import numpy as np
from time import time
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.svm import LinearSVC
import sklearn.metrics as sk_metric

#reading the data
df_train = pd.read_csv('./Train/wdvc16_train.csv', dtype={'REVISION_ID': object, \
	'PAGE_TITLE': object, 'USER_NAME': object, 'USER_ID': object, \
	'USER_IP': object, 'REVISION_SESSION_ID': object, 'USER_COUNTRY_CODE': object, \
	'USER_CONTINENT_CODE': object, 'USER_TIME_ZONE': object, 'USER_REGION_CODE': object, \
	'USER_CITY_NAME': object, 'USER_COUNTY_NAME': object, })
df_validation = pd.read_csv('./Validation/wdvc16_validation.csv', dtype={'REVISION_ID': object, \
	'PAGE_TITLE': object, 'USER_NAME': object, 'USER_ID': object, \
	'USER_IP': object, 'REVISION_SESSION_ID': object, 'USER_COUNTRY_CODE': object, \
	'USER_CONTINENT_CODE': object, 'USER_TIME_ZONE': object, 'USER_REGION_CODE': object, \
	'USER_CITY_NAME': object, 'USER_COUNTY_NAME': object, })
#remove NaN in datatrame
df_train = df_train.fillna('')
df_validation = df_validation.fillna('')


#processing raw features to text strings

#processing page titles
train_data =  'page_tile=' + df_train.PAGE_TITLE + ' '
#processing username and userid
df_train.USER_NAME = df_train.USER_NAME.replace([''], 'anonymous')
df_train['USER'] = 'user=' + df_train.USER_NAME + '_' + df_train.USER_ID
train_data += df_train.USER + ' '
#processing user ip address
#change ip to a string with ip features
def create_ip_string(raw_ip):
	ip_string = ''
	if raw_ip != '':
		ip_list = raw_ip.split('.')
		partial_ip_string = ''
		for ip in ip_list :
			partial_ip_string += ip + '_'
			ip_string += partial_ip_string + ' '
	return ip_string
#apply ip processing to ip addresses
df_train.USER_IP = df_train.USER_IP.apply(create_ip_string)
train_data += df_train.USER_IP
#processing left features
train_data += 'revision_id=' + df_train.REVISION_SESSION_ID + ' '\
 + 'country_code=' + df_train.USER_COUNTRY_CODE + ' '\
 + 'continent_code=' + df_train.USER_CONTINENT_CODE + ' '\
 + 'region_code=' + df_train.USER_REGION_CODE + ' '\
 + 'city_name=' + df_train.USER_CITY_NAME + ' '\
 + 'county_name=' + df_train.USER_COUNTY_NAME

#processing page titles
validation_data =  'page_tile=' + df_validation.PAGE_TITLE + ' '
#processing username and userid
df_validation.USER_NAME = df_validation.USER_NAME.replace([''], 'anonymous')
df_validation['USER'] = 'user=' + df_validation.USER_NAME + '_' + df_validation.USER_ID
validation_data += df_validation.USER + ' '
#processing user ip address
df_validation.USER_IP = df_validation.USER_IP.apply(create_ip_string)
validation_data += df_validation.USER_IP
#processing left features
validation_data += 'revision_id=' + df_validation.REVISION_SESSION_ID + ' '\
 + 'country_code=' + df_validation.USER_COUNTRY_CODE + ' '\
 + 'continent_code=' + df_validation.USER_CONTINENT_CODE + ' '\
 + 'region_code=' + df_validation.USER_REGION_CODE + ' '\
 + 'city_name=' + df_validation.USER_CITY_NAME + ' '\
 + 'county_name=' + df_validation.USER_COUNTY_NAME


#feature data
vec = HashingVectorizer(token_pattern="\\S+",n_features=10000000, norm=None,\
	binary=True, dtype=np.uint16, lowercase=False)
X_train = vec.transform(train_data)
X_validation = vec.transform(validation_data)


#label data
df_train.ROLLBACK_REVERTED = df_train.ROLLBACK_REVERTED.replace(['F'],0)
df_train.ROLLBACK_REVERTED = df_train.ROLLBACK_REVERTED.replace(['T'],1)
y_train = df_train.ROLLBACK_REVERTED.values

df_validation.ROLLBACK_REVERTED = df_validation.ROLLBACK_REVERTED.replace(['F'],0)
df_validation.ROLLBACK_REVERTED = df_validation.ROLLBACK_REVERTED.replace(['T'],1)
y_validation = df_validation.ROLLBACK_REVERTED.values

t = time()
#train
clf = LinearSVC(dual=False)
clf.fit(X_train, y_train)

#get the score
y_score = clf.decision_function(X_validation)
y_predict = clf.predict(X_validation)
roc_score = sk_metric.roc_auc_score(y_validation, y_score)
acc_score = sk_metric.accuracy_score(y_validation, y_predict)
print ('Time used: %.2fs, ROC_AUC=%.6f, ACCURACY=%.6f' % (time() - t,roc_score,acc_score))













