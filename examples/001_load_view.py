## Ensure code is imported in path
import sys
from pathlib import Path
CODEDIR = str(Path(__file__).resolve().parent.parent )+ "/src/"
sys.path.append(CODEDIR)
DATADIR = str(Path(__file__).resolve().parent )+ "/data/"
from leuci_geo import pdbloader as pl

pdbs = ["1ejg","6eex","7uly","3nir"]

print("---")
for pdb in pdbs:    
    pla = pl.PdbLoader(pdb,DATADIR,cif=True)    
    po = pla.load_pdb()
    print(po,len(po.lines()))
    print("---")
    
