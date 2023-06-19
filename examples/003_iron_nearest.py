

######### TEST THE DATAFRAME ##############################





## Ensure code is imported in path
import sys
from pathlib import Path
CODEDIR = str(Path(__file__).resolve().parent.parent )+ "/src/"
sys.path.append(CODEDIR)
DATADIR = str(Path(__file__).resolve().parent )+ "/data/"

from leuci_geo import pdbloader as pl
from leuci_geo import pdbgeometry as pg

pdbs = ["5d8v"]
pdbs = ['4u9h','5jsk','6rk0']
pobjs = []

print("---")
for pdb in pdbs:    
    pla = pl.PdbLoader(pdb,DATADIR,cif=True)    
    po = pla.load_pdb()
    print(po,len(po.lines()))
    print("---")
    pobjs.append(po)
    #for line in po.lines(atoms=False):
    #    print(line)

gm = pg.GeometryMaker(pobjs)
#geos = ['FE:{O}','FE:{O@2}','FE:{O,N,NE2}','FE:{O,N@2}','(FE):(O,N)+1']
geos = ['FE:{(N),(O)}','FE:{(N),(O)@2}','FE:{(N),(O)&2}','(FE):(O,N)+1']
#geos = ['FE:{N,O}','FE:{N,O@2}','FE:{N,O@3}']
for geo in geos:
    df = gm.calculateGeometry([geo],log=0)
    print(df)

df = gm.calculateGeometry(geos,log=0)
print(df)




    


