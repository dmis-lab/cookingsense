import CookingSense as cs

class config:
    data_streaming = True
    data_dir = './datasets/'
    spacy_n_process = 2
    spacy_batch_size = 4

datasets = cs.load_datasets(config)

pipeline = cs.Pipeline(config)
web_sens = pipeline.get_sentences('web', datasets)
recipe_sens = pipeline.get_sentences('recipe', datasets)
paper_sens = pipeline.get_sentences('paper', datasets)

print('>> web sentences')
print(web_sens[:5])

print('>> recipe sentences')
print(recipe_sens[:5])

print('>> paper_sentences')
print(paper_sens[:5])
