# Processing Specs Data

Python Scripts under this dicrectory is used to process specs data into a multilingual specs dataset.

## How to Use

To aggregrate dataset for each macro type in each language, execute
```
python data_processing.py --type Number --do_merge 1
```
by specifying which type of specs you want to process with token `--type`, <br>
and specifying whether you want to merge the processed datasets with token `--do_merge`.
The results will be in EdiLU json format. Each micro dataset will be in the directory *`type\language\processed_data.json`*, and the merged\macro dataset will be *`type\merged_data.json`*.


To convert json files into conll files, execute
```
python data_conversion.py --type Number
```
by specifying which type of specs you want to process with token `--type`. 
The results will be `processed_data.conll` in conll format, under the corresponding directory.

Meanwhile, logs will be `log.log` under your current directory.

## Off-the-Shelf Scripts

You can easily process all data by running the below commands

```

python data_processing.py --type Choice --do_merge 1

python data_processing.py --type DateTime --do_merge 1

python data_processing.py --type Number --do_merge 1

python data_processing.py --type NumberWithUnit --do_merge 1

python data_processing.py --type Sequence --do_merge 1

```