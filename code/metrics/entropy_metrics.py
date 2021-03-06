import math


# http://www.cs.toronto.edu/~lcharlin/papers/vhred_aaai17.pdf
class EntropyMetrics():
  def __init__(self, vocab, distro):
    '''
    Params:
      :vocab: Vocabulary dictionary.
      :ditro: Train distribution.
    '''
    self.vocab = vocab
    self.distro = distro

    self.metrics = {'per-unigram-entropy': [],
                    'per-bigram-entropy': [],
                    'utterance-unigram-entropy': [],
                    'utterance-bigram-entropy': []}

  # Update metrics for one example.
  def update_metrics(self, resp_words, gt_words, source_words):
    '''
    Params:
      :resp_words: Response word list.
      :gt_words: Ground truth word list.
      :source_words: Source word list.
    '''
    uni_entropy = []
    bi_entropy = []
    word_count = len(resp_words)
    for i, word in enumerate(resp_words):
      # Calculate unigram entropy.
      word = word if self.vocab.get(word) else '<unk>'
      probability = self.distro['uni'].get(word)
      if probability:
        uni_entropy.append(math.log(probability, 2))

      # Calculate bigram entropy.
      if i < word_count - 1:
        w = resp_words[i + 1] if self.vocab.get(resp_words[i + 1]) else '<unk>'
        probability = self.distro['bi'].get((word, w))
        if probability:
          bi_entropy.append(math.log(probability, 2))

    # Check if lists are empty.
    if uni_entropy:
      entropy = -sum(uni_entropy)
      self.metrics['per-unigram-entropy'].append(entropy / len(uni_entropy))
      self.metrics['utterance-unigram-entropy'].append(entropy)
    if bi_entropy:
      entropy = -sum(bi_entropy)
      self.metrics['per-bigram-entropy'].append(entropy / len(bi_entropy))
      self.metrics['utterance-bigram-entropy'].append(entropy)
