import os, sys
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(Path(__file__).parent),"src"))
from prometry import pdbloader as pl
from prometry import pdbgeometry as pg


import pandas as pd

DATADIR = "tests/data/"
ls_structures = '2h8f 3d1k 3bom 4esa 5eui 6zmx 6ihx 6ii1 7dy3 7dy4 1uiw 6kah 6kai 6ka9 6kae 6lcx 6lcw 6l5w 6kao 6kaq 6kap 6l5v 1bab 1bz0 1ird 3s66 7jy3'.split(" ")

    
def test_one():
    ls_geos = ['FE:{N,O}']
    pobjs = []
    for pdb in ls_structures:
        print(pdb)         
        pla = pl.PdbLoader(pdb,DATADIR,cif=False,source="ebi")
        po = pla.load_pdb()
        pobjs.append(po)
    print("make geo")
    gm = pg.GeometryMaker(pobjs)
    print("make geo calc")
    df = gm.calculateGeometry(ls_geos)
    print(df)


if __name__ == "__main__":
    test_one()
    