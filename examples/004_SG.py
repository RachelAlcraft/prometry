

######### TEST THE DATAFRAME ##############################





## Ensure code is imported in path
import sys
from pathlib import Path
CODEDIR = str(Path(__file__).resolve().parent.parent )+ "/src/"
sys.path.append(CODEDIR)
DATADIR = str(Path(__file__).resolve().parent )+ "/data/"

from leuci_geo import pdbloader as pl
from leuci_geo import pdbgeometry as pg

pdbs =  ['6zx4','3u7z','6vb2']
pobjs = []

print("---")
for pdb in pdbs:    
    pla = pl.PdbLoader(pdb,DATADIR,cif=True)    
    po = pla.load_pdb()
    print(po,len(po.lines()))
    print("---")
    pobjs.append(po)
   #for line in po.lines(atoms=False):
   #     print(line)

gm = pg.GeometryMaker(pobjs)
for geo in ['SG:{SG}+1','SG:{N}+2','SG:{SG@1}','SG:{SG@2}','SG:SG','SG:(N)','SG:N']:
    print("-----",geo,"-----")
    df = gm.calculateGeometry([geo],log=0)
    print(df)




    


