# {{cookiecutter.project_name}}

{{cookiecutter.description}}

## Documentations

## Dataset

## Notebooks

- Notebooks for experiments are located under `notebooks`.
- Notebooks for visualization and presentation are located under `references`.

## Conda / Mamba Environment Setup

*[`mamba`](https://github.com/mamba-org/mamba) is a reimplementation of
the `conda` package manager in C++. I strongly recommend to use `mamba` instead
of `conda` to install the environment. `conda` mostly would stuck at **Solving
environment**, as it tries to do an SAT problem, which is NP-Complete, to solve
the dependency problem.*

### Bare Shell Command

```shell
# To firstly install the environment
mamba env create -f environment.yml
# To update the environment after updating environment.yml
# BEST PRACTICE, RECOMMENDED when updating a conda environment
mamba env update -f environment.yml --prune
```

### Using `Makefile`

```shell
# To firstly install the environment
make install
# To update the environment after updating environment.yml
make update
# To show help message
make
```

## Sandbox

The `sandbox` folder is a favor of my projects. It is also a good practice in
teamwork. Everyone works with the project should have a sub-folder named by
their id under it, and any scripts, doc, or data that are temporary should be
placed there.

---

Project based on
the [cookiecutter data science project template](https://drivendata.github.io/cookiecutter-data-science/)
. #cookiecutterdatascience
