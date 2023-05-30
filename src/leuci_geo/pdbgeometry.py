# !/usr/bin/python3
"""
GeoDataFrame (LeucipPy.GeoDataFrame))
------------------------------------------------------
This class manipulates given biopython structures and creates dataframes oft he geometry
"""

from operator import itemgetter
import pandas as pd
from . import pdbobject as po
from . import geocalculator as calc
from leuci_xyz import vectorthree as v3


class GeometryMaker:
    def __init__(self,pobjs,log=0,exc_hetatm=True):
        """Initialises a GeoDataFrame with the list of biopython structures

        :param biopython_structures: A list of structures that has been created from biopython
        """
        self.pobjs = pobjs
        self.exc_hetatm = exc_hetatm
        self.log = log
        
              
    def calculateGeometry(self,geos,hues=['pdb_code','resolution','chain','aa-1','aa','aa+1','id','rid','ridx','avgrid','avgridx','bfactor','avgbfactor','occupancy','info'],log=0):
        """Creates the geoemtry from the structures in the class

        :param geos: A list of geometric measures to calculate in the format 2,3 or 4 atoms for distance, angle or dihedral, e.g. 'N:CA', 'N:CA:C', or 'N:CA:C:N+1'
        :param hues:A list of hues hat will associate with the geoemtric values, can be bfactor, amino acid (aa), residue number (rid) etc see docs
        :returns: the pandas dataframe with a r per geoemtric calculation per residue wh columns of geoemtric measures and hues
        """

        vals = []
        used_hues = []
        for geo in geos:
            hues.append('info' + geo)

        count = 1
        for geopdb in self.pobjs:
            hue_pdb = geopdb.pdb_code
            if log > 0:
                print('LeucipPy(1) df calc for ' + hue_pdb, count, '/', len(self.pobjs))
                count += 1

            hue_res = geopdb.resolution
            ridx = 1
            for chain, res in geopdb.chains.items():
                for rid, resd in res.items():
                    avg_bfactor = 0
                    bfactor = 0
                    avg_occupancy = 0
                    avg_rid = 0
                    avg_ridx = 0
                    num_atoms = 0
                    hue_aa = resd.amino_acid
                    tuplerow = []
                    aam1 = ''
                    aap1 = ''
                    refatom = None
                    if len(resd.atoms) > 0 and 'CA' in resd.atoms:
                        refatom = resd.atoms['CA']

                    all_geos_ok = True
                    all_hues = {}
                    for geo in geos:
                        geo_as_atoms = self.geoToAtoms(geo)
                        ok,val,bfac,avgbfac,occ,rno, rnox,num,refatom,other = self.calculateOneGeometry(geopdb,chain,rid,geo_as_atoms,log)
                        avg_bfactor += avgbfac
                        avg_occupancy += occ
                        avg_rid += rno
                        avg_ridx += rnox
                        num_atoms += num
                        if bfactor == 0:
                            bfactor = bfac
                        if ok:
                            tuplerow.append(val)
                            all_hues['info' + geo] = other

                            geosaa = geo.split(':')
                            infosaa = other.split('_')
                            for i in range(0,len(geosaa)):
                                geoaa = geosaa[i]
                                if 'CA+1' == geoaa or 'N+1' == geoaa or 'C+1' == geoaa or 'O+1' == geoaa:
                                    aap1 = infosaa[i][:3]
                                if 'CA-1:' == geoaa or 'N-1' == geoaa or 'C-1' == geoaa or 'O-1' == geoaa:
                                    aam1 = infosaa[i][:3]

                        else:
                            all_geos_ok = False
                    #Append hues
                    if all_geos_ok:#we are only adding complete rows
                        all_hues['pdb_code'] =hue_pdb
                        all_hues['resolution'] =hue_res
                        all_hues['chain'] = chain
                        all_hues['aa'] =hue_aa
                        all_hues['aa+1'] = aap1
                        all_hues['aa-1'] = aam1
                        all_hues['avgrid'] = avg_rid/ num_atoms
                        all_hues['avgridx'] =avg_ridx/ num_atoms
                        all_hues['rid'] = rid
                        all_hues['ridx'] = resd.ridx
                        all_hues['avgbfactor'] =avg_bfactor / num_atoms
                        all_hues['bfactor'] = bfactor
                        all_hues['occupancy'] =avg_occupancy / num_atoms
                        used_hues = []
                        for hue in hues:
                            if hue in all_hues and hue not in used_hues:
                                used_hues.append(hue)
                                tuplerow.append(all_hues[hue])
                        # TODO special optional hue of type aa-1:aa:aa+1
                        vals.append(tuplerow)
                    ridx += 1

        geos2 = []
        for geo in geos:
            geos2.append(geo)

        geos2.extend(used_hues)
        df = pd.DataFrame(vals,columns=geos2)
        return df

    def geoToAtoms(self, geo):
        """Converts a single geo to the residue and atoms reuired
        """

        geo_atoms = []
        geo_split = geo.split(':')
        for g in geo_split:
            ref=0
            if '+' in g:
                g_split = g.split('+')
                g_atom = g_split[0]
                ref = int(g_split[1])
            elif '-' in g:
                g_split = g.split('-')
                g_atom = g_split[0]
                ref = int(g_split[1]) * -1
            else:
                g_atom = g
            geo_atoms.append([g_atom,ref])
        return geo_atoms

    def calculateData(self,hues=['pdb_code','resolution','chain','aa','rid','ridx','atom_no','atom_name','element','bfactor','occupancy','x','y','z'],log=0):
        """Creates the geoemtry from the structures in the class

        :param geos: A list of geometric measures to calculate in the format 2,3 or 4 atoms for distance, angle or dihedral, e.g. 'N:CA', 'N:CA:C', or 'N:CA:C:N+1'
        :param hues:A list of hues hat will associate with the geoemtric values, can be bfactor, amino acid (aa), residue number (rid) etc see docs
        :returns: the pandas dataframe with a r per geoemtric calculation per residue wh columns of geoemtric measures and hues
        """

        vals = []
        count = 1
        used_hues = []
        for geopdb in self.bio_strucs:
            pdb = geopdb.pdb_code
            if log > 0:
                print('LeucipPy(1) df calc for ' + pdb, count,'/',len(self.bio_strucs))
                count += 1
            reso = geopdb.resolution

            for chain, res in geopdb.chains.items():
                for rid, resd in res.items():
                    aa = resd.amino_acid
                    for nm,atm in resd.atoms.items():
                        tuplerow = []
                        all_hues = {}
                        all_hues['pdb_code'] =pdb
                        all_hues['resolution'] =reso
                        all_hues['chain'] = chain
                        all_hues['aa'] =aa
                        all_hues['rid'] = resd.rid
                        all_hues['ridx'] =resd.ridx
                        all_hues['atom_no'] = atm.atom_no
                        all_hues['atom_name'] = atm.atom_name
                        all_hues['element'] = atm.atom_type
                        all_hues['bfactor'] =atm.bfactor
                        all_hues['occupancy'] =atm.occupancy
                        all_hues['x'] = atm.x
                        all_hues['y'] = atm.y
                        all_hues['z'] = atm.z
                        used_hues = []
                        for hue in hues:
                            if hue in all_hues:
                                used_hues.append(hue)
                                tuplerow.append(all_hues[hue])
                        vals.append(tuplerow)
        df = pd.DataFrame(vals,columns=used_hues)
        return df

    def filterDataFrame(self,data, inclusions={},exclusions={}):
        df = data
        for ky,vls in inclusions.items():
            df = df[df[ky].isin(vls)]

        for ky,vls in exclusions.items():
            df = df[~df[ky].isin(vls)]
        return df

    def calculateOneGeometryX(self,pobj, chain, resno, geo_atoms,log=0):
        """Creates the geoemtry from the structure in the class for 1 geo

        :param chain: The chain id
        :param rid: The residue number
        :param geo_atoms: A list of tuples that is the atom, the displacement

        :returns: [bool,float,bfactor, occupancy, atoms, GeoAtom] a bool for if it could be calculated, and the value, and the reference atom
        """
        total_rid = 0
        total_ridx = 0
        other = ''
        is_nearest = False

        empty_return = [False, 0, 0, 0, 0, 0, 0, 0, None,'']

        rids = pobj.chains[chain]
        all_there = True
        atoms = []
        first = True
                        
        for atom,offset in geo_atoms:
            #print(atom,offset)
            #if '(' in atom and ')' in atom:
            #    atom = atom[1:len(atom) - 1]
            this_rid = resno + offset
            if False:#int(this_rid) not in rids:
                print('False')
                #print(this_rid, resno)
                #return False,0,0,0,0,0,0,None,''
            else:
                #rid = rids[this_rid]
                brackets = False
                elements = False
                if '{' in atom and '}' in atom:
                    #print(atom)
                    brackets = True
                elif '(' in atom and ')' in atom:
                    #print(atom)
                    brackets = True
                    elements = True

                if brackets and not first: #then we need to do a distance search first and iut must be the second atom
                    #print('dbg1', atom)
                    is_nearest = True
                    refatm = atoms[0]
                    atomlist = atom[1:len(atom) - 1]
                    nearest = 1
                    if "@" in atomlist:
                        #print('dbg1', atomlist)
                        ats = atomlist.split('@')
                        #print('dbg1',ats)
                        atomlist = ats[0]
                        nearest =ats[1]
                    else:
                        atomlist = atom[1:len(atom)-1]
                    atomlist = atomlist.split(',')
                    debugatomlist = atom[1:len(atom)-1].split(',')
                    last_atm = None
                    last_dis = 10000
                    last_other = ""
                    #for atmtype in atomlist:
                    dis,this_atm,other2 = self.getNearestAtom(pobj,refatm, resno,chain,atomlist,offset,nearest,log,elements)
                    if dis < last_dis:
                        last_atm = this_atm
                        last_dis = dis
                        last_other = other2

                    other += "_" + last_other
                    if last_other != "":
                        atoms.append(last_atm)
                    else:
                        if log > 1:
                            print('...LeucipPy(2) Not found',resno,chain,atomlist,offset,nearest)
                        return empty_return
                elif int(this_rid) not in rids:
                    #print(this_rid, resno)
                    return empty_return

                else:
                    rid = rids[this_rid]
                    if brackets:
                        atom = atom[1:len(atom) - 1]
                        isit, atom = pobj.elementInList(atom, rid.atoms)
                        if isit:
                            atm = rid.atoms[atom]
                            total_rid += rid.rid;
                            total_ridx += rid.ridx;
                            other += "_" + str(rid.amino_acid) + "|" + str(rid.rid) + str(chain) + "|" + atm.atom_name
                            atoms.append(atm)
                        else:
                            return empty_return
                    else:
                        if atom not in rid.atoms:
                            return empty_return
                        total_rid += rid.rid;
                        total_ridx += rid.ridx;
                        atm = rid.atoms[atom]
                        other += "_" + str(rid.amino_acid)  + "|" + str(rid.rid) + str(chain) + "|" + atm.atom_name
                        atoms.append(atm)

            first = False
        val = 0
        if len(atoms) == 2:
            if not is_nearest and atoms[0].atom_name == atoms[1].atom_name and atoms[0].atom_no == atoms[1].atom_no :#then we actually just want the distance magnitude of the single atom
                val = calc.getMagnitude(atoms[0].x,atoms[0].y,atoms[0].z)
            else:
                val = calc.getDistance(atoms[0].x, atoms[0].y, atoms[0].z,
                                       atoms[1].x, atoms[1].y, atoms[1].z)
        elif len(atoms) == 3:
            val = calc.getAngle(atoms[0].x, atoms[0].y, atoms[0].z,
                                atoms[1].x, atoms[1].y, atoms[1].z,
                                atoms[2].x, atoms[2].y, atoms[2].z)
        elif len(atoms) == 4:
            val = calc.getDihedral(atoms[0].x, atoms[0].y, atoms[0].z,
                                   atoms[1].x, atoms[1].y, atoms[1].z,
                                   atoms[2].x, atoms[2].y, atoms[2].z,
                                   atoms[3].x, atoms[3].y, atoms[3].z)

        total_bfactor = 0
        bfactor = 0
        total_occupancy = 0
        for atm in atoms:
            if bfactor == 0:
                bfactor = atm.bfactor
            total_bfactor += atm.bfactor
            total_occupancy  += atm.occupancy



        return True, val, bfactor,total_bfactor, total_occupancy, total_rid, total_ridx, len(atoms), atoms[0],other[1:]
    
    ###### MODICFIED VERSION ########
    def calculateOneGeometry(self,pobj, chain, resno, geo_atoms,log=0):
        """Creates the geoemtry from the structure in the class for 1 geo

        :param chain: The chain id
        :param rid: The residue number
        :param geo_atoms: A list of tuples that is the atom, the displacement

        :returns: [bool,float,bfactor, occupancy, atoms, GeoAtom] a bool for if it could be calculated, and the value, and the reference atom
        """
        total_rid = 0
        total_ridx = 0
        other = ''
        is_nearest = False

        empty_return = [False, 0, 0, 0, 0, 0, 0, 0, None,'']

        rids = pobj.chains[chain]
        all_there = True
        atoms = []
        atom_groups = []

        first_atoms = self.getMatchingStartAtoms(pobj, chain, resno,geo_atoms[0])
        first_atoms = self.getMatchingStartAtoms(pobj, chain, resno,geo_atoms[0])
        print(len(first_atoms))
        for chain, residue,atom in first_atoms:
            atom_group = []
            atom_group.append((chain, residue,atom))
            print("FIRST ATOM=",chain,residue,atom)
            for i in range(1,len(geo_atoms)):                
                candidate_atoms, nearest,criteria = self.getMatchingAtoms(pobj, resno, chain, residue,atom, geo_atoms[i])
                #candidate_atoms = self.applyCriteria()
                if len(candidate_atoms) > 0:
                    best_atom = self.getNearestAtomMatch(pobj, atom, candidate_atoms, nearest,criteria)
                    #for chain_m, residue_m,atom_m in candidate_atoms:
                    #    print("CANDIDATE=",chain_m, residue_m,atom_m)
                    print("BEST=",chain, residue,str(best_atom[1]))
                    atom_group.append(best_atom)
                else:
                    continue
            atom_groups.append(atom_group)
        
        for atoms in atom_groups:
            val = 0
            if len(atoms) == 2:                
                val = calc.getDistance(atoms[0][2].x, atoms[0][2].y, atoms[0][2].z,
                                        atoms[1][0][2].x, atoms[1][0][2].y, atoms[1][0][2].z)
            elif len(atoms) == 3:
                val = calc.getAngle(atoms[0][2].x, atoms[0][2].y, atoms[0][2].z,
                                    atoms[1][0][2].x, atoms[1][0][2].y, atoms[1][0][2].z,
                                    atoms[2][0][2].x, atoms[2][0][2].y, atoms[2][0][2].z)
            elif len(atoms) == 4:
                val = calc.getDihedral(atoms[0][2].x, atoms[0][2].y, atoms[0][2].z,
                                    atoms[1][0][2].x, atoms[1][0][2].y, atoms[1][0][2].z,
                                    atoms[2][0][2].x, atoms[2][0][2].y, atoms[2][0][2].z,
                                    atoms[3][0][2].x, atoms[3][0][2].y, atoms[3][0][2].z)

            else:
                print("???")
            total_bfactor = 0
            bfactor = 0
            total_occupancy = 0
            for atm in atoms:
                if bfactor == 0:
                    bfactor = 1
                total_bfactor += 1
                total_occupancy  += 1



            return True, val, bfactor,total_bfactor, total_occupancy, total_rid, total_ridx, len(atoms), atoms[0],other[1:]


        return empty_return
        
        
    
    def getMatchingStartAtoms(self,pobj, chain, resno,geo_atom):
        
        atom_starts = []
        criteria = ""

        if "[" in geo_atom[0] and "]" in geo_atom[0]:
            al = geo_atom[0].split("[")
            geo_atom[0] = al[0]
            criteria = al[1][:-1]

        if "{" in geo_atom[0] and "}" in geo_atom[0]:
            atom_list = geo_atom[0][1:-1]
            print(atom_list)
            atom_list = atom_list.split(",")
        else:
            atom_list = [geo_atom[0]]

        for geo_a in atom_list:
        
            atom_type = ""
            atom_name = ""
            if "(" in geo_a and ")" in geo_a:
                atom_type = geo_a[1]
            else:
                atom_name = geo_a
            res_match = resno + geo_atom[1]
            
            for chain,resdic in pobj.chains.items():
                for no,res in resdic.items():
                    if res.rid == res_match:
                        for attype,atm in res.atoms.items():
                            if atm.matchesCriteria(chain,res,criteria):
                                if atom_type != "" and atm.atom_type == atom_type:
                                    atom_starts.append((chain,res,atm))
                                elif atom_name != "" and atm.atom_name == atom_name:
                                    atom_starts.append((chain,res,atm))
                        break
        
        return atom_starts
    
    def getMatchingAtoms(self,pobj, resno,chain, res,atom, geo_atom):
        
        atom_matches = []
        criteria = ""

        if "[" in geo_atom[0] and "]" in geo_atom[0]:
            al = geo_atom[0].split("[")
            geo_atom[0] = al[0]
            criteria = al[1][:-1]

        nearest = 0
        if "{" in geo_atom[0] and "}" in geo_atom[0]:
            atom_list = geo_atom[0][1:-1]
            if "@" in atom_list:                        
                ats = atom_list.split('@')                
                atom_list = ats[0]
                nearest = ats[1]                    
            #print(atom_list)
            atom_list = atom_list.split(",")
        else:
            atom_list = [geo_atom[0]]
        
        for geo_a in atom_list:
            atom_type = ""
            atom_name = ""
            if "(" in geo_a and ")" in geo_a:
                atom_type = geo_a[1]
            else:
                atom_name = geo_a
            
            res_match = resno + geo_atom[1]
            
            for chain,resdic in pobj.chains.items():
                for no,res in resdic.items():
                    if res.rid == res_match:
                        for attype,atm in res.atoms.items():
                            if atom_type != "" and atm.atom_type == atom_type:
                                atom_matches.append((chain,res,atm))
                            elif atom_name != "" and atm.atom_name == atom_name:
                                atom_matches.append((chain,res,atm))
                        break
            
        return atom_matches, nearest,criteria

    def getNearestAtomMatch(self, pobj, atom, candidate_atoms, nearest,criteria):             
        disses = []
        va = v3.VectorThree(float(atom.x),float(atom.y),float(atom.z))
                
        for chain_m, residue_m,atom_m in candidate_atoms:            
            vc = v3.VectorThree(float(atom_m.x),float(atom_m.y),float(atom_m.z))            
            val = va.distance(vc)            
            if atom_m.matchesCriteria(chain_m,residue_m,criteria):
                disses.append(((chain_m, residue_m,atom_m),val))
        
        # now sort on the values
        sorted_disses = sorted(disses,key=itemgetter(1))
        if nearest < len(sorted_disses):
            return sorted_disses[nearest]
        else:
            return sorted_disses[-1]



    
    def getNearestAtom(self,pobj,refatm, ref_rid,ref_chain,atmtypes,resmax,nearest,log=0,elements=False):
        if log > 1:
            print('LeucipPy(2) nearest:',atmtypes,"within res num=",resmax,"nearest=",nearest)
        dic_res = {}
        last_dis = 10000
        last_atom = None
        other = ''
        for chain,resdic in pobj.chains.items():
            for no,res in resdic.items():
                for attype,atm in res.atoms.items():
                    inlist = False
                    if elements:
                        if attype[:1] in atmtypes:
                            inlist=True
                        elif len(attype) > 1:
                            if attype[:2] in atmtypes:
                                inlist = True
                    else:
                        if attype in atmtypes:
                            inlist=True
                    if inlist:
                        distance = calc.getDistance(refatm.x, refatm.y,refatm.z,atm.x,atm.y,atm.z)
                        if (abs(int(no) - int(ref_rid)) >= int(resmax) or ref_chain != chain):
                            other = str(res.amino_acid) + "|" + str(no) + str(chain) + "|" + atm.atom_name
                            dic_res[distance] = [atm,other]
                            if log > 2:
                                print("LeucipPy(3) to dictionary", other)

                        #    last_dis = distance
                        #    last_atom = atm


        count = 1
        sorted_dic = dict(sorted(dic_res.items()))
        found = False
        for dis,st in sorted_dic.items():
            if log > 2:
                print("LeucipPy(3) nearest", count,nearest,round(dis,4),st[0].atom_name)
            if int(count) == int(nearest):
                last_dis = dis
                last_atom = st[0]
                other = st[1]
                found = True
                if log > 3:
                    print("...LeucipPy(4) found")
                break
            count +=1

        if found:
            #print("...LeucipPy return",last_dis,other)
            return last_dis,last_atom,other
        else:
            return 0, "", ""
                

