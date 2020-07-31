import os
import subprocess
import sys
from pathlib import Path 
import numpy as np


dir_micromegas = os.path.dirname(__file__) + "/micromegas_5.0.8/"



FLAGS = {
    "MASSES_INFO"        : (1 << 0),
    "CONSTRAINTS"        : (1 << 1),
    "MONOJET"            : (1 << 2),
    "HIGGSBOUNDS"        : (1 << 3),
    "HIGGSSIGNALS"       : (1 << 4),
    "LILITH"             : (1 << 5),
    "SMODELS"            : (1 << 6),
    "OMEGA"              : (1 << 7),
    "FREEZEIN"           : (1 << 8),
    "INDIRECT_DETECTION" : (1 << 9),
    "RESET_FORMFACTORS"  : (1 << 10),
    "CDM_NUCLEON"        : (1 << 11),
    "CDM_NUCLEUS"        : (1 << 12),
    "NEUTRINO"           : (1 << 13),
    "DECAYS"             : (1 << 14),
    "CROSS_SECTIONS"     : (1 << 15),
    "SHOWPLOTS"          : (1 << 16),
    "CLEAN"              : (1 << 17)
}


#def flag_to_int(flag_name,bool_flag):
#    if type(bool_flag) is not bool: raise TypeError("invalid input for {}".format(key))
#    if bool_flag:
#        return FLAGS[flag_name]
#    else:
#        return 0

    
#def flags_to_int(dict_flags):
#    int_flags = [flag_to_int(flag_name,bool_flag) for flag_name,bool_flag in dict_flags.items() ] 
#    return sum(int_flags)
    
    
    
def run_bash(command,shell=True,stdout=subprocess.PIPE,encoding="UTF-8",check=True,input=None,cwd=None):
    return subprocess.run(command,shell=shell,stdout=stdout,encoding=encoding,check=check,input=input,cwd=cwd)



class PyMicrOmegas:    
    
    def __init__(self,verbose=False):
        self.path = dir_micromegas
        
        if os.path.isfile(self.path + "include/microPath.h"): 
            pass
        else:
            print("PyMicrOmegas: micromegas are not installed yet. Start install automatically...")
            outout = self.compile_micromegas()
            print("PyMicrOmegas: micromegas are installed.")
            if verbose: print(output)
            #raise RuntimeError("micromegas is not properly installed. Run 'make all' in micromegas_5.0.8 directory")
    
    
    def run_bash(self,command,shell=True,stdout=subprocess.PIPE,encoding="UTF-8",check=False,input=None):
        return run_bash(command,shell=shell,stdout=stdout,encoding=encoding,check=check,input=input,cwd=self.path)
    
    
    def compile_micromegas(self):
        return self.run_bash("make")

    
    def clean_micromegas(self):
        return self.run_bash("make clean",input="y\n")
    
    
    def project_exists(self,project_name):
        return os.path.isdir(self.path + project_name)
        
    
    def create_newproject(self,project_name,return_project=False):
        if self.project_exists(project_name): 
            raise RuntimeError("project '{}' exists already.".format(project_name))
            
        commands = [ "./newProject {0}", "mv {0}/main.cpp {0}/main_original.cpp", "cp ../main.c {0}/", "cp ../main.cpp {0}/"]
        process = self.run_bash("\n".join(commands).format(project_name))
        
        if return_project:
            return Project(project_name)
        else: 
            return process
        
    
    def load_project(self,project_name):
        if self.project_exists(project_name):
            return Project(project_name)
        else:
            print("Project {} is not created yet. Start creating...".format(project_name))
            return self.create_newproject(project_name,return_project=True)
    
    
#    def load_mdl(self,project_name,mdl_paths):
#        if self.project_exists(project_name): raise RuntimeError("project '{}' exists already.".format(project_name))
#        for path in mdl_paths:
#            if path[-4:] != ".mdl": raise RuntimeError("{} is not .mdl file".format(path))
#            commands = [ "cd {0}","cp main=main.cpp"]
    

    
class Project:
    
    
    def __init__(self,project_name):
        if not PyMicrOmegas().project_exists(project_name): raise RuntimeError("Project {} does not exist yet. Create it by PyMicrOmegas.create_newproject.".format(project_name))
        self.project_name = project_name
        self.path = dir_micromegas + project_name + "/"
        self.models_path = self.path + "work/models/"
    
    
    def run_bash(self,command,shell=True,stdout=subprocess.PIPE,encoding="UTF-8",check=False,input=None):
        '''
        run './main' and return the output string.
        '''
        return run_bash(command,shell=shell,stdout=stdout,encoding=encoding,check=check,input=input,cwd=self.path)
    
    
    def load_mdl_files(self,mdl_paths):
        if type(mdl_paths) not in [list, tuple]: raise RuntimeError("input arguments must be list or tuple.")
        processes = []
        for mdl_path in mdl_paths:
            if not os.path.isfile(mdl_path): raise RuntimeError("{} does not existing file".format(mdl_path))
            abs_mdl_path = str(Path(mdl_path).resolve())
            process = self.run_bash("cp {} {}".format(abs_mdl_path,self.models_path))
            processes.append(process)
        return processes
    
        
    def compile(self,main="main.c"):
        #process = subprocess.run("bash install_project.sh " + project_name,shell=True,stdout=subprocess.PIPE)
        return self.run_bash("make main={}".format(main))
           
      
    def clean(self):
        return self.run_bash("make clean")
    
    
    @property
    def vars(self):
        vars = np.loadtxt(self.models_path+"vars1.mdl",skiprows=3,delimiter="|",dtype=str)
        return vars
    
    
    def run(self,dict_parameters,flags=None):
        """
        kwargs: see 'PyMicrOmegas.FlAGS.keys()'. 
        """
        
        #int_flags = flags_to_int(kwargs)
        int_flags = 0 if (flags is None) else sum( FLAGS[key] for key in flags )

        n_inputvals = len(dict_parameters)
        par_names = " ".join(map(str,dict_parameters.keys()))
        par_vals  = " ".join(map(str,dict_parameters.values()))
        args = "{} {} {} {}".format(int_flags,n_inputvals,par_names,par_vals)
        print(args)
        return self.run_bash("./main {}".format(args))
    
        
        
    
    