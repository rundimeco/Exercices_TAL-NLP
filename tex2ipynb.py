import sys
import json
import os
import re

def clean_tex(l):
  print(l)
  l2 = re.sub(".vspace{.*?}", "", l)
  l2 = re.sub("{style=.*?}", "", l2)
  l2 = re.sub(".footnote", "\\\\textit", l2)
  #texttt : ` `
  titre = re.findall("exer{(.*?)}", l2)
  if len(titre)>0:
    l2 = "\\section{%s}"%titre[0] 
  print(l2)
  return l2

def markdownize(s):
  w = open("tmp.tex", "w")
  w.write(s)
  w.close()
  cmd = "pandoc -s tmp.tex -o tmp.md"
  os.system(cmd)
  f = open("tmp.md")
  s = f.read()
  f.close()
  return s

tex_path = sys.argv[1]
print(f"IN :{tex_path}") 
f = open(tex_path)
lignes = f.readlines()
f.close()

is_py = False
f = open("ressources/base.ipynb")
dic = json.load(f)
f.close()
{"cells" : []}

source = []
for l in lignes:
  if "begin{" in l:
    if "python" in l:
      is_py = True
      source = markdownize(" ".join(source))
      dic["cells"].append({"cell_type":"markdown","metadata":{}, "source":source})
      source = []
    continue
  elif "end{" in l:
    if "python" in l:
      is_py = False
#      dic["cells"].append({"cell_type":"markdown","metadata":{}, "source":source})
      dic["cells"].append({"cell_type":"code","metadata":{}, "execution_count": 0, "outputs": [],"source":source})
      source = []
    continue
  source.append(clean_tex(l))

w = open(f"{tex_path}.ipynb", "w")
w.write(json.dumps(dic, indent=1))
w.close()

print(f"OUT:{tex_path}.ipynb") 
