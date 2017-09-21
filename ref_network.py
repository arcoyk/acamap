def get_references(text):
  r = text.find('REFERENCE')
  return text[r:]

def get_head(text):
  return text[:500]

def validate(point):
  p = point > 40
  return p

def is_referenced(from_text, to_text):
  refs_words = get_references(from_text).split(' ')
  tops_words = get_head(to_text).split(' ')
  print(refs_words)
  print("vs")
  print(tops_words)
  print()
  point = 0
  for rw in refs_words:
    if rw in tops_words:
      point += 1
      print(rw)
  return validate(point)

def get_text(path):
  with open(path) as f:
    return f.read()

to_text = get_text('text/101.txt')
from_text = get_text('text/103.txt')

print(is_referenced(from_text, to_text))

