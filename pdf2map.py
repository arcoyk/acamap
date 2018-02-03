import os
import numpy as np
import random
import logging
from subprocess import call
from gensim.models.doc2vec import LabeledSentence
from gensim import models
from sklearn.decomposition import PCA

# Process PDF to metadata hash
# data = [
# {
#   'pdf': 'A Semantic Implication for HCI',
#   'doc': 'This paper present an implication...',
#   'tag': ['william@acm.org', 'CHI2016'],
#   'vec': [0.23, 0.54, 0.23 ... (doc2vec vector)],
#   'xyz': [0.33, 0.63, 0.23] (PCA of vec)
# }, ...]

ROOT_DIR = 'RKMTLAB'
TEXT_DIR = 'text'
MODEL_DIR = 'doc2vec.model'

def train(data):
  # require pdf, doc
  logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
  sentences = [LabeledSentence(words=d['doc'].split(' '), tags=[d['pdf']]) for d in data]
  model = models.Doc2Vec(sentences)
  for epoch in range(20):
    model.train(sentences, total_examples=model.corpus_count, epochs=model.iter)
    model.alpha -= (0.025 - 0.0001) / 19
    model.min_alpha = model.alpha
  model.save(MODEL_DIR)
  model = models.Doc2Vec.load(MODEL_DIR)
  return model

def all_files(r, d=list()):
  # Get all file paths under the root (r) recursively.
  if '.' in r:
    if '.pdf' in r:
      d += [r]
    return
  else:
    for f in os.listdir(r):
      all_files(r + '/' + f, d)
  return d

def read(path):
  with open(path) as f:
    return f.read().replace('\n', ' ')

def pdf2doc(pdf_path):
  pdf_name = pdf_path.split('/')[-1]
  text_path = '/'.join([TEXT_DIR, pdf_name + '.txt'])
  try:
    return read(text_path)
  except FileNotFoundError:
    call(['pdftotext', pdf_path, text_path])
    return read(text_path)

def get_tags(doc):
  rst = []
  for word in doc.split(' '):
    if '@' in word:
      rst.append(word)
  return rst

def append_doc(data):
  # require pdf
  for d in data:
    pdf = d['pdf']
    doc = pdf2doc(pdf)
    d['doc'] = doc
  return data

def append_tag(data):
  # require doc
  for d in data:
    doc = d['doc']
    tags = get_tags(doc)
    d['tag'] = tags
  return data

def pdf2vec(pdf, model):
  # [model.docvecs[tag] for tag in model.docvecs.doctags]
  return model.docvecs[pdf]

def valid_model(model, data):
  for d in data:
    pdf = d['pdf']
    tags = model.docvecs.doctags
    tags = tags.items()
    tags = [tag[0] for tag in tags]
    if not d in tags:
      return False
  return True

def get_model(data):
  model = models.Doc2Vec.load(MODEL_DIR)
  if not valid_model(model, data):
    print('Generating new model')
    model = train(data)
  return model

def append_vec(data):
  # require doc, pdf
  model = get_model(data)
  for d in data:
    pdf = d['pdf']
    vec = pdf2vec(pdf, model)
    d['vec'] = vec
  return data

def pca(vecs, n=3):
  pca = PCA(n_components=n)
  return pca.fit_transform(vecs)

def append_xyz(data):
  # require vec
  vecs = [d['vec'] for d in data]
  vecs = pca(vecs)
  for i, d in enumerate(data):
    d['xyz'] = vecs[i]
  return data

def pdfs2drops(data):
  data = append_doc(data)
  data = append_tag(data)
  data = append_vec(data)
  data = append_pca(data)
  return data

def get_pdfs(dr):
  pdfs = all_files(dr)
  data = []
  for pdf in pdfs:
    d = {'pdf':pdf}
    data.append(d)
  return data

def random_choice():
  i = random.choice(range(len(data)))
  return by_id(i)

def by_id(i):
  # for server
  d = data[i]
  rst = {}
  rst['text'] = d['pdf']
  rst['x'] = d['xyz'][0]
  rst['y'] = d['xyz'][1]
  rst['z'] = d['xyz'][2]
  return rst

data = get_pdfs(ROOT_DIR)
data = append_doc(data)
data = append_tag(data)
data = append_vec(data)
data = append_xyz(data)

