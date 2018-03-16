import codecs


with codecs.open('./Train/wdvc16_train.csv','r','utf8') as f:
    with codecs.open('./Train/wdvc16_train_no_header.csv','w','utf8') as f1:
        next(f) # skip header line
        for line in f:
            f1.write(line)

with codecs.open('./Validation/wdvc16_validation.csv','r','utf8') as f:
    with codecs.open('./Validation/wdvc16_validation_no_header.csv','w','utf8') as f1:
        next(f) # skip header line
        for line in f:
            f1.write(line)