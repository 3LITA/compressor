from . import huffman


COMPRESSORS = {
    # burrows_wheeler.Encoder.algorithm: burrows_wheeler.Encoder,
    huffman.Compressor.algorithm: huffman.Compressor,
}

DECOMPRESSORS = {
    # burrows_wheeler.Decoder.algorithm: burrows_wheeler.Decoder,
    huffman.Decompressor.algorithm: huffman.Decompressor,
}

__all__ = ['COMPRESSORS', 'DECOMPRESSORS']
