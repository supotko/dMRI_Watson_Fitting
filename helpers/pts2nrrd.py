import argparse
import numpy as np
import nrrd
import nibabel as nib
def main():
    """Take a list of seedpoints in pts format and create a labed nrrd files



    Returns
    -------

    """

    parser = argparse.ArgumentParser(
        description='This script performs tracking along a multi vector field')

    parser.add_argument('-i', help='Infile')
    parser.add_argument('-o', help='Outfile')
    parser.add_argument('-n', help='nrrd file with meta data')
    parser.add_argument("-r", help="create region", action='store_false')
    args = parser.parse_args()
    seeds = np.loadtxt(args.i)
    wm, meta = nrrd.read(args.n)
    labels = np.zeros(wm.shape, dtype=np.float32)
    trafo = np.zeros((4,4))
    trafo[:3,:3] = meta['space directions'] 
    trafo[3,3] = 1
    trafo[:3,3] = meta['space origin']
    trafo = np.linalg.inv(trafo)
    sc = np.ones((seeds.shape[0], 4))
    sc[:, :3] = seeds[:,:3]
    for i in range(seeds.shape[0]):
      #  sc = np.ones(4)

        sc[i] = trafo @ sc[i]
        if args.r:
            labels[int(sc[i,0]), int(sc[i,1]), int(sc[i,2])] = 1
    if not args.r:
        smin = np.min(sc, axis=0)
        print(smin)
        smax = np.max(sc, axis=0) + 2
        labels[int(smin[0]):int(smax[0]), int(smin[1]):int(smax[1]), int(smin[2]):int(smax[2])] = 1

    if args.o.endswith('nrrd'):
        nrrd.write(args.o, np.int16(labels), meta)
    elif args.o.endswith('nii.gz'):
        affine = np.zeros((4,4))
        affine[3,3] = 1
        affine[:3,:3] = meta['space directions']
        affine[:3,3] = meta['space origin']
        out_img = nib.Nifti1Image(np.int16(labels), affine)
        nib.save(out_img, args.o)
    else:
        print('unsupported format. Only nrrd and nii.gz are supported')
    
if __name__ == '__main__':
    main()
