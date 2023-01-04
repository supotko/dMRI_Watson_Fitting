import nibabel as nib
from plyfile import PlyData, PlyElement
import numpy as np
import argparse
from tqdm import tqdm

def ply2tck(args):
    with open(args.i, 'rb') as f:
        plydata = PlyData.read(f)
        num_verts = plydata['vertices'].count
        num_fiber = plydata['fiber'].count
        vertices = np.zeros(shape=[num_verts, 3], dtype=np.float64)
        endindex = np.zeros(shape=[num_fiber], dtype=int)
        vertices[:, 0] = plydata['vertices'].data['x']
        vertices[:, 1] = plydata['vertices'].data['y']
        vertices[:, 2] = plydata['vertices'].data['z']
        endindex[:] = plydata['fiber'].data['endindex']

    streamlines = nib.streamlines.ArraySequence(np.split(vertices, endindex))
    mytractogram = nib.streamlines.tractogram.Tractogram(streamlines, affine_to_rasmm=np.identity(4))
    tractogram = nib.streamlines.tck.TckFile(mytractogram)
    tractogram.save(args.o)

def tck2ply(args):
    streamlines  = nib.streamlines.load(args.i)
    streamlines = streamlines.streamlines
    endindex = [len(x) for x in streamlines]
    endindex = np.cumsum(endindex)
    streamlines = np.concatenate(streamlines)
    tracks = PlyElement.describe(np.array([tuple(x) for x in streamlines],  dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')]),
            'vertices', comments=[])
    endindex = PlyElement.describe(np.array([ *endindex], dtype=[('endindex', 'i4')]), 'fiber')
    PlyData([tracks, endindex]).write(args.o)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='Input')
    parser.add_argument('-o', help='output')
    args = parser.parse_args()
    if args.i.endswith('ply'):
        ply2tck(args)
    elif args.i.endswith('tck'):
        tck2ply(args)
    else:
        print('Only conversion from and to tck from and to ply is possible so far. Further, we assume that the affine matrix of is identity and all additional features except of coordinates are removed.')



if __name__ == '__main__':
    main()
