import pathlib

import click

from . import compressors


@click.group(name='compressor')
@click.argument('input-filepath', type=click.Path(exists=True))
@click.argument('output-filepath', type=click.Path())
@click.option('--algorithm', '-a', type=str, default='huffman')
@click.pass_context
def main(
    context: click.Context,
    input_filepath: pathlib.Path,
    output_filepath: pathlib.Path,
    algorithm: str,
) -> None:
    context.obj = dict(
        input_filepath=input_filepath,
        output_filepath=output_filepath,
        algorithm=algorithm,
    )


@main.command()
@click.pass_context
def compress(context: click.Context) -> None:
    algorithm = context.obj['algorithm']
    input_filepath = context.obj['input_filepath']
    output_filepath = context.obj['output_filepath']

    Compressor = compressors.COMPRESSORS[algorithm]
    compressor = Compressor(
        input_filepath=input_filepath, output_filepath=output_filepath
    )
    compressor.compress()


@main.command()
@click.pass_context
def decompress(context: click.Context) -> None:
    algorithm = context.obj['algorithm']
    input_filepath = context.obj['input_filepath']
    output_filepath = context.obj['output_filepath']

    Decomressor = compressors.DECOMPRESSORS[algorithm]
    decompressor = Decomressor(
        input_filepath=input_filepath, output_filepath=output_filepath
    )
    decompressor.decompress()
