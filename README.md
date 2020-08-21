# pymicromegas
Python interface of micromegas.

## Features
pymicromegas:

- directly reseives your model parameters as Python `dict` (does not generate internal `.par` files)
- can switch on/off by `flags` parameter

If you don't like Python, instead, you can use `main.c/cpp` in `/pymicromegas/` just as normal `main.c/cpp` of micromegas.
These modified `main` files receive arguments like:
```
./main <integer to define flags> <n: number of parameters> <parmeter name 1> ... <parmeter name n> <parmeter value 1> ... <parmeter value n>
```


# How to use it

`git clone` to download pymicromegas. Then 

```python
from pymicromegas import PyMicrOmegas

interf = PyMicrOmegas()
project = interf.create_newproject("test")
project.load_mdl_files(["the", "list of", "your", ".mdl file", "paths"])
project.compile()  # once a project is compiled, you can directly call the compiled project as Project(project_name).


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

#process = project.run(args,flags)  # return subprocess.CompletedProcess
#print(process.stdout)  # print the output text of micromegas

print(project(args,flags))  # directly return parsed output (at present, relic density only)
```

# Class

## `PyMicrOmegas`
- wrapper class of doing `newProject`, `make`, `make clean` in the micromegas directory.
- When pymicromegas imported for the first time, it unzip `miccromegas_5.0.8.tgz` and install (make) it

If you want to modify micromegas, 
1. clean
1. modify 
1. make again
    
## `Project`
  - wrapper class of `make`, `./main ...`, in project directories.
  - `Prpject.__call__` to directly return parsed micromegas outputs (callable object, used as if it is like a function. See the previous example.)


# TODO
- etc...
