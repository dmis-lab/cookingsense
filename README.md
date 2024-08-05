# cookingsense
CookingSense: A Culinary Knowledgebase with Multidisciplinary Assertions (LREC-COLING 2024)

## Prerequisite 

* Install prerequisite
```
conda create -n cs python=3.10
conda activate cs
pip install -r requirements.txt
```

* Download [this file](https://www.dropbox.com/scl/fi/8d57dqcpkednslagtefly/datasets.zip?rlkey=b2yxheddrc997ljb52uzc3hze&st=15c4tyi7&dl=0) and extract to './test/'.
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
