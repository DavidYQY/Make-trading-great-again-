# Make-trading-great-again-
repository for the Harvard cs109 project (2019 Fall)

## Directory Structure

```
preprocess/
	preprocess.py
	twokenize.py
	CleaningSPXData.ipynb
lstm/
	const.py
	dataset.py
	model.py
	train.py
	utils.py
baseline_model.ipynb
baseline_regression.ipynb
exploratory_data_analysis.ipynb
Feature Importance.ipynb
sentenment-analysis.ipynb
```

- ```preprocess.py``` (with twokenize.py imported): preprocess trump data from trumptwitterarchive.txt to processed_trumptwitterarchive.txt
- ```CleaningSPXData.ipynb```: clean SNP data and do the eda for the SNP data. 
- ```lstm folder```: codes to run lstm. To run it:
```python
python -m lstm.train
```
- ```baseline_model.ipynb```: notebook about the baseline models work.
- ```baseline_regression```: notebook about the regression work
- ``exploratory_data_analysis.ipynb```: notebook about the eda work
- ```Feature Importance```: notebook about the feature importance
- ```sentenment-analysis.ipynb```: notebook about the sentiment analysis (concluded in the eda section on the website)

Our website: 