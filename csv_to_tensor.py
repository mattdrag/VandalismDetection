"""Example code for TensorFlow Wide & Deep Tutorial using tf.estimator API , adapted for fun and for profit """
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import shutil
import sys

import tensorflow as tf
import pandas 

#[ 'REVISION_ID', 'IS_ANON', 'USER_NAME', 'USER_ID', 'USER_IP_1', 'USER_IP_2', 'USER_IP_3', 'USER_IP_4', ],REVISION_SESSION_ID,USER_COUNTRY_CODE,USER_CONTINENT_CODE,USER_TIME_ZONE,USER_REGION_CODE,USER_CITY_NAME,USER_COUNTY_NAME,REVISION_TAGS,ROLLBACK_REVERTED,UNDO_RESTORE_REVERTED

#features - 'rev_id', 'pg_title', 'user_name', 'user_id', 'user_ip',  'revision_session_id', 'user_country_code', 'user_continent_code', 'user_time_zone', 'user_region_code',
#			'user_city_name'
#label - rollback_reverted

_CSV_COLUMNS = [
    'rev_id', 'is_anon', 'user_name', 'user_id', 'user_ip_1', 'user_ip_2', 'user_ip_3', 'user_ip_4',
    'revision_session_id', 'user_country_code', 'user_continent_code', 'user_time_zone', 'user_region_code',
    'user_city_name', 'user_county_name', 'revision_tags', 'rollback_reverted',
    'undo_restore_reverted'
]

_CSV_COLUMN_DEFAULTS = [[''], [''], [''], [''], [''], [''], [''], [''], [''], [''],
                        [''], [''], [''], [''], [''], [''], [''], ['']]

parser = argparse.ArgumentParser()

parser.add_argument(
    '--model_dir', type=str, default='./tf_models',
    help='Base directory for the model.')

#Gachibass
parser.add_argument(
    '--model_type', type=str, default='wide',
    help="Valid model types: {'wide', 'deep', 'wide_deep'}.")

parser.add_argument(
    '--train_epochs', type=int, default=2, help='Number of training epochs.')

parser.add_argument(
    '--epochs_per_eval', type=int, default=2,
    help='The number of training epochs to run between evaluations.')

parser.add_argument(
    '--batch_size', type=int, default=40, help='Number of examples per batch.')

parser.add_argument(
    '--train_data', type=str, default='./Train/wdvc16_train_no_header.csv',
    help='Path to the training data.')

parser.add_argument(
    '--test_data', type=str, default='./Validation/wdvc16_validation_no_header.csv',
    help='Path to the test data.')


# Use pandas for useful information about csv file, such as how many rows and how many unique entries in a col
df = pandas.read_csv('./Train/wdvc16_train_no_header.csv', names=_CSV_COLUMNS )
df2 = pandas.read_csv('./Validation/wdvc16_validation_no_header.csv', names=_CSV_COLUMNS )


_NUM_EXAMPLES = {
    'train': df.shape[0],
    'validation': df2.shape[0],
}

#features -     'is_anon', 'user_id', 'user_ip_1', 'user_ip_2', 'user_ip_3', 'user_ip_4',
#     'user_country_code', 'user_continent_code', 'user_time_zone', 'user_region_code',
#    'user_city_name', 'user_county_name', 
def build_model_columns():
  """Builds a set of wide and deep feature columns."""
  # Continuous columns

  is_anon = tf.feature_column.categorical_column_with_vocabulary_list(
      'is_anon', ['T', 'F'])
  user_id = tf.feature_column.categorical_column_with_hash_bucket(
      'user_id', hash_bucket_size=len(df['user_id'].unique()))
  user_ip_1 = tf.feature_column.categorical_column_with_hash_bucket(
      'user_ip_1', hash_bucket_size=len(df['user_ip_1'].unique()))
  user_ip_2 = tf.feature_column.categorical_column_with_hash_bucket(
      'user_ip_2', hash_bucket_size=len(df['user_ip_2'].unique()))
  user_ip_3 = tf.feature_column.categorical_column_with_hash_bucket(
      'user_ip_3', hash_bucket_size=len(df['user_ip_3'].unique()))
  user_ip_4 = tf.feature_column.categorical_column_with_hash_bucket(
      'user_ip_4', hash_bucket_size=len(df['user_ip_4'].unique()))
  user_country_code = tf.feature_column.categorical_column_with_hash_bucket(
      'user_country_code', hash_bucket_size=len(df['user_country_code'].unique()))
  user_continent_code = tf.feature_column.categorical_column_with_hash_bucket(
      'user_continent_code', hash_bucket_size=len(df['user_continent_code'].unique()))
  user_time_zone = tf.feature_column.categorical_column_with_hash_bucket(
      'user_time_zone', hash_bucket_size=len(df['user_time_zone'].unique()))
  user_region_code = tf.feature_column.categorical_column_with_hash_bucket(
      'user_region_code', hash_bucket_size=len(df['user_region_code'].unique()))
  user_city_name = tf.feature_column.categorical_column_with_hash_bucket(
      'user_city_name', hash_bucket_size=len(df['user_city_name'].unique()))
  user_county_name = tf.feature_column.categorical_column_with_hash_bucket(
      'user_county_name', hash_bucket_size=len(df['user_county_name'].unique()))
  # Wide columns and deep columns.
  base_columns = [ is_anon, user_id, user_ip_1, user_ip_2, user_ip_3, user_country_code, user_continent_code, user_time_zone, user_region_code, user_city_name, user_county_name ]

  wide_columns = base_columns

  deep_columns = [
  ]

  return wide_columns, deep_columns

def build_estimator(model_dir, model_type):
  """Build an estimator appropriate for the given model type."""
  wide_columns, deep_columns = build_model_columns()
  hidden_units = [100, 75, 50, 25]

  # Create a tf.estimator.RunConfig to ensure the model is run on CPU, which
  # trains faster than GPU for this model.
  run_config = tf.estimator.RunConfig().replace(
      session_config=tf.ConfigProto(device_count={'GPU': 0}))

  if model_type == 'wide':
    return tf.estimator.LinearClassifier(
        model_dir=model_dir,
        feature_columns=wide_columns,
        config=run_config)
  elif model_type == 'deep':
    return tf.estimator.DNNClassifier(
        model_dir=model_dir,
        feature_columns=deep_columns,
        hidden_units=hidden_units,
        config=run_config)
  else:
    return tf.estimator.DNNLinearCombinedClassifier(
        model_dir=model_dir,
        linear_feature_columns=wide_columns,
        dnn_feature_columns=deep_columns,
        dnn_hidden_units=hidden_units,
        config=run_config)


def input_fn(data_file, num_epochs, shuffle, batch_size):
  """Generate an input function for the Estimator."""
  assert tf.gfile.Exists(data_file), (
      '%s not found. Please make sure you have either run data_download.py or '
      'set both arguments --train_data and --test_data.' % data_file)

  def parse_csv(value):
    print('Parsing', data_file)
    columns = tf.decode_csv(value, record_defaults=_CSV_COLUMN_DEFAULTS)
    features = dict(zip(_CSV_COLUMNS, columns))
    l1 = features.pop('undo_restore_reverted')
    labels = features.pop('rollback_reverted')
    return features, tf.equal(labels, 'T')

  # Extract lines from input files using the Dataset API.
  dataset = tf.data.TextLineDataset(data_file)

  if shuffle:
    dataset = dataset.shuffle(buffer_size=_NUM_EXAMPLES['train'])

  dataset = dataset.map(parse_csv, num_parallel_calls=5)

  # We call repeat after shuffling, rather than before, to prevent separate
  # epochs from blending together.
  dataset = dataset.repeat(num_epochs)
  dataset = dataset.batch(batch_size)
  return dataset

def main(unused_argv):
  # Clean up the model directory if present
  shutil.rmtree(FLAGS.model_dir, ignore_errors=True)
  model = build_estimator(FLAGS.model_dir, FLAGS.model_type)

  # Train and evaluate the model every `FLAGS.epochs_per_eval` epochs.
  for n in range(FLAGS.train_epochs // FLAGS.epochs_per_eval):
    model.train(input_fn=lambda: input_fn(
        FLAGS.train_data, FLAGS.epochs_per_eval, True, FLAGS.batch_size))

    results = model.evaluate(input_fn=lambda: input_fn(
        FLAGS.test_data, 1, False, FLAGS.batch_size))

    # Display evaluation metrics
    print('Results at epoch', (n + 1) * FLAGS.epochs_per_eval)
    print('-' * 60)

    for key in sorted(results):
      print('%s: %s' % (key, results[key]))


if __name__ == '__main__':
  tf.logging.set_verbosity(tf.logging.INFO)
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
