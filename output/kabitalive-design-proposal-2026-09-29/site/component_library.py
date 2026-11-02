"""Explicit public utility renderer; never admit arbitrary KB files or review aliases."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROUTE = 'component-library.html'

def render_component_library(site):
    site = Path(site).resolve()
    project = next((p for p in site.parents if (p/'utkal.config.json').is_file()), None)
    if project is None:
        raise ValueError('Kabita Live project root not found for component renderer')
    source = project/'kb/artifacts/design/component-library/build.py'
    if not source.is_file():
        raise ValueError('Approved component-library source missing')
    spec = spec_from_file_location('kabita_component_library', source)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    # Current generated journal inputs are passed explicitly. The renderer neither
    # reads its preview alias nor relies on stale local provenance manifests.
    return module.render(site=site, public=True)
