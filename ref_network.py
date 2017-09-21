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

def get_all_refs(text_paths):
  rst = []
  for i in range(len(text_paths)):
    for k in range(len(text_paths))[i+1:]:
      to_text_path = text_paths[i]
      from_text_path = text_paths[k]
      to_text = get_text(to_text_path)
      from_text = get_text(from_text_path)
      flag = is_referenced(from_text, to_text)
      if flag:
        rst.append([from_text_path, to_text_path])
  return rst

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

def path2name(path):
  return path.split('/')[-1].split('.')[0]

def dquote_join(c, a):
  return c.join(list(map(lambda x:'"'+x+'"', a)))

def to_json(refs):
  # data restruction
  uniq_from = list(set(map(lambda x:x[0], refs)))
  h = {}
  for u in uniq_from:
    h[u] = list()
  for from_path in uniq_from:
    for ref in refs:
      if ref[0] == from_path:
        h[from_path].append(ref[1])
  # to list and rename
  net = []
  for k in h:
    net.append([path2name(k), list(map(lambda x:path2name(x), h[k]))])
  # to json
  print('{"nodes":[')
  for link in net:
    print('{')
    print('"node_name":"' + link[0] + '",')
    print('"link_to":[' + dquote_join(',', link[1]) + '],')
    print('"attributes":["HCI"]')
    print('},')
  print(']}')


SW = list(set(get_text('skipwords.txt').split('\n')))
paths = get_all_paths('referencing')
text_paths = only_txt(paths)
refs = get_all_refs(text_paths)
to_json(refs)



