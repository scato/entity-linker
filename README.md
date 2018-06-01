# entity-linker

I'm going to build the best Entity Linker that I can.

## TODO

  - split data in a training set, a validation set and a test set
  - write train and test scripts
  - write more TODOs

## The Plan

I want to build an entity linker. I am not going to build a Named Entity
Recognizer (NER). I want to use SpaCy for that. I do, however, need to build a
Named Entity Disambiguator (NED).

I can use SpaCy as a NER, but I discovered that the tokenizer needs to be
fine-tuned to work properly. (Specifically, it turned "Koning Willem-Alexander"
into two mentions: "Koning Willem" and "Alexander".) I was thinking, if I use
Wikipedia articles (and the page links they contain), then I have a ground truth
for mentions. It's not an accurate one, but it's good enough for evaluating the
tokenizer settings.

Now I would love to be able to use Wikipedia articles as a training set for my
NED, but there are some problems with the page links. First, most of them are
actually not named entities (so not people, organizations, etc.). Second, an
entity is only linked to once. (Consecutive mentions of the same entities are
plain text).

What I want to try instead is to create a universal entity disambiguator. For
each article, I have a list of page links (both the mention - or label - and
the page). I can use these lists to create two other lists:
  - a list of label/page pairs
  - a graph containing all page links
  - a collection of input/output data, input being mentions (labels) and output
    being entities (pages)

I can use the label/page pairs to create entity candidates. I can use the page
link graph to create an embedding for entities. I can validate the disambiguator
using the input/output data.
