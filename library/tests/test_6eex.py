import os, sys
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(Path(__file__).parent),"src"))
from prometry import pdbloader as pl
from prometry import pdbgeometry as pg


import pandas as pd

DATADIR = "tests/data/"
ls_structures = ['6eex','6ee1']


def test_atoms():
    pobjs = []
    for pdb in ls_structures:            
        pla = pl.PdbLoader(pdb,DATADIR,cif=False,source="ebi")
        po = pla.load_pdb()        
        pobjs.append(po)        
    gm = pg.GeometryMaker(pobjs)
    df = gm.calculateData()
    print(df.to_csv())
    
def test_backbone():
    ls_geos = ['N:CA', 'N:CA:C', 'N:CA:C:N+1']        
    pobjs = []
    for pdb in ls_structures:            
        pla = pl.PdbLoader(pdb,DATADIR,cif=False,source="ebi")
        po = pla.load_pdb()
        pobjs.append(po)
    gm = pg.GeometryMaker(pobjs)
    df = gm.calculateGeometry(ls_geos)
    print(df.to_csv())


if __name__ == "__main__":
    test_atoms()
    test_backbone()