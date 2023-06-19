

######### TEST THE DATAFRAME ##############################

"""
Search criteria
method/refinement resolution < 1
Disulfide bond count >=1
Exp method x-ray


"""

pdbs = ["1AB1", "1AHO", "1CBN", "1DY5", "1EJG", "1ETL", "1ETM", "1ETN", "1F94", "1FN8", "1FY4", "1FY5", "1G4I", "1G66", "1G6X"]
pdbs.extend(["1GDN", "1GDQ", "1GQV", "1GVK", "1HJ9", "1HJE", "1IC6", "1IEE", "1JXT", "1JXU", "1JXW", "1JXX", "1JXY", "1K5C", "1KTH"])
pdbs.extend(["1L9L", "1MC2", "1OK0", "1P9G", "1PQ5", "1PQ7", "1SSX", "1V0L", "1V6P", "1VB0", "1VL9", "1X8P", "1X8Q", "1XVO", "1YWA", "1YWB", "1ZLB", "2AYW", "2B97"])

#pdbs.add(2BZZ, 2FMA, 2G58, 2H5C, 2H5D, 2IXT, 2NLS, 2PNE, 2PWA, 2V8B, 2VB1, 2VHK, 2VHR, 2VI3, 2VU6, 2XJH, 2XJP, 2XTT, 2XU3, 3AGN, 3AGO, 3C78
#pdbs.add(, 3D43, 3DW3, 3DWE, 3HGP, 3I2Y, 3I30, 3I37, 3LZT, 3M5Q, 3MFJ, 3MI4, 3NIR, 3ODV, 3PSM, 3Q8J, 3QPA, 3QPC, 3U7T, 3VLA, 3W7Y, 3WGE, 3WGX,
#pdbs.add(3WL2, 3WOU, 3X2H, 3X2L, 3X2M, 3X2P, 4A7U,4BCT, 4E3Y, 4F18, 4F19, 4F1U, 4F1V, 4HGU, 4I8G, 4I8H, 4I8J, 4I8K, 4I8L, 4LFS, 4LZT, 4M7G, 
#pdbs.add(4NDS, 4NSV, 4R5R, 4UNU, 4UYR, 4WKA, 4XDX, 4XOJ, 4Y9W, 4YEO, 4ZM7, 5A71, 5AVD, 5AVG, 5DJ7, 5DK1, 5DKM, 5E7W, 5E9N, 5HMV, 5HQI, 5I5B,
#pdbs.add(5II6, 5KWM, 5KXV, 5MB5, 5MN1, 5MNB, 5MNC, 5MNF, 5MNG, 5MNH, 5MNK, 5MNM, 5MNN, 5MNO, 5MON, 5MOP, 5MOQ, 5MOR, 5MOS, 5O0U, 5O2X, 5RBW, 
#pdbs.add(5RC2, 5RCB, 5SBQ, 5U3A, 5X9L, 5X9M, 6CNW, 6E6O, 6EQE, 6ETK, 6ETL, 6ETM, 6ETN, 6F1O, 6RGP, 6RHH, 6RHU, 6RHX, 6RI6, 6RI8, 6RII, 6RYG,
#pdbs.add(6SRY, 6SY3, 6SYE, 6TN1, 6YIV, 6YIW, 6ZSY, 7AEY, 7AF2, 7AVE, 7BCU, 7LTD, 7LTI, 7LTV, 7MBO, 7OL5, 7P4R, 7P6M, 7Q5G,7YRK]
print(len(pdbs),pdbs)
for i in range(len(pdbs)):
    pdbs[i] = pdbs[i].lower()


## Ensure code is imported in path
import sys
from pathlib import Path
CODEDIR = str(Path(__file__).resolve().parent.parent )+ "/src/"
sys.path.append(CODEDIR)
DATADIR = str(Path(__file__).resolve().parent )+ "/data/"

from leuci_geo import pdbloader as pl
from leuci_geo import pdbgeometry as pg


pobjs = []

print("---")
for pdb in pdbs:
    print("Loading",pdb)
    pla = pl.PdbLoader(pdb,DATADIR,cif=True)    
    po = pla.load_pdb()    
    pobjs.append(po)
    #for line in po.lines(atoms=True):
    #    print(line)
 
gm = pg.GeometryMaker(pobjs)

geos = ['SG:{SG@1}','SG:{(N),(O)}']
print("----- geos -----")
df = gm.calculateGeometry(geos,log=0)
print(df)

geos = ['SG:{SG@1}','SG:{(N),(O)}[dis|<3]','SG:{(N),(O)}:{SG@1}']
print("----- geos -----")
df = gm.calculateGeometry(geos,log=0)
print(df)

print(df[['SG:{(N),(O)}:{SG@1}','info_SG:{(N),(O)}:{SG@1}']])

# reduce range to < 2 angle
df2 = df.loc[(df['SG:{(N),(O)}:{SG@1}'] < 2) & (df['bf_SG:{(N),(O)}:{SG@1}'] < 10)  & (df['occ_SG:{(N),(O)}:{SG@1}'] == 1) ]
print(df2)

coords_list = []
for i, row in df2.iterrows():
    pdb_code = row['pdb_code']
    atoms = row['info_SG:{(N),(O)}:{SG@1}']    
    clp = atoms.split("(")    
    cen = clp[1][:-1]
    lin = clp[2][:-1]
    pla = clp[3][:-1]
    cens = cen.split("|")
    lins = lin.split("|")
    plas = pla.split("|")
    #central_atom = "A:707@C.A"
    cen_str = cens[0]+":"+cens[2]+"@"+cens[3]+".A"
    lin_str = lins[0]+":"+lins[2]+"@"+lins[3]+".A"
    pla_str = plas[0]+":"+plas[2]+"@"+plas[3]+".A"
    
    coords_list.append((pdb_code,cen_str,lin_str,pla_str))

print(coords_list)
    
    



