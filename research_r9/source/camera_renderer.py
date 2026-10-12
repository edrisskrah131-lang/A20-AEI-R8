"""Actual synthetic pinhole raster; no generated photograph or measured CAD claim."""
import time
import numpy as np
from scipy.ndimage import gaussian_filter

EXTRINSIC = np.array([.15, 0., .75])

def target_colors(n):
    import colorsys
    return np.array([np.array(colorsys.hsv_to_rgb((i*.61803398875)%1.,.88,.94))*255.
                     for i in range(n)])

def detect_fiducials(rgb,n):
    """Read synthetic uniquely colored CAD landmarks from raster pixels only."""
    begin=time.thread_time_ns()
    colors=target_colors(n)
    chroma=rgb.max(axis=2).astype(float)-rgb.min(axis=2)
    centers=np.full((n,2),np.nan)
    if not n:return centers,(time.thread_time_ns()-begin)*1e-9
    distance=np.linalg.norm(rgb[:,:,None,:].astype(float)-colors[None,None,:,:],axis=3)
    labels=np.argmin(distance,axis=2)
    best=np.min(distance,axis=2)
    for i,color in enumerate(colors):
        difference=distance[:,:,i]
        mask=(labels==i)&(best<65.) & (chroma>90.)
        row,col=np.nonzero(mask)
        if len(row)>=2:
            weights=1./np.maximum(difference[row,col],1.)
            centers[i]=[np.average(col+.5-rgb.shape[1]/2,weights=weights),
                        np.average(row+.5-rgb.shape[0]/2,weights=weights)]
    return centers,(time.thread_time_ns()-begin)*1e-9

def camera_frame(pose, exp, gimbal_R=None):
    body = exp(pose[3:])
    angle = -.12
    pitch = np.array([[np.cos(angle),0,np.sin(angle)], [0,1,0],
                      [-np.sin(angle),0,np.cos(angle)]])
    return pose[:3]+body@EXTRINSIC, body@(pitch if gimbal_R is None else gimbal_R)

def render(mesh, pose, map_t, map_R, rng, exp, width=192, height=144,
           focal_px=1800., exposure_s=.006, speed_m_s=.15, gimbal_R=None,target_geometry=None):
    start = time.thread_time_ns()
    wall = time.perf_counter_ns()
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
    if target_geometry is not None:
        # A projected 25-mm-radius synthetic fiducial at each known CAD patch.
        # This is a diagnostic landmark task, not a model of crack detection.
        colors=target_colors(len(target_geometry['xy']))
        raster_range=distance.reshape(height,width)
        for i,xy in enumerate(target_geometry['xy']):
            if not target_geometry['visible'][i]:continue
            radius=.025/max(target_geometry['gsd'][i],1e-12)
            mask=((u-xy[0])**2+(v-xy[1])**2<=radius**2)
            mask&=np.isfinite(raster_range)&(np.abs(raster_range-target_geometry['distance'][i])<.075)
            image[mask]=colors[i]
    if np.isfinite(blur_px) and blur_px > .05:
        image = gaussian_filter(image, sigma=(blur_px/np.sqrt(12),blur_px/np.sqrt(12),0))
    image += rng.normal(0,.8,image.shape)
    image = np.clip(np.rint(image),0,255).astype(np.uint8)
    return {'rgb':image,'distance':distance.reshape(height,width),
            'face':face.reshape(height,width),'gsd_m':gsd.reshape(height,width),
            'valid':valid.reshape(height,width),'blur_px':blur_px,
            'cpu_s':(time.thread_time_ns()-start)*1e-9,'wall_s':(time.perf_counter_ns()-wall)*1e-9,
            'origin':origin,'rotation':R,'focal_px':focal_px,
            'model':'synthetic pinhole, procedural texture, 25-mm-radius diagnostic fiducials and Gaussian exposure surrogate'}
