import os, sys
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(Path(__file__).parent),"src"))
from prometry import pdbloader as pl
from prometry import pdbgeometry as pg


import pandas as pd

DATADIR = "tests/data/"
ls_structures = ['4i8g']

def test_backbone():    
    ls_geos = ['CA[aa|ALA]:CA+1']    
    pobjs = []
    for pdb in ls_structures:            
        pla = pl.PdbLoader(pdb,DATADIR,cif=False,source="ebi")
        po = pla.load_pdb()
        pobjs.append(po)
    gm = pg.GeometryMaker(pobjs)
    df = gm.calculateGeometry(ls_geos)
    print(df.max())
    print(df[["info_CA[aa|ALA]:CA+1","CA[aa|ALA]:CA+1","occ_CA[aa|ALA]:CA+1"]])
    

if __name__ == "__main__":    
    test_backbone()