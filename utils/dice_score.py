import numpy as np
from bonndit.filter.filter import intersection_dict
from scipy.ndimage import gaussian_filter
from dipy.tracking.life import transform_streamlines
ds = tuple(3*np.array((145, 174, 145)))

def dice_intersection(streamlines, shape, dice_threshold, smoothing = 1):
    """
    dice_intersection creates the intersection grid for a set of streamlines.

    :param streamlines: the streamlines for the grid
    :param shape: shape of the grid
    :param dice_threshold: threshold for how many streamlines need to pass a point to count
    :param smoothing: smoothes the resulting grid, default is 1
    :return: returns the intersection grid
    """

    dice_mask = np.zeros(shape, dtype=np.float64)

    grid = intersection_dict(dice_mask, streamlines, 1)

    grid = gaussian_filter(grid, smoothing)
    grid[grid < dice_threshold] = 0
    grid[grid >= dice_threshold] = 1
    
    return grid

def dice_score(gt_streamlines, streamlines, dice_threshold, affine = None, shape = None, smoothing = 1, index_space = True, return_masks = False):
    """
    dice_score computes dice score, overreach and overlap for two sets of streamlines

    :param gt_streamlines: ground truth set of streamlines
    :param streamlines: second set of streamlines
    :param dice_threshold: threshold for how many streamlines need to pass a point to count
    :param affine: affine transformation, default is None
    :param shape: shape of the grid, default is None
    :param smoothing: smoothes the resulting grid, default is 1
    :param index_space: compute dice score in index space, default is True
    :param return_masks: return the intersection masks, default is False
    :return: returns dice score, overreach and overlap
    """
    if index_space:
        gt_streamlines = transform_streamlines(gt_streamlines, np.linalg.inv(affine))
        streamlines = transform_streamlines(streamlines, np.linalg.inv(affine))
    if shape is None:
        shape = ds
    grid_gt_bin = dice_intersection(gt_streamlines, shape, dice_threshold, smoothing)
    grid_bin = dice_intersection(streamlines, shape, dice_threshold, smoothing)
        
    inter = grid_bin * grid_gt_bin
    overlap = inter.sum() / grid_gt_bin.sum()
    gt = np.abs(1 - grid_gt_bin)
    inter_inv = gt*grid_bin
    overreach = inter_inv.sum() / grid_gt_bin.sum()
    dice = 2 * inter.sum() / (grid_bin.sum() + grid_gt_bin.sum())

    if return_masks:
        return dice, overreach, overlap, grid_gt_bin, grid_bin

    return dice, overreach, overlap