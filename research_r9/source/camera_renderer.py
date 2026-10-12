"""Actual synthetic pinhole raster; no generated photograph or measured CAD claim."""
import time
import numpy as np
from scipy.ndimage import gaussian_filter

EXTRINSIC = np.array([.15, 0., .75])

def camera_frame(pose, exp, gimbal_R=None):
    body = exp(pose[3:])
    angle = -.12
    pitch = np.array([[np.cos(angle),0,np.sin(angle)], [0,1,0],
                      [-np.sin(angle),0,np.cos(angle)]])
    return pose[:3]+body@EXTRINSIC, body@(pitch if gimbal_R is None else gimbal_R)

def render(mesh, pose, map_t, map_R, rng, exp, width=192, height=144,
           focal_px=1800., exposure_s=.006, speed_m_s=.15, gimbal_R=None):
    start = time.process_time_ns()
    origin, R = camera_frame(pose, exp, gimbal_R)
    u,v = np.meshgrid(np.arange(width)+.5-width/2, np.arange(height)+.5-height/2)
    directions = np.c_[np.ones(u.size), -u.ravel()/focal_px, -v.ravel()/focal_px]
    directions /= np.linalg.norm(directions, axis=1)[:,None]
    world_dirs = directions@R.T
    origins = np.repeat(((origin-map_t)@map_R)[None,:], len(directions), axis=0)
    distance, face = mesh.cast(origins, world_dirs@map_R)
    valid = np.isfinite(distance) & (face >= 0)
    rgb = np.full((len(directions),3), 205., dtype=float)
    gsd = np.full(len(directions), np.inf)
    if np.any(valid):
        local = origins[valid]+(world_dirs[valid]@map_R)*distance[valid,None]
        incidence = np.abs(np.einsum('ij,ij->i',mesh.n[face[valid]],world_dirs[valid]@map_R))
        light = .25+.75*np.abs(mesh.n[face[valid]]@np.array([.2,.3,.932737905]))
        texture = 125.+28.*np.sin(local[:,0]*5.)*np.cos(local[:,1]*7.)
        rgb[valid] = (texture*light)[:,None]*np.array([.92,.97,1.02])
        gsd[valid] = distance[valid]/(focal_px*np.maximum(incidence,1e-8))
    positive = gsd[np.isfinite(gsd)]
    median_gsd = float(np.median(positive)) if len(positive) else np.inf
    blur_px = speed_m_s*exposure_s/median_gsd if np.isfinite(median_gsd) else np.inf
    image = rgb.reshape(height,width,3)
    if np.isfinite(blur_px) and blur_px > .05:
        image = gaussian_filter(image, sigma=(blur_px/np.sqrt(12),blur_px/np.sqrt(12),0))
    image += rng.normal(0,.8,image.shape)
    image = np.clip(np.rint(image),0,255).astype(np.uint8)
    return {'rgb':image,'distance':distance.reshape(height,width),
            'face':face.reshape(height,width),'gsd_m':gsd.reshape(height,width),
            'valid':valid.reshape(height,width),'blur_px':blur_px,
            'cpu_s':(time.process_time_ns()-start)*1e-9,
            'origin':origin,'rotation':R,'focal_px':focal_px,
            'model':'synthetic pinhole, procedural texture and Gaussian exposure surrogate'}
