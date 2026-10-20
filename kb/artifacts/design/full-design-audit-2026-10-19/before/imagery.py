"""Shared image identity and captions; canonical metadata lives in the OKF KB."""
imagery_records=json.loads((R/'data/imagery-catalogue.json').read_text())['artworks']
imagery_by_src={a['src']:a for a in imagery_records}
def image_caption(src):
    return imagery_by_src[src]['caption']
