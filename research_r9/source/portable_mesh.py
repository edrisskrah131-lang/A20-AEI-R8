"""Windows adapter for the unchanged retained BVH source and mesh sampling."""
from pathlib import Path
import ctypes
import numpy as np

class PortableMesh:
    library_path = None
    prior_map_class = None

    def __init__(self, mesh_path, map_points=80000):
        if self.library_path is None or self.prior_map_class is None:
            raise RuntimeError('Configure the verified native library and prior map first')
        with np.load(mesh_path, allow_pickle=True) as z:
            self.v = np.ascontiguousarray(z['vertices'], dtype=np.float64)
            self.f = np.ascontiguousarray(z['faces'], dtype=np.int32)
            self.n = z['normals'].copy()
            self.area = z['area'].copy()
            self.names = z['names'].copy()
        self.lib = ctypes.CDLL(str(Path(self.library_path).resolve()))
        ptr = ctypes.c_void_p
        self.lib.build_mesh.restype = ptr
        self.lib.build_mesh.argtypes = [ptr, ptr, ctypes.c_int]
        self.lib.cast_rolling.argtypes = [ptr, ptr, ptr, ctypes.c_int, ptr, ptr]
        self.lib.free_mesh.argtypes = [ptr]
        self.handle = self.lib.build_mesh(self.v.ctypes.data, self.f.ctypes.data, len(self.f))
        if not self.handle:
            raise RuntimeError('Native mesh initialization failed')
        rng = np.random.default_rng(7093)
        faces = rng.choice(len(self.f), size=map_points, p=self.area/self.area.sum())
        u, v = rng.random(map_points), rng.random(map_points)
        flip = u+v > 1
        u[flip], v[flip] = 1-u[flip], 1-v[flip]
        t = self.v[self.f[faces]]
        points = t[:, 0]+u[:, None]*(t[:, 1]-t[:, 0])+v[:, None]*(t[:, 2]-t[:, 0])
        self.prior = self.prior_map_class(points, self.n[faces], faces)

    def cast(self, origins, directions):
        origins = np.ascontiguousarray(origins, dtype=np.float64)
        directions = np.ascontiguousarray(directions, dtype=np.float64)
        if origins.shape != directions.shape or directions.ndim != 2 or directions.shape[1] != 3:
            raise ValueError('Each ray requires one three-dimensional origin and direction')
        if not np.all(np.isfinite(origins)) or not np.all(np.isfinite(directions)):
            raise ValueError('Non-finite ray coordinates')
        ranges = np.empty(len(directions), dtype=np.float64)
        faces = np.empty(len(directions), dtype=np.int32)
        self.lib.cast_rolling(self.handle, origins.ctypes.data, directions.ctypes.data,
                             len(directions), ranges.ctypes.data, faces.ctypes.data)
        return ranges, faces

    def close(self):
        if getattr(self, 'handle', None):
            self.lib.free_mesh(self.handle)
            self.handle = None

    def __del__(self):
        self.close()
