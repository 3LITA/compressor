from . import huffman


ENCODERS = {
    huffman.Encoder.algorithm: huffman.Encoder,
}

DECODERS = {
    huffman.Decoder.algorithm: huffman.Decoder,
}

__all__ = ['ENCODERS', 'DECODERS']
