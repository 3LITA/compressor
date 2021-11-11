import pathlib
import sys

from compression import compressors


def error_message() -> None:
    print(
        "The command interface is \n"
        "./decompress <input-filepath> <output-filepath>\n"
        "<input-filepath> has to exist"
    )


def decompress() -> None:
    if len(sys.argv) != 3:
        return error_message()
    input_fp, output_fp = sys.argv[1:]
    input_filepath = pathlib.Path(input_fp)
    if not input_filepath.exists():
        return error_message()
    output_filepath = pathlib.Path(output_fp)
    Decompressor = compressors.DECOMPRESSORS['bwt']
    decompressor = Decompressor(
        input_filepath=input_filepath, output_filepath=output_filepath
    )  # type: ignore
    decompressor.decompress()


if __name__ == '__main__':
    decompress()
