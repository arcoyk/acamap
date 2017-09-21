from os import listdir
import logging
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure as fig
from sklearn.decomposition import PCA
from gensim.models.doc2vec import LabeledSentence
from gensim import models
from subprocess import call

DATA_DIR = './data/'
MODEL_DIR = 'doc2vec.model'

def pdf2text(pdf_path):
    pdf_name = pdf_path.split('/')[-1]
    text_path = DATA_DIR + pdf_name + '.txt'
    call(('pdftotext %s %s' % (pdf_path, text_path)).split(' '))
    return text_path

def read_doc(path):
    words = []
    with open(path) as f:
        words = f.read().split(' ')
    name = path.split('/')[-1]
    return LabeledSentence(words = words, tags=[name])
# Train
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = [read_doc(DOCS_DIR + x) for x in listdir(DOCS_DIR)]

if True:
    model = models.Doc2Vec(sentences)
    for epoch in range(20):
        model.train(sentences)
        model.alpha -= (0.025 - 0.0001) / 19
        model.min_alpha = model.alpha
    model.save(MODEL_DIR)

model = models.Doc2Vec.load(MODEL_DIR)

X = [model.docvecs[tag] for tag in model.docvecs.doctags]
T = [tag for tag in model.docvecs.doctags]

# PCA
X = np.array(X)
pca = PCA(n_components=2)
X = pca.fit_transform(X)

# Plot
plt.figure(num=None, figsize=(30, 20), dpi=80, facecolor='w', edgecolor='w')
plt.plot(X[:,0], X[:,1], '.')
for i in range(len(X)):
    x = X[i][0]
    y = X[i][1]
    t = T[i]
    plt.text(x, y, t)

plt.savefig('pyplot.png')
plt.show()
plt.draw()
