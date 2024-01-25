import os, sys
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(Path(__file__).parent),"src"))
from prometry import pdbloader as pl
from prometry import pdbgeometry as pg


import pandas as pd

DATADIR = "tests/data/" 
ls_structures = ['6eex']
#ls_structures = ['5nqo']

   
def test_i_rid():
    geo = "CA:{CA@i}[rid|>1]:{CA@i}[rid|>1]"
    #minmax = ["MINDIS|","MAXDIS|","SUMDIS|"]
    minmax = ["SUMDIS|"]
    for mm in minmax:    
        pobjs = []
        for pdb in ls_structures:            
            pla = pl.PdbLoader(pdb,DATADIR,cif=False,source="ebi")
            po = pla.load_pdb()
            pobjs.append(po)
        gm = pg.GeometryMaker(pobjs)
        df = gm.calculateGeometry([mm+geo])
        print("rows=",len(df.index))
        print(df)
    


if __name__ == "__main__":   
    test_i_rid()
    
    