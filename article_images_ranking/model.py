from CaptionGenerator import CaptionGenerator


class ImageCaptioning(object):

    def __init__(self, rnn_model, cnn_model, vocab):
        # TODO (SuJiaKuan):
        # 1. Do not hard-code the input arguments.
        # 2. Enable GPU.
        self._caption_generator = CaptionGenerator(
            rnn_model_place=rnn_model,
            cnn_model_place=cnn_model,
            dictonary_place=vocab,
            beamsize=3,
            depth_limit=50,
            gpu_id=-1,
            first_word='<sos>',
        )

    def generate(self, image_path):
        captions = self._caption_generator.generate(image_path)
        sentences = []
        for idx, caption in enumerate(captions):
            beam_size = idx + 1
            sentence = ' '.join(caption['sentence'][1:-1])
            sentences.append((beam_size, sentence))

        return sentences
