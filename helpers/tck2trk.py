import nibabel as nib
from nibabel.streamlines import Field
from nibabel.orientations import aff2axcodes
import argparse
import os
import numpy as np


def build_argparser():
    DESCRIPTION = "Convert tractograms (TCK -> TRK)."
    p = argparse.ArgumentParser(description=DESCRIPTION)
    p.add_argument('tractograms', metavar='bundle', nargs="+", help='list of tractograms.')
    p.add_argument('-f', '--force', action="store_true", help='overwrite existing output files.')
    return p


def main():
    parser = build_argparser()
    args = parser.parse_args()

    for tractogram in args.tractograms:
        if nib.streamlines.detect_format(tractogram) is not nib.streamlines.TckFile:
            print("Skipping non TCK file: '{}'".format(tractogram))
            continue
        output_filename = tractogram[:-4] + '.trk'
        if os.path.isfile(output_filename) and not args.force:
            print("Skipping existing file: '{}'. Use -f to overwrite.".format(output_filename))
            continue
        trk = nib.streamlines.load(tractogram)
        nib.streamlines.save(trk.tractogram, output_filename) #, header=header)


if __name__ == '__main__':
        main()