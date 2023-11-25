
## Ensure code is imported in path
import sys
from pathlib import Path
CODEDIR = str(Path(__file__).resolve().parent.parent )+ "/src/"
sys.path.append(CODEDIR)
DATADIR = str(Path(__file__).resolve().parent )+ "/data/"
RESDIR = str(Path(__file__).resolve().parent )+ "/results/"

from prometry import pdbloader as pl
from prometry import pdbgeometry as pg
from prometry import reportmaker as rm
import numpy as np

pdbs =  ['6zx4','3u7z','6vb2']
pobjs = []

print("---")
for pdb in pdbs:    
    pla = pl.PdbLoader(pdb,DATADIR,cif=True)    
    po = pla.load_pdb()
    print(po,len(po.lines()))
    print("---")
    pobjs.append(po)
   #for line in po.lines(atoms=False):
   #     print(line)

gm = pg.GeometryMaker(pobjs)
df = gm.calculateGeometry(['C:N+1','C:O'])
df = df.loc[(df['C:N+1'] < 5)]
print(df.columns)
rep = rm.ReportMaker("Testing LeucipPy",RESDIR+"test_leu10.html",remove_strip=False)
rep.addPlot1d(df,'histogram','C:N+1',hue='rid',title='Hist')
rep.addPlot1d(df,'histogram','C:N+1',hue='aa',title='Hist')
rep.addPlot1d(df,'histogram','C:N+1',hue='bf_C:N+1',title='Hist')
rep.changeColNumber(3)

rep.addPlot2d(df,'scatter',geo_x='C:N+1',geo_y='C:O',hue='bf_C:N+1',title='Hist')
np1 = np.array([[1,2,3],[2,3,4],[3,2,1]])
rep.addSurface(np1)
np2 = np.array([[1,2,3,2],[0,0,1,1],[2,0,4,4],[3,2,1,1]])
rep.addContours(np2,overlay=True,colourbar=False)
rep.addPoints2d([[1,1],[2,2]],overlay=False)

df2 = df.groupby(['aa'])['aa'].count().reset_index(name='count')
rep.addPlotPi(df2,'count',hue='aa',title='plot title for aa',percent=True)   

df3 = df2.loc[(df2['aa'] == 'CYS')]
print(df3)
col_dic = {"CYS":"blue"}
rep.addPlotPi(df3,'count',hue='aa',title='plot title for aa',colors=['blue'])   

rep.changeColNumber(4)
rep.addPlot2d(df,'barplot',geo_x='chain',geo_y='C:O',title='Hist',hue='C:O',palette='r')
rep.addPlot2d(df2,'barplot',geo_x='aa',geo_y='count',title='Hist',hue='count')


rep.addPlot2d(df2,'seaborn',geo_x='aa',geo_y='count',title='Hist',hue='count')


#rep.addSeries(df['C:N+1'].describe(),'C:N+1', transpose=True)
#df = df.sort_values(by='C:N+1',ascending=True)
#rep.addDataFrame(df,'C:N+1')
#rep.addPlotPi(df,'C:N+1','aa','me')

rep.printReport()




    


