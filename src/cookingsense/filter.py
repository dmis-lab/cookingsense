import spacy
from .filter_util import WordFilter
from .generic_filter import is_generic

from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)


class Pipeline:

    def __init__(self, config):
        self.config = config
        self.word_filter = WordFilter(config)
        self.nlp = spacy.load("en_core_web_sm")

        self.nli_checkpoint_path = (
            config.data_dir + "checkpoints/fine-tuned-bert-large/"
        )
        self.nli_tokenizer = AutoTokenizer.from_pretrained(self.nli_checkpoint_path)
        self.nli_model = AutoModelForSequenceClassification.from_pretrained(
            self.nli_checkpoint_path
        ).to("cuda")
        self.nli_model.to_bettertransformer()

    def get_spacy_sentences(self, documents):
        pipe = self.nlp.pipe(
            documents,
            n_process=self.config.spacy_n_process,
            batch_size=self.config.spacy_batch_size,
        )

        docs = [doc for doc in pipe]

        sentences = []
        for doc in docs:
            for sen in doc.sents:
                sentences.append(sen)
        return sentences

    def filter_generic(self, sentences):
        filtered_sens = []
        for sen in sentences:
            if is_generic(sen):
                filtered_sens.append(sen.text)
        return filtered_sens

    def filter_domain(self, sentences):
        filtered_sentences = []
        for sen in sentences:
            if self.word_filter.is_in_filter(sen):
                filtered_sentences.append(sen)
        return filtered_sentences

    def filter_semantic(self, sentences):
        inputs = self.nli_tokenizer(sentences, return_tensors="pt", padding=True).to(
            "cuda"
        )
        nli_result = self.nli_model(**inputs)

        # class candidates = ["1) Food Commonsense","2) Culinary Arts","3) Healthy diet & Nutrition","4) Culinary Culture","5) Food Management & Food Safety","6) Irrelevant or None of the aboves"]
        filtered_sentences = []
        for sen, c in zip(sentences, nli_result.logits.argmax(dim=1)):
            if c != 5:
                filtered_sentences.append(sen)
        return filtered_sentences

    def get_sentences(self, domain, datasets, start_idx=0, end_idx=1000):
        dataset = datasets[domain]
        if domain == "recipe":
            dataset = dataset["train"]
        elif domain == "paper":
            dataset = dataset["text"]

        documents = []
        for idx, doc in enumerate(dataset):
            if idx < start_idx:
                continue
            elif idx >= end_idx:
                break
            else:
                documents.append(doc)

        sentences = []
        if domain == "web":
            documents = [doc["text"] for doc in documents]
            print(f">> Num of documents : {len(documents)}")
            sentences = self.get_spacy_sentences(documents)
            print(f">> Num of sentences : {len(sentences)}")
            sentences = self.filter_generic(sentences)
            print(f">> Num of sentences (after generic filter): {len(sentences)}")
            sentences = self.filter_domain(sentences)
            print(f">> Num of sentences (after term filter) : {len(sentences)}")
            sentences = self.filter_semantic(sentences)
            print(f">> Num of sentences (after semantic filter) : {len(sentences)}")

        elif domain == "paper":
            sentences = documents

        elif domain == "recipe":
            for doc in documents:
                for instruction in doc["directions"]:
                    sentences.append(f"{doc['title']} {instruction}")
        return sentences
