from . import burrows_wheeler, huffman


ENCODERS = {
    burrows_wheeler.Encoder.algorithm: burrows_wheeler.Encoder,
    huffman.Encoder.algorithm: huffman.Encoder,
}

DECODERS = {
    burrows_wheeler.Decoder.algorithm: burrows_wheeler.Decoder,
    huffman.Decoder.algorithm: huffman.Decoder,
}

__all__ = ['ENCODERS', 'DECODERS']
