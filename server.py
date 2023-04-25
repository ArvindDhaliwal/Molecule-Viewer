import io
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import MolDisplay
import molsql
import urllib
import molecule


# allow user to upload file

db = molsql.Database(True)
db.create_tables()

db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 );
db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/homepage.html":
            self.send_response(200)  # OK
            f = open('homepage.html', 'r')
            home = f.read()
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(home))
            self.end_headers()
            self.wfile.write(bytes(home, "utf-8"))
            f.close()

        elif self.path == "/homepage2.html":
            self.send_response(200)  # OK
            self.send_header("Content-type", "text/html")
            # self.send_header( "Content-length", len(home) );
            self.end_headers()
            with open('homepage2.html', 'rb') as f:
                self.wfile.write(f.read())

        elif self.path == "/homepage3.html":

            self.send_response(200)  # OK
            self.send_header("Content-type", "text/html")
            # self.send_header( "Content-length", len(home) );
            self.end_headers()
            with open('homepage3.html', 'rb') as f:
                self.wfile.write(f.read())

        elif self.path == "/homepage4.html":

            self.send_response(200)  # OK
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open('homepage4.html', 'rb') as f:
                self.wfile.write(f.read())

        elif self.path == "/HPstyle.css":
            self.send_response(200)  # OK
            print("css")
            f = open('HPstyle.css', 'r')
            home = f.read()
            self.send_header("Content-type", "text/css")
            self.send_header("Content-length", len(home))
            self.end_headers()
            self.wfile.write(bytes(home, "utf-8"))
            f.close()

        elif self.path == "/JavaScript.js":
            self.send_response(200)  # OK
            print("css")
            f = open('JavaScript.js', 'r')
            home = f.read()
            self.send_header("Content-type", "text/js")
            self.send_header("Content-length", len(home))
            self.end_headers()
            self.wfile.write(bytes(home, "utf-8"))
            f.close()

        elif self.path == "/createbutton":
            self.send_response(200)  # OK

            db.c.execute("SELECT * FROM Molecules")
            t = db.c.fetchall()
            result = ""
            for item in t:

                k = str(item[1])

                result = result+k+','

                db.c.execute(
                    "SELECT * FROM MoleculeBond WHERE MOLECULES_ID=?", (item[0],))
                BOND = db.c.fetchall()
                B = len(BOND)
                B_D = str(B)
                result = result+B_D+','
                db.c.execute(
                    "SELECT * FROM MoleculeAtom WHERE MOLECULES_ID=?", (item[0],))
                ATOM = db.c.fetchall()
                A = len(ATOM)
                A_D = str(A)
                result = result+A_D+','

            result = result.rstrip(", ")

            # num=1
            # db.c.execute("SELECT * FROM MoleculeBond WHERE MOLECULES_ID=? ORDER BY BOND_ID DESC LIMIT 1",(num,))
            # Bond = db.c.fetchone()[1]
            # print(Bond)
            # db.c.execute("SELECT * FROM MoleculeAtom WHERE MOLECULES_ID=? ORDER BY ATOM_ID DESC LIMIT 1",(num,))
            # Atom = db.c.fetchone()[1]
            # print(Atom)
            print(result)

   
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", len(result))
            self.end_headers()
            self.wfile.write(bytes(result, "utf-8"))

        elif self.path == "/file.svg":
            self.send_response(200)  # OK
            self.send_header("Content-type", "image/svg+xml")
            self.end_headers()
            with open('file.svg', 'r') as f:
                k = f.read()
                print(k)
                P = k.encode()
                self.wfile.write(P)

        elif self.path == "/getelements":
            self.send_response(200)  # OK

            db.c.execute("SELECT ELEMENT_NAME, * FROM Elements")
            
            t = db.c.fetchall()
            db.conn.commit()
            result=""
            for item in t:
                k = str(item[0])
                result = result+k+','
            result = result.rstrip(", ")
            print(result)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", len(result))
            self.end_headers()
            self.wfile.write(bytes(result, "utf-8"))
        
        
        elif self.path == "/":
            self.send_response(200)  # OK
            f = open('homepage.html', 'r')
            home = f.read()
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(home))
            self.end_headers()
            self.wfile.write(bytes(home, "utf-8"))
            f.close()

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: not found", "utf-8"))

    def do_POST(self):

        if self.path == "/molecule":

            # get content lenght
            # one of the atributes from 'headers' is a dictionary
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            body1 = body.decode('utf-8')
            print("PRINTING")
            print(body1)
            new = body1.split("filename=")
            name = new[1]

            name2 = name.split('name="filename"\r\n\r\n')
            name3 = name2[1].split('\r\n')
            print("PRINTINGFINAL")
            print(name3[0])
            namefinal = name3[0]

            # get file and turn into TextIoWrapper object
            # H = self.rfile.read(content_length)
            bytes_io = io.BytesIO(body)
            text_io = io.TextIOWrapper(bytes_io)
            # skip 4 lines
            text_io.readline()
            text_io.readline()
            text_io.readline()
            text_io.readline()
            # parse file and obtinag svg string
            Test = MolDisplay.Molecule()
            # add molecule with specified name to database
            db.add_molecule(namefinal, text_io)

            self.send_response(200)  # OK
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open('homepage2.html', 'rb') as f:
                self.wfile.write(f.read())

        elif self.path == "/showmol":
            # one of the atributes from 'headers' is a dictionary
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            body1 = body.decode('utf-8')
            print(body1)
            name = body1.split("&")
            mol = name[0].split("=")
            print(mol[1])
            axis = name[1].split("=")
            print(axis)
            degree = name[2].split("=")
            print(degree)

            MolDisplay.radius = db.radius()
            MolDisplay.element_name = db.element_name()
            MolDisplay.header = db.radial_gradients()  
            mol = db.load_mol(mol[1])
            mol.sort()
            if (degree[1] == '' or axis[1] == ''):

                k = mol.svg()

                f = open("file.svg", "w")
                f.write(k)
                f.close()
                self.send_response(200)  # OK
                self.send_header("Content-type", "text/html")
                self.end_headers()
                # P = k.encode()
                with open('homepage4.html', 'rb') as f:
                    self.wfile.write(f.read())
                # self.send_header("Content-type", "image/svg+xml")
                # self.send_header( "Content-length", len(P));
                # self.wfile.write(P) 
                self.end_headers()
                # self.wfile.write(P)
            else:
                deg = int(degree[1])
                if (axis[1] == 'x' or axis[1] == 'X'):

                    mx = molecule.mx_wrapper(deg, 0, 0)
                    mol.xform(mx.xform_matrix)
                    k = mol.svg()
                    f = open("file.svg", "w")
                    f.write(k)
                    f.close()

                elif (axis[1] == 'y' or axis[1] == 'Y'):

                    mx = molecule.mx_wrapper(0, deg, 0)
                    mol.xform(mx.xform_matrix)
                    k = mol.svg()
                    f = open("file.svg", "w")
                    f.write(k)
                    f.close()
                else:
                    mx = molecule.mx_wrapper(0, 0, deg)
                    mol.xform(mx.xform_matrix)
                    k = mol.svg()
                    f = open("file.svg", "w")
                    f.write(k)
                    f.close()
                    # encode svg string and send back to user in the form of a image
                # P = k.encode()
                self.send_response(200)  # OK
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open('homepage4.html', 'rb') as f:
                    self.wfile.write(f.read())
                # self.send_header("Content-type", "image/svg+xml")
                # self.send_header( "Content-length", len(P));
                # self.wfile.write(P)
                self.end_headers()
                
        elif self.path =="/TB":
            db.c.execute("SELECT * FROM Elements")
            t = db.c.fetchall()

            # result=""
            # for item in t:
            #     i=0
            #     for x in item:
            #         k=str(item[i])
            #         result=result+k+','
            #         i=i+1
            # result = result.rstrip(", ")
            result="heelo"
            print(result)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", len(result))
            self.end_headers()
            self.wfile.write(bytes(result, "utf-8"))

        elif self.path =="/remove":
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            body1 = body.decode('utf-8')
        
            remove=body1.split("=")[1]
            print(remove)
            db.c.execute("DELETE FROM Elements WHERE ELEMENT_NAME=?",(remove,))
            self.send_response(200)  # OK
            self.send_header("Content-type", "text/html")
            # self.send_header( "Content-length", len(home) );
            self.end_headers()
            with open('homepage3.html', 'rb') as f:
                self.wfile.write(f.read())

        elif self.path == "/senddata.html":
            # one of the atributes from 'headers' is a dictionary
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            postvars = urllib.parse.parse_qs(
                body.decode('utf-8'))  # parse query string

            values_list = [v[0] for v in postvars.values()]
            my_tuple = tuple(values_list)
            # Print the result  ing list
            db["Elements"] = my_tuple

            # #db['Elements'] = ( str(A), 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );

            self.flush_headers()

            self.send_response(200)  # OK
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open('homepage3.html', 'rb') as f:
                self.wfile.write(f.read())

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: not found", "utf-8"))


httpd = HTTPServer(('localhost', int(sys.argv[1])), MyHandler)
httpd.serve_forever()
