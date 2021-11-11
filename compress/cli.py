import pathlib

import click

from . import compressors


@click.group(name='compressor')
def main() -> None:
    pass


@main.command()
@click.argument('input-filepath', type=click.Path(exists=True))
@click.argument('output-filepath', type=click.Path())
@click.option('--algorithm', '-a', type=str, default='bwt', show_default=True)
def compress(
    input_filepath: pathlib.Path, output_filepath: pathlib.Path, algorithm: str
) -> None:
    Compressor = compressors.COMPRESSORS[algorithm]
    compressor = Compressor(
        input_filepath=input_filepath, output_filepath=output_filepath
    )  # type: ignore
    compressor.compress()


@main.command()
@click.argument('input-filepath', type=click.Path(exists=True))
@click.argument('output-filepath', type=click.Path())
@click.option('--algorithm', '-a', type=str, default='bwt', show_default=True)
def decompress(
    input_filepath: pathlib.Path, output_filepath: pathlib.Path, algorithm: str
) -> None:
    Decomressor = compressors.DECOMPRESSORS[algorithm]
    decompressor = Decomressor(
        input_filepath=input_filepath, output_filepath=output_filepath
    )  # type: ignore
    decompressor.decompress()
