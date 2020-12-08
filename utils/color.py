import numpy as np
import matplotlib
from PIL import Image

def trans_colormapped_depth_image(disp_image):
    vmax = np.percentile(disp_image, 95)
    normalizer = matplotlib.colors.Normalize(vmin=disp_image.min(), vmax=vmax)
    mapper = matplotlib.cm.ScalarMappable(norm=normalizer, cmap='magma')
    colormapped_im = (mapper.to_rgba(disp_image)[:, :, :3] * 255).astype(np.uint8)
    im = Image.fromarray(colormapped_im)
    return im

