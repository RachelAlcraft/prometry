

######### TEST THE DATAFRAME ##############################





## Ensure code is imported in path
import sys
from pathlib import Path
CODEDIR = str(Path(__file__).resolve().parent.parent )+ "/src/"
sys.path.append(CODEDIR)
DATADIR = str(Path(__file__).resolve().parent )+ "/data/"

from prometry import pdbloader as pl
from prometry import pdbgeometry as pg

pdbs =  ['1ejg']
pobjs = []

print("---")
for pdb in pdbs:    
    pla = pl.PdbLoader(pdb,DATADIR,cif=True)    
    po = pla.load_pdb()    
    pobjs.append(po)
    #for line in po.lines(atoms=True):
    #    print(line)
   
"""
Simplest so far:
[] after a geo specify a comma delim list of criteria, pmly so far

aa - amino acid of the residue

dis - distance from the first atom where
< less than
> greater than
<> between
>< extremes

occ - occupancy, with just =, < or >


"""

gm = pg.GeometryMaker(pobjs)

#for geo in ['{(N),(C)}[aa:ser]:(O)','(O):{(N),OG}','(N):(O)+1','(O):(N)@1']:
geos = ['N[aa|ser]:{(O)}[dis|2.0<>3.00]','N:CA:C']
for geo in geos:
    print("-----",geo,"-----")
    df = gm.calculateGeometry([geo],log=0)
    print(df)
print("----- geos -----")
df = gm.calculateGeometry(geos,log=0)
print(df)

geos = ['O:{(N),(O)&1}[dis|2.5<>3.00]','N:CA:C']
for geo in geos:
    print("-----",geo,"-----")
    df = gm.calculateGeometry([geo],log=0)
    print(df)
print("----- geos -----")
df = gm.calculateGeometry(geos,log=0)
print(df)

geos = ['N[occ|=1]:CA[occ|=1]']
for geo in geos:
    print("-----",geo,"-----")
    df = gm.calculateGeometry([geo],log=0)
    print(df)
print("----- geos -----")
df = gm.calculateGeometry(geos,log=0)
print(df)




    


