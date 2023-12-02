import streamlit as st


st.set_page_config(
        page_title="prometry",
        page_icon="app/static/plot.png",
        layout="wide",
    )

st.header("Prometry - Documentation and help")

st.write("### Restrictions")
st.write("""
        The data is restricted to only those atoms that make a reasonable contribution to the protein geoemtry. 
        Atoms with occupancy less than 1 and atoms that are part of a set of possible mutation locations are excluded automatically.

        The data is not automatically restricted to standard amino acids - HOH, HM8 and any other HETAMS are included by default. 
        HETATMs can be excluded explicitly, or the 20 standard amino acids can be specified explicitly with the criterion aa|20
        """)

st.write("### Geo definitions")
st.code("""
        ---------------------------------------------------------------------       
        Examples
        ---------------------------------------------------------------------  
        Lengths in the backbone: N:CA CA:C C:N+1 C:O  
        Backbone angle tau: N:CA:C  
        Phi and psi : C-1:N:CA:C and N:CA:C:N+1                  
        The carbonyl oxygen and the nearest N to it that is not in the same residue: O:(N&1) 
        The disulfide bonds (or nearest cysteine sulphurs): SG:(SG&1)  
        Any O or N within 2.5-3 of the N but not the same residue: N:{(O),(N)@1}[dis|2.5<>3.0]
        The second nearest O or N: N:(N,O@1)
        The nearest O or N not the same residue: N:{N,O&1}
        Only glycine: N[aa|GLY]:CA
        Never water: N:(O)[~aa|HOH]
        Only glycine TO glycine:  N[aa|GLY]:CA[aa|GLY]
        Contacts CA-CA between 0.5 and 6: CA:{CA@i}[dis|0.5<>6]
        ---------------------------------------------------------------------  
        Description
        ---------------------------------------------------------------------  
        With no brackets or symbols, the simple case is that you are looking for atom types within a residue  
        N:CA - is looking for all atoms of type N and the CA in the same residue, for the distance  
        N:CA:C - is looking for all atoms of types N, CA and C in the same residue and the angle  

        +/- look for neighbouring residues
        C:N+1 - looks for the C in a residue and the N in the next residue  
        C-1:N - as per above but the previous residue to the current""")
        
st.write("### Criteria and searches")
st.code("""---------------------------------------------------------------------  
        () brackets symbolise element rather than atom type, eg N can mean NZ, NE1 etc, and this starts a 
        nearest lookup if it is not the first item, or a cross product if it is
        (N):N - means any type N, and the N in the same residue - there can be more than 1 per residue
        N:(N) - means all N's in a reside and the nearest type N in the same residue - only 1 per residue
        ---------------------------------------------------------------------  
        {} symbolise distance searchers - the list of atoms is all the candidates
        N:{O,N} is all N's in a residue and the nearest O or N to it - 1 per residue
        ---------------------------------------------------------------------  
        () brackets can be used
        N:{(O),(N)} is all N's in a residue and the nearest O type or N type to it - 1 per residue
        ---------------------------------------------------------------------  
        operators @ or & specify x nearest or at least x away as follows
        N:{O,N@1} means N and the second nearest  O or N to it - 0 indexed
        N:{O,N&2} means N and the nearest O or N as long as it is at least 2 residues away
        CA:{CA@i} i means all CAs so it is CA with all possible CAs.
        ---------------------------------------------------------------------  
        [] after a geo specify a comma delim list of criteria
        aa - amino acid of the residue
        dis - distance from the first atom where
        < less than
        > greater than
        <> between
        >< extremes
        occ - occupancy, with just =, < or >
        ---------------------------------------------------------------------  
    """)