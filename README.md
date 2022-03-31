# Cookiecutter Machine Learning

Cookiecutter template for reproducible machine learning projects. The template
is for personal use.

*Inspired
by [drivendata/cookiecutter-data-science](https://github.com/drivendata/cookiecutter-data-science)*
.

## Usage

1. Install `cookiecutter` via pip.

```bash
pip install cookiecutter
```

2. Create new project by the following command

```bash
cookiecutter gh:garywei944/cookiecutter-machine-learning
```

## Directory structure

The directory structure is developed
from [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/)
.

```text
.
├── checkpoints                             >> saved model checkpoints
├── cli.py                                  >> command line interface
├── config.py                               >> load configurations
├── configs                                 >> experiments configurations
│   ├── baseline.yml
│   ├── latest.yml
│   └── toy.yml
├── data                                    >> data directory
│   ├── external                            >> external data
│   ├── interim                             >> intermedia, temporary data
│   ├── processed                           >> generated, final dataset
│   └── raw                                 >> immutable raw data
├── environment.yml                         >> python package dependencies
├── LICENSE                                 >> LICENSE
├── Makefile                                >> some useful commands
├── notebooks                               >> jupyter notebooks that perform experiments
│   └── template.ipynb
├── README.md                               >> README
├── references                              >> explanatory notebooks and docs
├── reports                                 >> result figures for report publication
│   └── figures
├── sandbox                                 >> sandbox folder for workspace
├── scripts                                 >> standalone scripts
├── set_up_notebook.sh                      >> setup remote jupyter port on UMass gypsum
└── src                                     >> pipeline source code
    ├── data                                >> make dataset from raw data
    │   ├── __init__.py
    │   └── make_dataset.py
    ├── features                            >> make features from processed data
    │   ├── build_features.py
    │   └── __init__.py
    ├── __init__.py
    ├── models                              >> model implementation
    │   ├── __init__.py
    │   ├── predict_model.py
    │   └── train_model.py
    └── visualization                       >> result visualization
        ├── __init__.py
        └── visualize.py
```
