import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import nilearn
    from nilearn import datasets
    from ipyniivue import NiiVue
    from pathlib import Path
    import nibabel as nib

    return NiiVue, Path, datasets, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Interactive Dashboard
    """)
    return


@app.cell
def _(datasets):
    fsaverage = datasets.fetch_surf_fsaverage(mesh="fsaverage")
    return (fsaverage,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Plot Glasser Atlas
    """)
    return


@app.cell
def _(mo):
    hemi = mo.ui.radio(
        options=["Left", "Right"],
        value = "Left",
        label="Hemisphere"
    )
    hemi
    return (hemi,)


@app.cell
def _(mo):
    get_label, set_label = mo.state("Hover over brain...")
    return get_label, set_label


@app.cell
def _(NiiVue, Path, fsaverage, hemi, set_label):
    meshes = []
    if hemi.value in ("Left"):
        meshes.append({
            "path": Path(fsaverage["infl_left"]),
            "layers": [{"path": Path("data/atlases/lh.HCPMMP1.label.gii")}]
        })
    if hemi.value in ("Right"):
        meshes.append({
            "path": Path(fsaverage["infl_right"]),
            "layers": [{"path": Path("data/atlases/rh.HCPMMP1.label.gii")}]
        })

    nv = NiiVue()
    nv.load_meshes(meshes)


    @nv.on_location_change
    def show_location(location):
        set_label(location["string"])

    nv
    return


@app.cell
def _(get_label, mo):

    mo.md(get_label())
    return


if __name__ == "__main__":
    app.run()
