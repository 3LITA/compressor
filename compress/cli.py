import pathlib

import click

from . import coders


@click.group(name='compressor')
@click.argument('filepath', type=click.Path(exists=True))
@click.option('--algorithm', '-a', type=str, default='huffman')
@click.pass_context
def main(context: click.Context, filepath: pathlib.Path, algorithm: str) -> None:
    context.obj = dict(
        filepath=filepath,
        algorithm=algorithm,
    )


@main.command()
@click.pass_context
def encode(context: click.Context) -> None:
    algorithm = context.obj['algorithm']
    filepath = context.obj['filepath']

    Encoder = coders.ENCODERS[algorithm]
    encoder = Encoder.from_file(filepath)
    encoder.to_file(pathlib.Path(f'{filepath}.{algorithm}'))


@main.command()
@click.pass_context
def decode(context: click.Context) -> None:
    algorithm = context.obj['algorithm']
    filepath = context.obj['filepath']

    Decoder = coders.DECODERS[algorithm]
    decoder = Decoder.from_file(filepath)
    decoder.to_file(pathlib.Path(f'{filepath}.decoded'))
