
from datasets import load_dataset, Dataset
import pathlib
import os
import pandas as pd

__domains__ = ["web", "paper", "recipe"]

def load_raw_dataset(domain, config):
    if domain == "web":
        web_raw_dataset = load_dataset("allenai/c4", "en", streaming=config.data_streaming)['train']
        web_raw_dataset = web_raw_dataset.remove_columns(['timestamp', 'url'])
        return web_raw_dataset
    elif domain == "paper":
        _PAPER_PATH_ = os.path.join(config.data_dir, 'saved','paper', 'raw.csv')
        paper_df = pd.read_csv(_PAPER_PATH_)
        paper_dataset = Dataset.from_pandas(pd.DataFrame(paper_df['title'] + ' '  + paper_df['tldr'], columns=['text']))
        return paper_dataset 
    elif domain == "recipe":
        recipe_raw_dataset = load_dataset("recipe_nlg", data_dir=config.data_dir, streaming=config.data_streaming)
        return recipe_raw_dataset 

def load_datasets(config):
    return {
        k: load_raw_dataset(k, config) for k in __domains__
    }



