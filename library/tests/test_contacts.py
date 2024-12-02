import os, sys
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(Path(__file__).parent),"src"))
from prometry import pdbloader as pl
from prometry import pdbgeometry as pg
from prometry import pdbcontacts as pc


import pandas as pd

DATADIR = "tests/data/"
ls_structures = ['6eex']

   
def test_nn():    
    ls_geos = ['N:{N@i}[dis|0.0<>10.0,rid|>2]']
    pobjs = []
    for pdb in ls_structures:            
        pla = pl.PdbLoader(pdb,DATADIR,cif=False,source="ebi")
        po = pla.load_pdb()
        pobjs.append(po)
    gm = pg.GeometryMaker(pobjs)
    df = gm.calculateGeometry(ls_geos)
    print(df)

def test_nn_2d():    
    geo = 'N:N[dis|0.0<>10.0,rid|>2]'
    pobjs = []
    for pdb in ls_structures:            
        pla = pl.PdbLoader(pdb,DATADIR,cif=False,source="ebi")
        po = pla.load_pdb()
        pobjs.append(po)
    cm = pc.ContactMaker(pobjs)
    df = cm.calculateContacts(geo)
    print(df)

 


if __name__ == "__main__":
    test_nn()
    

    