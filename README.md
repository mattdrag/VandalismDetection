# VandalismDetection

CS145 Group Project. Group members: Matt Dragotto, Andy Kuang, Shuhao Sun

## Instructions for running the code:

## Depedencies:
#### For data_to_csv.py: 
- "codecs": was needed for dealing with unicode characters, 
- "lxml": was used for parsing the xml into trees
- "tqdm": was used for progress bars in the terminal window

#### For csv_to_tensor.py:
- Python version 3.5
- "pandas" was used for metrics about the data

#### For ski-train-v1.py:
- Python version X.X
- [list dependencies]

## Running the data:
1. Aquire the training, validation, and test data from http://www.wsdm-cup-2017.org/vandalism-detection.html

2. Extract it into their respective directories, named: Train, Validation, and Test

3. Run data_to_csv.py. This will generate the csv files needed for training and testing the models
> py data_to_csv.py

4. If you are using Tensorflow, first run remove_header_columns.py, because the data needs to be formatted differently. Then run csv_to_tensor.py
> py remove_headers.py
> py -3.5 csv_to_tensor.py



