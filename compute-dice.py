import numpy as np
import os
import argparse
import logging
from utils.dice_score import dice_score
logging.basicConfig(level = logging.INFO)
from dipy.io.streamline import load_tractogram
from dipy.tracking.life import transform_streamlines

def main():
    parser = argparse.ArgumentParser(
        description='Computes Dice score, Overreach and Overlap.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    import warnings
    warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

    parser.add_argument('-st', help='generated streamlines to check, as trk or tck file', required=True)
    parser.add_argument('-rst', help='reference streamlines, as trk file', required=True)
    parser.add_argument('-dt', help='threshold for how many streamlines need to pass a voxel to count', default=1)
    parser.add_argument('-smoothing', help='smoothes the resulting grid', default=1)
    parser.add_argument('-save', help='if filename given, save scores to npy file')

    args = parser.parse_args()

    # load the streamlines
    logging.info("Loading streamlines")
    sft_rs = load_tractogram(args.rst, 'same')
    streamlines_r = sft_rs.streamlines#transform_streamlines(sft_rs.streamlines, np.linalg.inv(sft_rs.affine))

    if args.st.endswith('.tck'):
      sft_gs = load_tractogram(args.st, reference=args.rst)
    else:
      sft_gs = load_tractogram(args.st, 'same')
    streamlines_g = sft_gs.streamlines#transform_streamlines(sft_gs.streamlines, np.linalg.inv(sft_gs.affine))

    # compute dice, overreach and overlap
    logging.info("Computing dice, overreach and overlap")
    dice, overreach, overlap = dice_score(streamlines_r, streamlines_g, int(args.dt), sft_gs.affine, smoothing = int(args.smoothing))
    logging.info(f"\nDice:\t\t{dice}\nOverreach:\t{overreach}\nOverlap:\t{overlap}\n# Streamlines:\t{len(streamlines_g)}\n")
    if args.save is not None:
      np.save(args.save, np.array([dice, overreach, overlap, len(streamlines_g)]))

if __name__ == "__main__":
    main()