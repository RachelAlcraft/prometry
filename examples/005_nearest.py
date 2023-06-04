

######### TEST THE DATAFRAME ##############################





## Ensure code is imported in path
import sys
from pathlib import Path
CODEDIR = str(Path(__file__).resolve().parent.parent )+ "/src/"
sys.path.append(CODEDIR)
DATADIR = str(Path(__file__).resolve().parent )+ "/data/"

from leuci_geo import pdbloader as pl
from leuci_geo import pdbgeometry as pg

pdbs =  ['6eex']
pobjs = []

print("---")
for pdb in pdbs:    
    pla = pl.PdbLoader(pdb,DATADIR,cif=True)    
    po = pla.load_pdb()    
    pobjs.append(po)
    #for line in po.lines(atoms=True):
    #    print(line)
   
gm = pg.GeometryMaker(pobjs)
#for geo in ['{(N),(C)}[aa:ser]:(O)','(O):{(N),OG}','(N):(O)+1','(O):(N)@1']:
for geo in ['N[aa|ser]:CA[dis|<1.456]']:
    print("-----",geo,"-----")
    df = gm.calculateGeometry([geo],log=0)
    print(df)




    


