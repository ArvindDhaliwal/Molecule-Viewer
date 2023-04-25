import sqlite3
import MolDisplay
import os
import MolDisplay


class Database():

    conn = None  # will store Database connection to file

    def __init__(self, reset=False):
        if (reset == True and os.path.exists('molecules.db')==True ):  # does file need to be removed

            os.remove('molecules.db')

        self.conn = sqlite3.connect('molecules.db')  # store database connection to file
        self.c = self.conn.cursor() #used later for easier syntax
        self.c.execute('PRAGMA foreign_keys = ON') #turn on foreign keys 
        self.conn.commit() 
        self.Anum = 0
        self.Bnum = 0

    def create_tables(self):

        self.c.execute("""CREATE TABLE IF NOT EXISTS Elements(
                    ELEMENT_NO integer NOT NULL,
                    ELEMENT_CODE varchar(3) NOT NULL PRIMARY KEY,
                    ELEMENT_NAME varchar(32) NOT NULL,
                    COLOUR1 char(6) NOT NULL,
                    COLOUR2 char(6) NOT NULL,
                    COLOUR3 char(6) NOT NULL,
                    RADIUS decimal(3) NOT NULL
                    );
                    """)

        self.c.execute("""CREATE TABLE IF NOT EXISTS Atoms(
                    ATOM_ID integer PRIMARY KEY AUTOINCREMENT,
                    ELEMENT_CODE varchar(3) NOT NULL ,
                    X decimal(7,4) NOT NULL,
                    Y decimal(7,4) NOT NULL,
                    Z decimal(7,4) NOT NULL,
                    FOREIGN KEY(ELEMENT_CODE)  REFERENCES Elements(ELEMENT_CODE)
                    );
                    """)
        self.c.execute("""CREATE TABLE IF NOT EXISTS Bonds(
                    BOND_ID integer PRIMARY KEY AUTOINCREMENT,
                    A1 integer NOT NULL,
                    A2 integer NOT NULL,
                    EPAIRS integer NOT NULL
                    );
                    """)
        self.c.execute("""CREATE TABLE IF NOT EXISTS Molecules(
                    MOLECULES_ID integer PRIMARY KEY AUTOINCREMENT,
                    NAME text NOT NULL UNIQUE
                    )
                    """)
        self.c.execute("""CREATE TABLE IF NOT EXISTS MoleculeAtom(
                    MOLECULES_ID integer  NOT NULL,
                    ATOM_ID integer  NOT NULL,
                    PRIMARY KEY (MOLECULES_ID, ATOM_ID),
                    FOREIGN KEY(MOLECULES_ID)  REFERENCES molecules(MOLECULES_ID),
                    FOREIGN KEY(ATOM_ID)  REFERENCES Atoms(ATOM_ID)
                    )
                    """)
        self.c.execute("""CREATE TABLE IF NOT EXISTS MoleculeBond(
                    MOLECULES_ID integer,
                    BOND_ID integer,
                    PRIMARY KEY (MOLECULES_ID, BOND_ID),
                    FOREIGN KEY(MOLECULES_ID)  REFERENCES molecules(MOLECULES_ID),
                    FOREIGN KEY(BOND_ID)  REFERENCES Bonds(BOND_ID)
                    )
                    """)

        self.conn.commit()

    def __setitem__(self, table, values):
        #get total Colums in table
        H=len(values)
        i=0
        COL='?'
        while (i<H-1):
            COL+=',?'
            i=i+1

        #f used to denote a formated string literal(can add values directly with {})
        self.c.execute(f"INSERT INTO {table} VALUES ({COL});",tuple(values))
        self.conn.commit()
        
    def add_atom(self, molname, atom):
        #add atom into Atoms table
        self.c.execute("INSERT INTO Atoms (ELEMENT_CODE,X,Y,Z) VALUES(:ECODE,:X,:Y,:Z)", {
                       'ECODE': atom.element, 'X': atom.x, 'Y': atom.y, 'Z': atom.z})
        self.conn.commit()

        self.c.execute("SELECT * FROM Atoms ORDER BY ATOM_ID DESC LIMIT 1")
        Lrow = self.c.fetchone()
        ATOM = Lrow[0]

        #add value inot MoleculeAtom table
        self.c.execute("INSERT INTO MoleculeAtom VALUES(:MOLID,:ATOMID)", {
                       'MOLID': self.Anum, 'ATOMID': ATOM})
        self.conn.commit()

    def add_bond(self, molname, bond):
        #add bond into Bonds table
        self.c.execute("INSERT INTO Bonds (A1,A2,EPAIRS) VALUES(:A1,:A2,:EPAIRS)", {
                       'A1': bond.a1, 'A2': bond.a2, 'EPAIRS': bond.epairs})
        self.conn.commit()

        self.c.execute("SELECT * FROM Bonds ORDER BY BOND_ID DESC LIMIT 1")
        Lrow = self.c.fetchone()
        BOND = Lrow[0]

        #add value inot MoleculeBond table
        self.c.execute("INSERT INTO MoleculeBond VALUES(:MOLID,:BONDID)", {
                       'MOLID': self.Bnum, 'BONDID': BOND})
        self.conn.commit()

    def add_molecule(self, name, fp):

        mm = MolDisplay.Molecule()  # create molecule object
        mm.parse(fp)  # parse inputed file
        self.c.execute(
            "INSERT INTO Molecules (NAME) VALUES (:name)", {'name': name})
        self.conn.commit()
        self.Anum = self.Anum+1
        self.Bnum = self.Bnum+1
        i = 0
        while i < mm.atom_no:
            self.add_atom(name, mm.get_atom(i))
            i = i+1
            
        i = 0
        while i < mm.bond_no:
            self.add_bond(name, mm.get_bond(i))
            i = i+1
            
    def load_mol(self, name):

        mm = MolDisplay.Molecule()

        #get numebr form molecule
        self.c.execute(
            "SELECT * FROM Molecules WHERE Molecules.NAME=?", (name,))
        NUM = self.c.fetchone()[0]

        #join tables
        self.c.execute("""SELECT *
        FROM Molecules 
        INNER JOIN MoleculeAtom 
        ON Molecules.MOLECULES_ID=MoleculeAtom.MOLECULES_ID
        INNER JOIN Atoms 
        ON MoleculeAtom.ATOM_ID=Atoms.ATOM_ID
        WHERE Molecules.MOLECULES_ID = ?""", (NUM,))
        Array = self.c.fetchall()
        
        #get values and append atom
        k = Array.__len__()
        i = 0
        while (i < k):
            mm.append_atom(Array[i][5], Array[i][6], Array[i][7], Array[i][8])
            i = i+1

        #join tables
        self.c.execute("""SELECT*
        FROM Molecules 
        INNER JOIN MoleculeBond 
        ON Molecules.MOLECULES_ID=MoleculeBond.MOLECULES_ID
        INNER JOIN Bonds 
        ON MoleculeBond.BOND_ID=Bonds.BOND_ID
        WHERE Molecules.MOLECULES_ID = ?""", (NUM,))
        Array2 = self.c.fetchall()
        k2 = Array2.__len__()
        i = 0
        #get values and append bonds
        while (i < k2):
            mm.append_bond(Array2[i][5], Array2[i][6], Array2[i][7])
            i = i+1
        return mm
    
    def radius(self):
        #obtain the number of rows and create a radius dictionary
        self.c.execute("SELECT * FROM Elements")
        Array = self.c.fetchall()
        k = Array.__len__()

        i = 0
        radius = {}
        while (i < k):
            radius[Array[i][1]] = Array[i][6]
            i = i+1

        return radius

    def element_name(self):
        #obtain the number of rows and create a element_name dictionary
        self.c.execute("SELECT * FROM Elements")
        Array = self.c.fetchall()
        k = Array.__len__()

        i = 0
        element_name = {}
        while (i < k):
            element_name[Array[i][1]] = Array[i][2]
            i = i+1

        return element_name

    def radial_gradients(self):
        #get number of rows and create necessary amount of radialGradientSVG strings
        self.c.execute("SELECT * FROM Elements")
        Array = self.c.fetchall()
        k = Array.__len__()
        i = 0
        radialGradientSVG="""<svg version="1.1" width="2000" height="2000"
        xmlns="http://www.w3.org/2000/svg">"""
        while (i < k):
            radialGradientSVG = radialGradientSVG + """
            <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
                <stop offset="0%%" stop-color="#%s"/>
                <stop offset="50%%" stop-color="#%s"/>
                <stop offset="100%%" stop-color="#%s"/>
            </radialGradient>""" % (Array[i][2], Array[i][3], Array[i][4], Array[i][5])

            i = i+1
        return radialGradientSVG