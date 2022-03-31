# Load configurations from configs folder
# Created and maintained by garywei944 (garywei944@gmail.com)

import numpy as np
import torch
# import tensorflow as tf

import os
import sys
import logging
from dotenv import find_dotenv, load_dotenv
from ruamel.yaml import YAML
from multiprocessing import cpu_count
import json
from pathlib import Path
import random
from numpy.random import Generator

# Global Variables
PROJECT_DIR = str(Path(__file__).resolve().parents[0])

__SEED = None

# Configure logger
log_fmt = "%(asctime)s - %(levelname)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_fmt, stream=sys.stderr)
logger = logging.getLogger(__name__)

# find .env automagically by walking up directories until it's found, then
# load up the .env entries as environment variables
load_dotenv(find_dotenv())

yaml = YAML(typ='safe')


def salting(salt: int = 0, seed: int = __SEED) -> Generator:
    """
    Reset the random seed of python, numpy, and torch for each subprocess, and
    return a numpy default RNG object
    This is a workaround for RNG states being badly forked across subprocesses.
    Referring to https://github.com/pytorch/pytorch/issues/5059, numpy doesn't
    properly handle RNG states when fork subprocesses, which give rise to the
    issue that all subprocesses generate the same randomness pattern when
    processing data.
    torch.randint() would encounter similar issues.
    python builtin random class seems not to fork the seed state at all, so
    that the experiments won't be reproducible anyway.
    """
    if seed is None:
        return np.random.default_rng()
    else:
        __seed = seed + salt
        random.seed(__seed)
        np.random.seed(__seed)
        torch.manual_seed(__seed)
        # tf.random.set_seed(__seed)
        torch.backends.cudnn.deterministic = True

        return np.random.default_rng(__seed)


def is_using_mp(config: dict):
    return config.get('N_JOBS') > 1 and os.name != 'nt'


def init_mp(
        config: dict,
        progress_bar: bool = False
) -> None:
    """
    Initialize the parallel used by pandarallel
    """
    if not is_using_mp(config):
        return

    from pandarallel import pandarallel

    pandarallel.initialize(
        nb_workers=config.get('N_JOBS'),
        progress_bar=progress_bar,
        verbose=0
    )

    print(f'Initialized using {config.get("N_JOBS")} cpus')


def load_config(
        config_name: str = 'baseline',
        collect_env: bool = False,
        n_jobs: int = None,
        seed: int = None,
        batch_size: int = None,
        init_multiprocess: bool = True,
        progress_bar: bool = False
) -> dict:
    """
    1. Load .env environment variables
    2. Load the configuration file with config_name
    3. Print torch.utils.collect_env if collect_env is true
    4. Set up seeds for python, numpy and torch
    Return the config dict
    """
    if collect_env:
        from torch.utils.collect_env import main as collect_env_

        collect_env_()

    print(f'Loading config from configs/{config_name}.yml')

    with open('configs/baseline.yml', 'r') as f:
        config = yaml.load(f)
    if config_name != 'baseline':
        with open(f'configs/{config_name}.yml', 'r') as f:
            config.update(yaml.load(f))

    # Load USE_CUDA and N_JOBS from os.environ if they are not provided by
    # the config
    config['USE_CUDA'] = bool(int(os.environ.get(
        'USE_CUDA',
        config.get(
            'USE_CUDA',
            torch.cuda.is_available()
        )
    )))
    if config.get('USE_CUDA'):
        print('Use GPU(s) for training')
    else:
        print('Only use CPU(s) for training')

    config['N_JOBS'] = n_jobs if n_jobs is not None else int(os.environ.get(
        'N_JOBS',
        config.get(
            'N_JOBS',
            cpu_count()
        )
    ))
    if config.get('N_JOBS') == -1:
        config['N_JOBS'] = cpu_count()
    print(f'Using {config.get("N_JOBS")} CPU(s)')

    if init_multiprocess:
        init_mp(config, progress_bar=progress_bar)

    # Set random seeds
    global __SEED
    __SEED = seed if seed is not None else config.get('SEED')
    config['SEED'] = __SEED
    assert __SEED is None or (type(__SEED) is int and __SEED >= 0)

    salting(0, __SEED)

    # Set batch size
    if batch_size is not None:
        config['train_batch_size'] = batch_size
        config['eval_batch_size'] = batch_size

    print('Loaded config file')
    print('-' * 40)
    print(json.dumps(config, indent=4))
    print('-' * 40)

    return config
