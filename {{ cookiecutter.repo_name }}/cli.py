import os
import click
from config import load_config

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(
    invoke_without_command=True,
    options_metavar='<options>',
    context_settings=CONTEXT_SETTINGS
)
@click.option(
    '-c', '--config-name',
    default='baseline',
    envvar="CONFIG",
    help='Config file at "./configs/<config>.yml", default is "baseline"',
    metavar='<config>'
)
@click.option('-C', '--collect-env', is_flag=True,
              help='Whether to print torch.utils.collect_env')
@click.option('-N', '--n-jobs', type=int, default=None,
              help='Number of CPU\'s to use')
@click.option('-s', '--seed', type=int, default=None,
              help='Seed to make experiments reproducible')
@click.option('-ng', '--no-gpu', is_flag=True,
              help='Don\'t use gpu for training')
@click.option('-b', '--batch-size', type=int, default=None,
              help='batch size of training and validation')
@click.pass_context
def cli(
        ctx: click.core.Context,
        config_name: str,
        collect_env: bool,
        n_jobs: int,
        seed: int,
        no_gpu: bool,
        batch_size: int
):
    """
    NoteAid-Annotation
    """

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
    else:
        ctx.ensure_object(dict)
        if no_gpu:
            os.environ['USE_CUDA'] = '0'
        config = load_config(
            config_name,
            collect_env=collect_env,
            n_jobs=n_jobs,
            seed=seed,
            batch_size=batch_size
        )
        ctx.obj['config'] = config
        ctx.obj['collect_env'] = collect_env


@cli.command('data')
@click.pass_context
def _data(ctx: click.core.Context):
    """
    Make datasets
    """
    from src.data.make_dataset import make_dataset

    make_dataset(ctx.obj['config'])


@cli.command('features')
@click.pass_context
def _features(ctx: click.core.Context):
    """
    Make features
    """
    from src.features.make_features import make_features

    make_features(ctx.obj['config'])


@cli.command('all')
@click.pass_context
def _all(ctx: click.core.Context):
    """
    Run data, features, and train
    """
    ctx.invoke(_data)
    ctx.invoke(_features)


@cli.command('env')
@click.pass_context
def _env(ctx: click.core.Context):
    """
    Test PyTorch and cuda env
    """
    if not ctx.obj['collect_env']:
        from torch.utils.collect_env import main as collect_env_

        collect_env_()


if __name__ == '__main__':
    cli(obj={})
