import os

def get_references(text):
  r = text.find('REFERENCE')
  return text[r:]

def get_head(text):
  return text[:500]

def validate(point):
  p = point > 10
  return p

def skipwords(tar, skips):
  return list(filter(lambda x:not x in skips, tar))

def is_referenced(from_text, to_text):
  refs_words = get_references(from_text).split(' ')
  refs_words = skipwords(refs_words, SW)
  tops_words = get_head(to_text).split(' ')
  tops_words = skipwords(tops_words, SW)
  rst = []
  for rw in refs_words:
    if rw in tops_words:
      rst.append(rw)
  return validate(len(rst))

def get_text(path):
  with open(path) as f:
    return f.read()

to_text = get_text('text/101.txt')
from_text = get_text('text/103.txt')

def test_all_pattern(text_paths):
  for i in range(len(text_paths)):
    for k in range(len(text_paths))[i+1:]:
      to_text_path = text_paths[i]
      from_text_path = text_paths[k]
      to_text = get_text(to_text_path)
      from_text = get_text(from_text_path)
      flag = is_referenced(from_text, to_text)
      if flag:
        print(from_text_path + ',' + to_text_path)

def pathlize(a):
  return '/'.join(a)

def get_all_paths(r, d=list()):
  if r.find('.txt') != -1:
    d += [r]
    return
  else:
    for f in os.listdir(r):
      if not f == '.DS_Store':
        get_all_paths(pathlize([r, f]), d)
  return d

def only_txt(paths):
  return list(filter(lambda x:x.find('txt') != -1, paths))

SW = list(set(get_text('skipwords.txt').split('\n')))
paths = get_all_paths('referencing')
text_paths = only_txt(paths)
test_all_pattern(text_paths)



