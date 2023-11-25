import os, sys
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(Path(__file__).parent),"src"))
from prometry import pdbloader as pl
from prometry import pdbgeometry as pg


import pandas as pd

DATADIR = "tests/data/"
ls_structures = ['1ejg']

    
def test_aa():    
    ls_geos = ['N:CA[aa|GLY]']
    pobjs = []
    for pdb in ls_structures:            
        pla = pl.PdbLoader(pdb,DATADIR,cif=False,source="ebi")
        po = pla.load_pdb()
        pobjs.append(po)
    gm = pg.GeometryMaker(pobjs)
    df = gm.calculateGeometry(ls_geos)
    print(df.T)

def test_no():    
    ls_geos = ['N:{N,O}','N:{N,O@1}','N:{N,O&1}','N:{N,O&1}','N:(N,O)','N:(N,O@1)','N:(N,O&1)','N:(N,O&2)']
    #ls_geos = ['N:(N,O&1)']
    pobjs = []
    for pdb in ls_structures:            
        pla = pl.PdbLoader(pdb,DATADIR,cif=False,source="ebi")
        po = pla.load_pdb()
        pobjs.append(po)
    gm = pg.GeometryMaker(pobjs)
    df = gm.calculateGeometry(ls_geos)
    print(df.T)


if __name__ == "__main__":
    test_aa()
    test_no()
    