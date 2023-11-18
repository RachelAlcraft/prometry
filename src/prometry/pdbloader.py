
from os.path import exists
import urllib.request

from Bio.PDB.MMCIFParser import MMCIFParser        
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
from Bio.PDB.PDBParser import PDBParser
import warnings
from Bio import BiopythonWarning
warnings.simplefilter('ignore', BiopythonWarning)

from . import pdbobject as po

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
class PdbLoader(object):
    def __init__(self, pdb_code, directory="", cif=False,source="ebi"):        
        self.pdb_code = pdb_code
        self.directory = directory        
        self.cif = cif
        self.pobj = po.PdbObject(pdb_code)                
        if source == "ebi":
            self.cif_filepath = f"{directory}{pdb_code}.cif"
            self.cif_url = f"https://www.ebi.ac.uk/pdbe/entry-files/download/{pdb_code}.cif"        
            self.pdb_filepath = f"{directory}{pdb_code}.pdb"
            self.pdb_url = f"https://www.ebi.ac.uk/pdbe/entry-files/download/pdb{pdb_code}.ent"
        elif source == "alphafold":
            #https://alphafold.ebi.ac.uk/files/AF-Q8CGX5-F1-model_v4.pdb
            #https://alphafold.ebi.ac.uk/files/AF-Q8CGX5-F1-model_v4.cif
            self.cif_filepath = f"{directory}{pdb_code}.cif"
            self.cif_url = f"https://alphafold.ebi.ac.uk/files/{pdb_code}.cif"
            self.pdb_filepath = f"{directory}{pdb_code}.pdb"
            self.pdb_url = f"https://alphafold.ebi.ac.uk/files/{pdb_code}.pdb"
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
    def exists_pdb(self):
        if exists(self._filepath):
            return True
        else:            
            return False
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
    def download_pdb(self,cif=False):
        if cif:
            if not exists(self.cif_filepath):
                try:            
                    urllib.request.urlretrieve(self.cif_url, self.cif_filepath)                                
                except:            
                    return False
        else:
            if not exists(self.pdb_filepath):
                try:            
                    urllib.request.urlretrieve(self.pdb_url, self.pdb_filepath)                                
                except:            
                    return False
        return True
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
    def load_pdb(self):
        loaded = False
        if self.cif:
            try:
                self.download_pdb(cif=True)
                structure = MMCIFParser().get_structure(self.pdb_code, self.cif_filepath)            
                loaded = True
            except Exception as e:                              
                print("Error loading cif file", str(e))
                loaded = False
        if not loaded:
            self.download_pdb(cif=False)            
            structure = PDBParser(PERMISSIVE=True).get_structure(self.pdb_code, self.pdb_filepath)                                        
        self.pobj.add_atoms(structure)                
        #print(structure.header)
        return self.pobj
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""