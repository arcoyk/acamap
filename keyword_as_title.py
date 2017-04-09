import time
import random
import os
import numpy as np
from gensim.summarization import keywords
from os import listdir

def get_keywords(q):
  k = ""
  try:
    k = keywords(q, ratio=0.01)
  except:
    print("Error")
  return k.split("\n")

def read_socket(fname):
  with open(fname) as f:
    return f.read()

def write_socket(fname, w):
  with open(fname, 'w') as f:
    f.write(w)

def get_hand_keywords(q):
    for line in q.split('\n'):
        if (len(line.split(';')) > 1):
            return(line.split(';'))

def gen_keyword_all():
  d = "/users/yui/Projects/acamap/text/"
  text = ""
  lim = 40
  cnt = 0
  for f in listdir(d):
    cnt += 1
    if cnt > lim:
        break
    if f == ".DS_Store":
      continue
    fullpath = (d + f)
    with open(fullpath) as src:
        text += src.read()
    # print(get_hand_keywords(text))
    # s = read_socket(dd)
    # keys = get_keywords(s)
    # print((",").join(keys))
    # write_socket(tar, ("\n").join(keys))
  return get_keywords(text)

def gen_keys_titles():
  d = "/users/yui/Projects/acamap/text/"
  keys_titles = []
  lim = 1000
  cnt = 0
  for f in listdir(d):
    cnt += 1
    if cnt > lim:
      break
    if f == ".DS_Store":
      continue
    fullpath = (d + f)
    text = ""
    with open(fullpath) as src:
      text = src.read()
    keys_titles.append([get_keywords(text), f])
  return keys_titles

def gen_keyword():
  d = "/users/yui/Projects/acamap/text/"
  keys = []
  lim = 1000
  cnt = 0
  for f in listdir(d):
    cnt += 1
    if cnt > lim:
        break
    if f == ".DS_Store":
      continue
    fullpath = (d + f)
    text = ""
    with open(fullpath) as src:
        text = src.read()
    # print(get_hand_keywords(text))
    keys.append(get_keywords(text))
    # s = read_socket(dd)
    # keys = get_keywords(s)
    # print((",").join(keys))
    # write_socket(tar, ("\n").join(keys))
  return keys

def similar(a, b):
    small = a
    big = b
    if small > big:
        small = b
        big = a
    for i in range(len(small)):
        if i < len(big) * 0.5 and small[i] != big[i]:
            return False
    return True

def smaller(a, b):
    return [a, b][len(a) > len(b)]

def word_groups(uniq):
    uniq.sort()
    near = False
    tars = []
    tar = []
    for u in uniq:
        if len(tar) == 0 or similar(tar[0], u):
            tar.append(u)
        else:
            tars.append(tar)
            tar = [u]
    tars.append(tar)
    return tars

def flatten(not_flat):
    flat = []
    for arr in not_flat:
        for a in arr:
            flat.append(a)
    return flat

def uniq(not_uniq):
    return list(set(not_uniq))

def simplize(keys, wgs):
    result = []
    for key in keys:
        for wg in wgs:
            if key in wg:
                result.append(wg[0])
                break
    result.sort()
    return list(set(result))

def write_in_tags_titles(tags_titles):
    text_d = "/users/yui/Projects/acamap/text/"
    tags_d = "/users/yui/Projects/acamap/tags/"
    for x in tags_titles:
        tags = x[0]
        title = x[1]
        with open(text_d + title) as text_f:
            text = text_f.read()
            if len(tags) >= 1:
                title += "." + ('_').join(tags)
            print(tags_d + title)
            with open(tags_d + title, 'w') as tags_f:
                tags_f.write(text)

tags = ['virtual', 'design', 'display', 'interact', 'gesture', 'haptic', 'physic', 'touch']
keys_titles = gen_keys_titles()
tags_titles = []
for x in keys_titles:
    hit = []
    keys = x[0]
    title = x[1]
    for key in keys:
        for tag in tags:
            if similar(tag, key):
                hit.append(tag)
    hit = list(set(hit))
    tags_titles.append([hit, title])
write_in_tags_titles(tags_titles)
