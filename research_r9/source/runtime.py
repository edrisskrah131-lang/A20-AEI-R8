"""Load retained R8 without modifying its sources, models or result directory."""
from pathlib import Path
import os, sys, json

os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
HERE = Path(__file__).resolve().parents[1]
WORKSPACE = HERE.parents[2]
R8 = WORKSPACE / 'work/A20_R8_start/A20_release/output/A20_AEI_R8'
sys.path.insert(0, str(R8 / 'source'))

def initialize():
    from portable_mesh import PortableMesh
    from r8_collect import generate
    from r8_geometry import geometry, route
    from rcp.core import PriorMap, exp, log, propagate
    from r8_service import controlled, prediction_cache, load_models, state_from
    from r8_policy import policies
    import numpy as np
    PortableMesh.library_path = HERE / 'native/bvh_windows.dll'
    PortableMesh.prior_map_class = PriorMap
    meshes = {(m, level): PortableMesh(geometry(m, level))
              for m in ('B767', 'C172', 'UnfittedAirframe') for level in range(4)}
    routes = {m: np.load(route(m))['pose'] for m in ('B767', 'C172', 'UnfittedAirframe')}
    keep = ['Fixed2', 'Fixed4', 'Final', 'FlatCART', 'FlatRF', 'KG1', 'ContractRF', 'OldRAVC']
    ps = {p['id']: p for p in policies()}
    clock = json.loads((R8 / 'data/r8_final/clock_profile.json').read_text())
    bindings = json.loads((R8 / 'data/r8_final/runtime_bindings.json').read_text())
    return dict(meshes=meshes, routes=routes, generate=generate, exp=exp, log=log,
                propagate=propagate, controlled=controlled, prediction_cache=prediction_cache,
                models=load_models(), state_from=state_from, policies=[ps[p] for p in keep],
                clock=clock, bindings=bindings)
