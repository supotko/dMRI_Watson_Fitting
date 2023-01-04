import numpy as np
import argparse
import logging
logging.basicConfig(level = logging.INFO)
from dipy.io.streamline import load_tractogram, save_tractogram
from dipy.tracking.life import transform_streamlines
from dipy.io.stateful_tractogram import StatefulTractogram
from dipy.tracking.streamline import Streamlines, cluster_confidence

def main():
    parser = argparse.ArgumentParser(
		description='Filters a set of streamlines by cluster confidence index.',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    import warnings
    warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)
    warnings.filterwarnings("ignore", category=UserWarning)

    parser.add_argument('-st', help='streamlines to be postprocessed, as trk or tck file', required=True)
    parser.add_argument('-cci', help='Threshold for the cluster confidence index', required=True)
    parser.add_argument('-rst', help='Reference file for the affine if st is of type tck, e.g. trk file of same brain')
    parser.add_argument('-o', help='Outfile', required=True)

    args = parser.parse_args()

    # load the streamlines
    logging.info("Loading streamlines")
    if args.st.endswith("tck"):
        sft = load_tractogram(args.st, args.rst)
    else:
        sft = load_tractogram(args.st, 'same')
    streamlines = transform_streamlines(sft.streamlines, np.linalg.inv(sft.affine))

    # filter by cci
    logging.info("Removing streamlines with too low cluster confidence")
    streamlines = filter_by_cluser_confidence(streamlines, float(args.cci))

    # saving
    streamlines = transform_streamlines(streamlines, sft.affine)
    new_sft = StatefulTractogram.from_sft(streamlines, sft)
    save_tractogram(new_sft, args.o)
    logging.info(f"Saved output to {args.o}")

def filter_by_cluser_confidence(streamlines, threshold):
    """
    filter_by_cluser_confidence remove streamlines that have a cluster confidence below a given threshold

    :param streamlines: streamlines to filter
    :param threshold: threshold for the cci to be included
    :return: returns the filtered streamlines
    """
    filtered_streamlines = Streamlines()
    cci = cluster_confidence(streamlines, override=True)
    for i, streamline in enumerate(streamlines):
        if cci[i] >= threshold:
            filtered_streamlines.append(streamline)
    return filtered_streamlines

if __name__ == "__main__":
    main()