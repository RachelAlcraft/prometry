

######### TEST THE DATAFRAME ##############################





## Ensure code is imported in path
import sys
from pathlib import Path
CODEDIR = str(Path(__file__).resolve().parent.parent )+ "/src/"
sys.path.append(CODEDIR)
DATADIR = str(Path(__file__).resolve().parent )+ "/data/"

from leuci_geo import pdbloader as pl
from leuci_geo import pdbgeometry as pg

pdbs = ["1ejg","6eex","7uly","3nir","5d8v"]
pobjs = []

print("---")
for pdb in pdbs:    
    pla = pl.PdbLoader(pdb,DATADIR,cif=True)    
    po = pla.load_pdb()
    print(po,len(po.lines()))
    print("---")
    pobjs.append(po)

gm = pg.GeometryMaker(pobjs)
df = gm.calculateGeometry(['C:O','C:N+1'])
print(df)


    


