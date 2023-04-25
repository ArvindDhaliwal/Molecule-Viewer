import MolDisplay;
import molecule;
import molsql
db = molsql.Database(False)
MolDisplay.radius = db.radius()
MolDisplay.element_name = db.element_name()
MolDisplay.header += db.radial_gradients()

mol = MolDisplay.Molecule();

fp = open( 'caffeine-3D-structure-CT1001987571.sdf' );
mol.parse( fp );
mol.sort();

print( mol );

mx = molecule.mx_wrapper(0,70,0);
mol.xform( mx.xform_matrix );

print( mol.svg());

