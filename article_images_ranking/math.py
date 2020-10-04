import math

import numpy as np


def is_nan(x):
    return isinstance(x, float) and math.isnan(x)


def cal_cosine(x, y):
    norm_x = x / np.linalg.norm(x)
    norm_y = y / np.linalg.norm(x)

    return float(np.dot(norm_x, norm_y))
