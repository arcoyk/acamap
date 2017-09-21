import os
from subprocess import call

def mkdir(d):
  call(['rm', '-rf', d])
  call(['mkdir', d])
  return d

def pdftotext(pdf_path, text_path):
  call(['pdftotext', pdf_path, text_path])
  return text_path

def get_all_paths(r):
  return list(map(lambda x:'/'.join([r,x]), os.listdir(r)))

def pdfpath2textpath(pdf_path):
  return textpath

def pathlize(a):
  return '/'.join(a)

def create_dir(pdf_path, root):
  # pdf_path = 'pdfs/sample.pdf'
  # pdf_name = 'sample'
  pdf_name = pdf_path.split('/')[-1].split('.pdf')[0]
  mkdir(pathlize([root, pdf_name]))
  pdftotext(pdf_path, pathlize([root, pdf_name, pdf_name + '.txt']))
  mkdir(pathlize([root, pdf_name, 'refs']))

pdf_paths = get_all_paths('pdfs')
root = 'referencing'
mkdir(root)
for pdf_path in pdf_paths:
  create_dir(pdf_path, root)
