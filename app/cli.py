import pathlib

import click

from . import compressors


@click.group(name='compressor')
def main() -> None:
    pass


@main.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.option('--algorithm', '-a', 'algorithm', type=str, default='huffman', help="Encoding algorithm")
def encode_file(filepath: pathlib.Path, algorithm: str) -> None:
    Encoder = compressors.ENCODERS[algorithm]
    encoder = Encoder.from_file(filepath)
    encoder.to_file(pathlib.Path(f'{filepath}.huff'))


@main.command()
@click.argument('source', type=str)
@click.option('--algorithm', '-a', 'algorithm', type=str, default='huffman', help="Encoding algorithm")
def encode_string(source: str, algorithm: str) -> None:
    Encoder = compressors.ENCODERS[algorithm]
    encoder = Encoder(text=source)
    print(encoder.encode())


@main.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.option(
    '--algorithm',
    '-a', 'algorithm', type=str, default='huffman', help="Encoding algorithm"
)
def decode_file(filepath: pathlib.Path, algorithm: str) -> None:
    Decoder = compressors.DECODERS[algorithm]
    decoder = Decoder.from_file(filepath)
    decoder.to_file(pathlib.Path(f'{filepath}.decoded'))


@main.command()
@click.argument('encoded', type=str)
@click.option('--algorithm', '-a', 'algorithm', type=str, default='huffman', help="Encoding algorithm")
def decode_string(encoded: str, algorithm: str) -> None:
    Decoder = compressors.DECODERS[algorithm]
    decoder = Decoder(text=encoded)
    print(decoder.decode())
