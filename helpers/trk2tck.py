import nibabel as nib
from nibabel.streamlines import Field
from nibabel.orientations import aff2axcodes
import argparse
import os
import numpy as np


def build_argparser():
    DESCRIPTION = "Convert tractograms (TRK -> TCK)."
    p = argparse.ArgumentParser(description=DESCRIPTION)
    p.add_argument('tractograms', metavar='bundle', nargs="+", help='list of tractograms.')
    p.add_argument('-f', '--force', action="store_true", help='overwrite existing output files.')
    return p


def main():
    parser = build_argparser()
    args = parser.parse_args()

    for tractogram in args.tractograms:
        if nib.streamlines.detect_format(tractogram) is not nib.streamlines.TrkFile:
            print("Skipping non TRK file: '{}'".format(tractogram))
            continue
        output_filename = tractogram[:-4] + '.tck'
        if os.path.isfile(output_filename) and not args.force:
            print("Skipping existing file: '{}'. Use -f to overwrite.".format(output_filename))
            continue
        tck = nib.streamlines.load(tractogram)
        nib.streamlines.save(tck.tractogram, output_filename) #, header=header)


if __name__ == '__main__':
        main()