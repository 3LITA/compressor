from . import burrows_wheeler, huffman


COMPRESSORS = {
    burrows_wheeler.ALGORITHM_NAME: burrows_wheeler.Compressor,
    huffman.ALGORITHM_NAME: huffman.Compressor,
}

DECOMPRESSORS = {
    burrows_wheeler.ALGORITHM_NAME: burrows_wheeler.Decompressor,
    huffman.ALGORITHM_NAME: huffman.Decompressor,
}

__all__ = ['COMPRESSORS', 'DECOMPRESSORS']
