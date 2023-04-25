import molecule


# header = """<svg version="1.1" width="1000" height="1000"
# xmlns="http://www.w3.org/2000/svg">"""

footer = """</svg>"""

offsetx = 500

offsety = 500

#Used in Molecule class
class Atom():

    def __init__(self, c_atom):
        self.z = c_atom.z
        self.atom = c_atom

    def __str__(self): #for debugging only
        return "element={a},x={b:f} y={c:f} z={d:f}".format(a=self.atom.element,b=self.atom.x, c=self.atom.y,d=self.z)
    

    def svg(self):
        #write svg line
        x = (self.atom.x*100)+offsetx
        y = (self.atom.y*100)+offsety
        rad = radius[self.atom.element]
        colour = element_name[self.atom.element]
        H = ' <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (
            x, y, rad, colour)
        return H

#Used in Molecule class
class Bond():

    def __init__(self, c_bond):
        self.z = c_bond.z
        self.bond = c_bond

    def __str__(self):  #for debugging only
        print('new atom')
        print('a1.x1='+str(self.bond.x1)+' a1.y1='+str(self.bond.y1) +
              'a2.x1='+str(self.bond.x2)+' a2.y2='+str(self.bond.y2))
        print('bond.dx='+str(self.bond.dx)+' bond.dy='+str(self.bond.dy))
        print('len=' + str(self.bond.len) + ' z value' + str(self.z))

    def svg(self):
        #write svg line
        xa = (self.bond.x1*100)+offsetx-(self.bond.dy*10)
        ya = (self.bond.y1*100)+offsety-(self.bond.dx*10)

        xb = (self.bond.x1*100)+offsetx+(self.bond.dy*10)
        yb = (self.bond.y1*100)+offsety+(self.bond.dx*10)

        xc = (self.bond.x2*100)+offsetx-(self.bond.dy*10)
        yc = (self.bond.y2*100)+offsety-(self.bond.dx*10)

        xd = (self.bond.x2*100)+offsetx+(self.bond.dy*10)
        yd = (self.bond.y2*100)+offsety+(self.bond.dx*10)
        #coordinate order MATTERS
        H = ' <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (
            xb, ya, xa, yb, xc, yd, xd, yc)
        return H

#helper funtion
def JoinString(s):
    return ' '.join(s.split())


class Molecule(molecule.molecule):
    
    def __str__(self): #for debugging
        for i in range(self.atom_no):
            A = Atom(self.get_atom(i))
            #A.__str__()
            return "element={a},x={b:f} y={c:f} z={d:f}".format(a=A.atom.element,b=A.atom.x, c=A.atom.y,d=A.z)
        # for i in range(self.bond_no):
        #     B = Bond(self.get_bond(i))
        #     B.__str__()
    def svg(self):

        #create new array to merger 2 SORTED arrays
        Ap = header 
        res = []
        i, j = 0, 0

        #Loop until one Array is empty
        while i < self.atom_no and j < self.bond_no:
            if self.get_atom(i).z < self.get_bond(j).z:
                res.append(self.get_atom(i))
                A = Atom(self.get_atom(i))
                append = A.svg()
                Ap += append
                i += 1
            else:
                res.append(self.get_bond(j))
                B = Bond(self.get_bond(j))
                append = B.svg()
                Ap += append
                j += 1
                
        #add remaining vlaues         
        while i < self.atom_no:
            res.append(self.get_atom(i))
            A = Atom(self.get_atom(i))
            append = A.svg()
            Ap += append
            i += 1
        while j < self.bond_no:
            res.append(self.get_bond(i))
            B = Bond(self.get_bond(j))
            append = B.svg()
            Ap += append
            j += 1
        Ap += footer

        return Ap

    def parse(self, f):
        for i in range(3):  # skip first 3 lines
            f.readline()

        #read and strip first line, then split at space to create a array
        first_line = JoinString(f.readline().strip())
        first_line_array = first_line.split(' ')
        atom_m = int(first_line_array[0])
        bond_m = int(first_line_array[1])

        for i in range(atom_m):  # parse through atoms
            atom_line = JoinString(f.readline().strip())
            atom_line_array = atom_line.split(' ')

            self.append_atom(atom_line_array[3], float(atom_line_array[0]), float(atom_line_array[1]), float(atom_line_array[2]))
            
        for i in range(bond_m):  # parse through bonds
            bond_line = JoinString(f.readline().strip())
            bond_line_array = bond_line.split(' ')

            self.append_bond(int(bond_line_array[0])-1, int(bond_line_array[1])-1, int(bond_line_array[2]))
            #-1 for a1 and a2
