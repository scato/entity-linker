# entity-linker

I'm going to build the best Entity Linker that I can.

## Running

To train the models and test against the test set, just run:

```bash
script/test
```

This script:

  - installs the necessary dependencies (using `script/bootstrap`)
  - prepares the different data sets (using `script/setup`)
  - calculates metrics for the test data set

The output could look like this:

```
$ script/test
Creating data sets...
Running test...
Calculating metrics for "test" data set...
Precision: 0.3333333333333333
Recall: 0.0007898894154818326
```

## Named Entity Linking (NEL)

Entity Linking is done in three steps:

  - extract mentions (NER)
  - generate candidates (NEC)
  - disambiguate candidates (NED)

## Named Entity Recognition (NER)

Named entity recognition is performed by [spaCy](https://spacy.io/).

The validation data set was used to tweak processing and parameters:

```
$ script/validate
Creating data sets...
Running manual validation...
Calculating metrics for "validation" data set...
Precision: 0.5291377012538027
Recall: 0.24313756550840926
```

## Named Entity Candidate generation (NEC)

TODO

## Named Entity Disambiguation (NED)

TODO

## Notes

```
(text)-[NER]->(mentions)-[NEC]->(candidates)-[NED]->(entities)

(text/labels)-[config]->(NER)
(labels/pages)-[ES]->(NEC)
(id/pages)-[PCA]->(NED)

(text/pages)-[validate/test]->(accuracy/recall)

script/bootstrap - install dependencies
script/setup     - prepare data sets and the NEC database
script/train     - train models
script/validate  - validate NER, NEC+NED, and NER+NEC+NED
script/test      - test NEL

script/build     - train models using ALL data?
```
