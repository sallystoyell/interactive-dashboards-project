import numpy as np
import nibabel as nib

def annot_to_label_gii(annot_path, out_path):
    labels, ctab, names = nib.freesurfer.read_annot(annot_path)
    
    label_table = nib.gifti.GiftiLabelTable()
    for i, (name, color) in enumerate(zip(names, ctab)):
        gl = nib.gifti.GiftiLabel(
            key=i,
            red=color[0]/255,
            green=color[1]/255,
            blue=color[2]/255,
            alpha=1.0
        )
        gl.label = name.decode() if isinstance(name, bytes) else name
        label_table.labels.append(gl)

    arr = nib.gifti.GiftiDataArray(
        data=labels.astype(np.int32),
        intent=nib.nifti1.intent_codes['NIFTI_INTENT_LABEL'],
        datatype='NIFTI_TYPE_INT32'
    )
    img = nib.gifti.GiftiImage(darrays=[arr], labeltable=label_table)
    nib.save(img, out_path)


annot_to_label_gii("data/atlases/lh.HCPMMP1.annot", "data/atlases/lh.HCPMMP1.label.gii")
annot_to_label_gii("data/atlases/rh.HCPMMP1.annot", "data/atlases/rh.HCPMMP1.label.gii")