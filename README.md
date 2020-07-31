# pymicromegas
Python interface of micromegas.

## features
pymicromegas:

- directly reseives your model parameters as Python `dict` (does not generate internal `.par` files)
- can switch on/off by `flags` parameter

# How to use it

`git clone` to download pymicromegas. Then 

```python
from pymicromegas import PyMicrOmegas

interf = PyMicrOmegas()
project = interf.create_newproject("test")
project.load_mdl_files(["the", "list of", "your", ".mdl file", "paths"])

args = {
  "parname1" : 1.0  # parameter values
  "parname2" : 10   
  "parname3" : 1e-8
}

##########
# flags: defined in pymicromegas.FLAGS. 
# 
# List of available flags:
# ['MASSES_INFO','CONSTRAINTS','MONOJET','HIGGSBOUNDS', 'HIGGSSIGNALS', 'LILITH', 'SMODELS', 'OMEGA', 'FREEZEIN', 'INDIRECT_DETECTION', 'RESET_FORMFACTORS', 'CDM_NUCLEON', 'CDM_NUCLEUS', 'NEUTRINO', 'DECAYS', 'CROSS_SECTIONS', 'SHOWPLOTS', 'CLEAN']
##########
flags = ["MASSES_INFO","OMEGA"]

process = project.run(args,flags)  # return subprocess.CompletedProcess
print(process.stdout)  # print the output text of micromegas
```

# TODO
- parse output text
- etc...
