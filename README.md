# CookingSense
CookingSense: A Culinary Knowledgebase with Multidisciplinary Assertions (LREC-COLING 2024)
* [Paper](https://anthology.aclweb.org/2024.lrec-main.354/)

## Prerequisite 

* Install prerequisite
```
conda create -n cs python=3.10
conda activate cs
pip install -r requirements.txt
```

* Download [this file](https://www.dropbox.com/scl/fi/v2f7zaym12yusacvbddhy/datasets.zip?rlkey=36x1rcwmyup7qb85eadv2ooe9&st=ny3tdq9i&dl=0) and extract to './test/'.
* So, the directory should be 
```
./test/datasets
├── biomedical
├── checkpoints
│   └── fine-tuned-bert-large
├── commons
├── recipedb
└── saved
    └── paper
```

* Install this project as a package
```
pip install .
```

## Runfile
* This test file contains to get datasets for each domains
```
cd test
python run.py
```
