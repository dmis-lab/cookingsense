from spacy.tokens import Span, Token
from typing import Union

"""
core function : is_generic

Input  List<DocBin>     : Sentences
Output List<Boolean>    : Boolean results whether this sentence is generic or not  
Usage  : df['generic'] = df['sen_span'].apply(is_generic)
"""



def get_first_word(sentence: Span) -> Union[None, Token]:
    """
    Returns the first word of a sentence, ignoring the heading spaces
    """
    if len(sentence) == 0:
        return None

    first_word = sentence[0]
    i = 0
    while first_word.is_space:
        if i >= len(sentence):
        # if i > len(sentence):
            return None

        try:
            first_word = sentence[i + 1]
        except BaseException as e:
            # print(e, '\t', sentence, '\t', i)
            return None
        i += 1
    return first_word


def get_doc_url(sentence: Span) -> str:
    """
    Returns the URL of the document containing the sentence, if it exists,
    otherwise returns an empty string
    """
    return sentence.doc.user_data.get("url", "")

_filter_config = {
    "is-short-enough": {
        "max_length": 150
    },
    "has-no-bad-first-word":{
        "words":[
            "this","that","these","those","he","she","her","his"
        ]
    },
    "all-propn-have-acceptable-ne-labels":{
        "excluded": []
    },
    "has-no-pronouns":{
        "words":[ "i", "me", "my", "we", "us", "our", "you", "your"]
    },
    "not-from-unreliable-source":{
        "domain_tails": ["tk"]
    }
}

filter = {
            "is-short-enough": (
                lambda s: len(s.text.strip()) <=
                          _filter_config["is-short-enough"]["max_length"]),
            "has-at-least-one-token": (lambda s: len(s) >= 1),
            "first-word-is-not-none": (
                lambda s: get_first_word(s) is not None and get_first_word(
                    s).text.strip() != ""),
            "starts-with-capital": (
                lambda s: get_first_word(s).text[0].isupper()),
            "ends-with-period": (lambda s: s.text.strip()[-1] == "."),
            "has-no-bad-first-word": (
                lambda s: get_first_word(s).lower_ not in
                          _filter_config["has-no-bad-first-word"][
                              "words"]),
            "first-word-is-not-verb": (
                lambda s: get_first_word(s).pos_ != "VERB"),
            "first-word-is-not-conjunction": (
                lambda s: get_first_word(s).pos_ not in {"CCONJ", "SCONJ"}),
            "noun-exists-before-root": (lambda s: any(
                t.pos_ in {"NOUN", "PROPN"} for t in s if t.i < s.root.i)),
            "has-no-digits": (lambda s: not any(t.isdigit() for t in s.text)),

            "all-propn-have-acceptable-ne-labels": (lambda s: all(
                e.label_ not in set(_filter_config[
                    "all-propn-have-acceptable-ne-labels"].get(
                    "excluded", [])) for e in s.ents)),

            "has-no-pronouns": (lambda s: not any((t.lower_ in set(
                _filter_config["has-no-pronouns"][
                    "words"])) and t.pos_ == "PRON" for t in s)),

            "root-has-nsubj-or-nsubjpass": (
                lambda s: any(
                    t.dep_ in {"nsubj", "nsubjpass"} for t in s.root.children)),

            "has-no-email": (lambda s: not any(t.like_email for t in s)),
            "scr.dot_dot_in_sentence": (lambda s: ".." not in s.text),
            "scr.www_in_sentence": (lambda s: "www" not in s.text),
            "scr.com_in_sentence": (lambda s: "com" not in s.text),
            "scr.http_in_sentence": (lambda s: "http" not in s.text),

            "scr.many_hyphens_in_sentence": (
                lambda s: s.text.count("-") < 2 and s.text.count("–") < 2),
            # these are two different hyphens

            "remove-non-verb-roots": (lambda s: s.root.pos_ in {"VERB", "AUX"}),
            "remove-first-word-roots": (
                lambda s: s.root.i != get_first_word(s).i),

            "remove-present-participle-roots": (lambda s: s.root.tag_ != "VBG"),
            "remove-past-tense-roots": (lambda s: s.root.tag_ != "VBD"),

            "not-from-unreliable-source": (
                lambda s: not any(f".{d}/" in get_doc_url(s) for d in
                                  _filter_config[
                                      "not-from-unreliable-source"][
                                      "domain_tails"])),
        }

def is_generic( s: Span) -> bool:
    if len(s) ==0:
        return None
    return not any((not func(s)) for func in filter.values())
