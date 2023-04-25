#include "mol.h"

void atomset(atom *atom, char element[3], double *x, double *y, double *z)
{

    strcpy(atom->element, element); // atom name
    // atom elements
    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
}

void atomget(atom *atom, char element[3], double *x, double *y, double *z)
{

    strcpy(element, atom->element); // atom name

    // atom elements
    *x = atom->x;
    *y = atom->y;
    *z = atom->z;
}

void compute_coords(bond *bond)

{
    //a1=x1/y1 a2=x2/y2
    bond->x1 = bond->atoms[bond->a1].x;
    bond->x2 = bond->atoms[bond->a2].x;
    bond->y1 = bond->atoms[bond->a1].y;
    bond->y2 = bond->atoms[bond->a2].y;

    bond->z = ((bond->atoms[bond->a2].z + bond->atoms[bond->a1].z) / 2); // average of 2 z values

    bond->len = sqrt(pow(bond->x1 - bond->x2, 2) + pow(bond->y1 - bond->y2, 2));
    bond->dx = (bond->x2 - bond->x1) / bond->len;
    bond->dy = (bond->y2 - bond->y1) / bond->len;
}

void bondset(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs)
{

    // assign values
    bond->epairs = *epairs;
    bond->a1 = *a1; 
    bond->a2 = *a2;
    bond->atoms = *atoms; //
    compute_coords(bond); //ensure new values are set
}

void bondget(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs)
{
    //get values
    *epairs = bond->epairs;
    *a1 = bond->a1;
    *a2 = bond->a2;
    *atoms = bond->atoms;
}

molecule *molmalloc(unsigned short atom_max, unsigned short bond_max)
{
    molecule *ptr = (struct molecule *)malloc(sizeof(struct molecule));
    if (ptr == NULL) // check if malloc failed!
    {
    }
    else
    {
        ptr->atom_max = atom_max;
        ptr->atom_no = 0;

        if (ptr->atom_max == 0)
        {
            ptr->atoms = NULL;
            ptr->atom_ptrs = NULL;
        }
        else
        {
            ptr->atoms = (struct atom *)malloc(sizeof(struct atom) * atom_max); // allocate memory for atoms
            ptr->atom_ptrs = (struct atom **)malloc(sizeof(struct atom *) * atom_max);
        }

        ptr->bond_max = bond_max;
        ptr->bond_no = 0;

        if (ptr->bond_max == 0)
        {
            ptr->bond_ptrs = NULL;
            ptr->bonds = NULL;
        }
        else
        {

            ptr->bond_ptrs = (struct bond **)malloc(sizeof(struct bond *) * bond_max);
            ptr->bonds = (struct bond *)malloc(sizeof(struct bond) * bond_max);
        }
    }

    return ptr;
}
// uses in molecure and allocate memory

molecule *molcopy(molecule *src) // copy molecule
{
    molecule *tmp;      // pointer that will store address
    tmp = molmalloc(src->atom_max, src->bond_max); // return address to malloced memory by sending atom max and bond max
    int i = 0;
    while (i < src->atom_no) // atom_no will already be at the value of total atoms
    {
        atom *tmp2 = src->atoms + i;

        molappend_atom(tmp, tmp2); // append atom to molecule tmp
        i++;
    }
    i = 0;
    while (i < src->bond_no) // bond_no will already be at the value of total atoms
    {
        bond *tmp3 = src->bonds + i;

        molappend_bond(tmp, tmp3); // append bond to molecule tmp
        i++;
    }

    tmp->atom_no = src->atom_no;
    tmp->bond_no = src->bond_no;

    return tmp;
}

void molfree(molecule *ptr) // free atom and set to null
{
    if (ptr->atom_ptrs == NULL)
    {
        // do nothing
    }
    else
    {
        free(ptr->atom_ptrs);
        ptr->atom_ptrs = NULL;
    }

    if (ptr->atoms == NULL)
    {
        // do nothing
    }
    else
    {
        free(ptr->atoms);
        ptr->atoms = NULL;
    }
    if (ptr->bond_ptrs == NULL)
    {
    }
    else
    {
        free(ptr->bond_ptrs);
        ptr->bond_ptrs = NULL;
    }

    if (ptr->bonds == NULL)
    {
        // do nothing
    }
    else
    {
        free(ptr->bonds);
        ptr->bonds = NULL;
    }
    if (ptr == NULL)
    {
        // do nothing
    }
    else
    {
        free(ptr);
        ptr = NULL;
    }

} // free memory stored by moleule

void molappend_atom(molecule *molecule, atom *atom)
{

    if (molecule->atom_max == 0) // if atom_max is 0 make it one and malloc space
    {

        molecule->atom_max = 1;
        molecule->atoms = (struct atom *)malloc(sizeof(struct atom) * molecule->atom_max);
        molecule->atom_ptrs = (struct atom **)malloc(sizeof(struct atom) * molecule->atom_max);
    }
    else if (molecule->atom_max == molecule->atom_no) // if atom_max is equal to atom_no realloc space
    {

        molecule->atom_max = molecule->atom_max * 2;
        molecule->atoms = (struct atom *)realloc(molecule->atoms, sizeof(struct atom) * molecule->atom_max);
        molecule->atom_ptrs = (struct atom **)realloc(molecule->atom_ptrs, sizeof(struct atom *) * molecule->atom_max);
        for (int i = 0; i < molecule->atom_no; i++)
        { // ensure atom_ptrs are pointed to the correct new atom!
            molecule->atom_ptrs[i] = molecule->atoms + (i);
        }
    }

    molecule->atoms[molecule->atom_no] = *atom;
    molecule->atom_ptrs[molecule->atom_no] = molecule->atoms + (molecule->atom_no); // addres of pointer given to doubel pointer
    molecule->atom_no++;
}

void molappend_bond(molecule *molecule, bond *bond)
{
    if (molecule->bond_max == 0) // if atom_bond is 0 make it one and malloc space
    {
        molecule->bond_max = 1;
        molecule->bonds = (struct bond *)malloc(sizeof(struct bond) * molecule->bond_max);
        molecule->bond_ptrs = (struct bond **)malloc(sizeof(struct bond *) * molecule->bond_max);
    }
    if (molecule->bond_max == molecule->bond_no) // if bond_max is equal to atom_no realloc space
    {
        molecule->bond_max = molecule->bond_max * 2;
        molecule->bonds = (struct bond *)realloc(molecule->bonds, sizeof(struct bond) * molecule->bond_max);
        molecule->bond_ptrs = (struct bond **)realloc(molecule->bond_ptrs, sizeof(struct bond *) * molecule->bond_max);
        for (int i = 0; i < molecule->bond_no; i++)
        { // ensure bond_ptrs are pointed to the correct new atom!
            molecule->bond_ptrs[i] = molecule->bonds + (i);
        }
    }

    molecule->bonds[molecule->bond_no] = *bond;
    molecule->bond_ptrs[molecule->bond_no] = molecule->bonds + (molecule->bond_no); // addres of pointer given to doubel pointer
    molecule->bond_no++;
}

int atom_comp(const void *a, const void *b) // compare atoms
{
    // dereference doubel pointer
    const atom *eval1 = *(struct atom **)a;
    const atom *eval2 = *(struct atom **)b;

    if (eval1->z < eval2->z)
    {
        return -1;
    }
    else if (eval1->z > eval2->z)
    {
        return +1;
    }
    else

        return 0;
}

int bond_comp(const void *a, const void *b) // compare bonds
{   // dereference doubel pointer
    const bond *eval1 = *(struct bond **)a;
    const bond *eval2 = *(struct bond **)b;
    float E1 = eval1->z;

    float E2 = eval2->z;

    if (E1 < E2)
    {
        return -1;
    }
    else if (E1 > E2)
    {
        return +1;
    }
    else
    {
        return 0;
    }
}

void molsort(molecule *molecule)
{
    // use compare function to sort, send in size of one atom_ptrs (aka atom)
    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(struct atom *), atom_comp);
    // use compare2 function to sort, send in size of one bond_ptrs (aka bond)
    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(struct bond *), bond_comp);
}

void xrotation(xform_matrix xform_matrix, unsigned short deg)
{

    // apply xrotation matrix
    double rad = deg * (M_PI / 180.0);
    xform_matrix[0][0] = 1;
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = 0;

    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = sin(rad) * -1;

    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = sin(rad);
    xform_matrix[2][2] = cos(rad);
}

void yrotation(xform_matrix xform_matrix, unsigned short deg)
{

    // apply xrotation matrix
    double rad = deg * (M_PI / 180.0);
    xform_matrix[0][0] = cos(rad);
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = sin(rad);

    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = 1;
    xform_matrix[1][2] = 0;

    xform_matrix[2][0] = sin(rad) * -1;
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = cos(rad);
}

void zrotation(xform_matrix xform_matrix, unsigned short deg)
{

    // apply xrotation matrix
    double rad = deg * (M_PI / 180.0);
    xform_matrix[0][0] = cos(rad);
    xform_matrix[0][1] = sin(rad) * -1;
    xform_matrix[0][2] = 0;

    xform_matrix[1][0] = sin(rad);
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = 0;

    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = 1;
}

void mol_xform(molecule *molecule, xform_matrix matrix)
{
    // apply rotation matrix to atom coordinates
    for (int i = 0; i < molecule->atom_no; i++) // maybe shoudl change to atom_no
    {
        double x = molecule->atoms[i].x;
        double y = molecule->atoms[i].y;
        double z = molecule->atoms[i].z;

        molecule->atoms[i].x = ((x * matrix[0][0]) + (y * matrix[0][1]) + (z * matrix[0][2]));
        molecule->atoms[i].y = ((x * matrix[1][0]) + (y * matrix[1][1]) + (z * matrix[1][2]));
        molecule->atoms[i].z = ((x * matrix[2][0]) + (y * matrix[2][1]) + (z * matrix[2][2]));
    }
    // apply rotation matrix to bond coordinates
    for (int i = 0; i < molecule->bond_no; i++)
    {
        //apply the compute_coords funtion to each bond
        bondset(molecule->bonds + i, &molecule->bonds[i].a1, &molecule->bonds[i].a2, &(molecule->atoms), &molecule->bonds[i].epairs);
    }
}
