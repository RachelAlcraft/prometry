

######### TEST THE DATAFRAME ##############################





## Ensure code is imported in path
import sys
from pathlib import Path
CODEDIR = str(Path(__file__).resolve().parent.parent )+ "/src/"
sys.path.append(CODEDIR)
DATADIR = str(Path(__file__).resolve().parent )+ "/data/"

from prometry import pdbloader as pl
from prometry import pdbgeometry as pg


"""
With no brackets or symbols, the simple case is that you are looking for atom types within a residue
e.g.
N:CA - is looking for all atoms of type N and the CA in the same residue, for the distance
N:CA:C - is looking for all atoms of types N, CA and C in the same residue and the angle
+/- look for neighbouring residues
C:N+1 - looks for the C in a residue and the N in the next residue
C-1:N - as per above but the start

() brackets symbolise element rather than atom type, eg N can mean NZ, NE1 etc, and this starts a nearest lookup if it is not the first item, or a cross product if it is
(N):N - means any type N, and the N in the same residue - there can be more than 1 per residue
N:(N) - means all N's in a reside and the nearest type N in the same residue - only 1 per residue

{} symbolise distance searchers - the list of atoms is all the candidates
N:{O,N} is all N's in a residue and the nearest O or N to it - 1 per residue

() brackets can be used
N:{(O),(N)} is all N's in a residue and the nearest O type or N type to it - 1 per residue

operators @ or & specify x nearest or at least x away as follows
N:{O,N@1} means N and the second nearest  O or N to it - 0 indexed
N:{O,N&2} means N and the nearest O or N as long as it is at least 2 residues away

"""
print("---")
pdbs =  ['6eex']
pobjs = []
for pdb in pdbs:    
    pla = pl.PdbLoader(pdb,DATADIR,cif=True)    
    po = pla.load_pdb()    
    pobjs.append(po)       
gm = pg.GeometryMaker(pobjs)
geos = ['N:O','N:{N,O}','N:{N,O@1}','N:{N,O&2}']
df = gm.calculateGeometry(geos,log=0)
print(df)

print("---")
pdbs =  ['2xjh']
pobjs = []
for pdb in pdbs:    
    pla = pl.PdbLoader(pdb,DATADIR,cif=True)    
    po = pla.load_pdb()    
    pobjs.append(po)   
gm = pg.GeometryMaker(pobjs)
geos = ['SG:{SG@1}']
#geos = ['N:O','N:{N,O}','N:{N,O@1}','N:{N,O&2}']
df = gm.calculateGeometry(geos,log=0)
print(df)




    


