import numpy as np
import argparse
import nrrd
from dipy.io.streamline import load_tractogram
from dipy.tracking.life import transform_streamlines
from dipy.tracking.utils import density_map, random_seeds_from_mask
from nibabel.affines import apply_affine
import nibabel as nib
import logging

def save_seeds_to_file(filename, seeds, directions, include_directions = True, append = False):
    """
    save_seeds_to_file saves seeds to file with space separated x,y,z values, the parameter means is set and include_directions is true, the direction values are added as additional columns
    :param filename: file to write seeds to (and initial directions)
    :param seeds: seeding points
    :param means: initial direction values, optional
    :param include_directions: flag, if directions are included, default is True
    """
    seeds_str = ""
    for i in range(len(seeds)):
        for v in seeds[i]:
            seeds_str += str(v) + ' '
        if include_directions:
            if len(directions) == 1:
                for v in directions[0]:
                    seeds_str += str(v) + ' '
            else:
                for v in directions[i]:
                    seeds_str += str(v) + ' '
        seeds_str += '\n'
    mode = 'w'
    if append:
        mode = 'a'
    with open(filename, mode) as file:
        if append:
            file.write('\n')
        file.write(seeds_str)

def main():
    parser = argparse.ArgumentParser(
		description='Generates seeds in a given seeding region. Additionally reference streamlines can be included to additionally filter the seeding plane to.',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    import warnings
    warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

    parser.add_argument('-mask', help='bounds of the seed mask in the order sagittal, coronal, axial', default='0:144,0:173,10:30')
    parser.add_argument('-maskfile', help='instead of mask, use a maskfile (nii.gz)')
    parser.add_argument('-n', help='number of seeds', default=1000)
    parser.add_argument('-o', help='Outfile', required=True)
    parser.add_argument('-append', help='Seeds are appended to existing seeds in the outfile', action='store_true')
    parser.add_argument('-st', help='Optional reference streamlines to additionally filter the seeding plane to')
    parser.add_argument('-affine', help='Optional NRRD File with Affine transformation to convert to world space, e.g. wmvolume.nrrd')
    parser.add_argument('-direction', help='Optional initial directions, e.g. 0,1,0')
    parser.add_argument('-shape', help='custom shape of the dMRI data', default='145,174,145')

    args = parser.parse_args()

    logging.basicConfig(level = logging.INFO)
    logging.getLogger().setLevel(logging.INFO)

    # get shape
    shape = tuple(np.array(args.shape.split(',')).astype(int))

    # generate seed mask
    if args.maskfile is None:
        b = np.array(np.char.split(np.array(args.mask.split(',')), ':').tolist()).astype(int)
        b[0] = np.clip(b[0], 1, shape[0]-2)
        b[1] = np.clip(b[1], 1, shape[1]-2)
        b[2] = np.clip(b[2], 1, shape[2]-2)
        seed_mask = np.zeros(shape, 'bool')
        seed_mask[b[0,0]:b[0,1],b[1,0]:b[1,1],b[2,0]:b[2,1]] = True
    else:
        img = nib.load(args.maskfile)
        seed_mask = np.asanyarray(img.dataobj).astype(bool)

    # load the streamlines
    if args.st is not None:
        logging.info("Loading streamlines")
        sft_gs = load_tractogram(args.st, 'same')
        streamlines_g = transform_streamlines(sft_gs.streamlines, np.linalg.inv(sft_gs.affine))
        st_mask = density_map(streamlines_g, np.eye(4), sft_gs.dimensions)

        # only include voxels that the reference streamlines cross
        seed_mask = seed_mask & st_mask
    
    # generate seeds
    logging.info("Generating seeds")
    seeds = random_seeds_from_mask(seed_mask, np.eye(4), seeds_count=int(args.n), seed_count_per_voxel=False, random_seed=None)
    
    # convert to world space if nrrd given
    if args.affine is not None:
        _, meta = nrrd.read(args.affine)
        wm_affine = np.zeros((4,4))
        wm_affine[:3,:3] = meta['space directions']
        wm_affine[:3,3] = meta['space origin']
        wm_affine[3,3] = 1
        seeds = apply_affine(wm_affine, seeds)

    # save seeds
    # get direction
    if args.direction is not None:
        direction = np.array(args.direction.split(',')).astype(float)
        save_seeds_to_file(args.o, seeds, np.array([direction]), True, append=args.append)
    else:
        save_seeds_to_file(args.o, seeds, None, False, append=args.append)
    logging.info(f"Saved output to {args.o}")

if __name__ == "__main__":
    main()