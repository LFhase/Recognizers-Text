# Data Processing for Specs

Python Scripts under this dicrectory is used to process specs data into a multilingual specs dataset.

To aggregrate dataset for each macro type in each language, execute
```
python data_processing.py --type Number
```
by specifying which type of specs you want to process with token `--type`. 
The results will be `processed_data.json` in EdiLU json format, under the corresponding directory.


To convert json files into conll files, execute
```
python data_conversion.py --type Number
```
by specifying which type of specs you want to process with token `--type`. 
The results will be `processed_data.conll` in conll format, under the corresponding directory.