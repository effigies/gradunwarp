import os
import tempfile

import numpy as np
import nibabel as nb
from nibabel.tmpdirs import InTemporaryDirectory

from ..gradient_unwarp import GradientUnwarpRunner


class Arguments:
    """Just something to dump args into"""


def test_trivial_unwarp():
    with InTemporaryDirectory() as tmpdir:
        # Siemens Allegra coefficient arrays are 15x15, keeping things small and fast
        coef_file = "allegra.coef"
        open(coef_file, 'wb').close()  # touch
        assert os.path.exists(coef_file)

        orig_arr = np.arange(24).reshape(2, 3, 4)

        # Use centered LAS affine for simplicity. Easiest way to get it is
        # creating the image and asking nibabel to make it for us.
        img = nb.Nifti1Image(orig_arr.astype("float32"), None)
        img.set_sform(img.header.get_base_affine(), 1)
        img.set_qform(img.header.get_base_affine(), 1)
        img.to_filename("test.nii")

        args = Arguments()
        args.infile = "test.nii"
        args.outfile = "out.nii"
        args.vendor = "siemens"
        args.coeffile = coef_file

        unwarper = GradientUnwarpRunner(args)
        unwarper.run()
        unwarper.write()

        unwarped_img = nb.load("out.nii")
        assert np.allclose(unwarped_img.get_fdata(), orig_arr)
