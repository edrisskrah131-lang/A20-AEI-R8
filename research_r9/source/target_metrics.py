"""Fixed engineering targets and offline task scoring, separate from policy choice.

The planned pose belongs to the prescribed route, not a localization oracle.
Each target is a retained face/barycentric CAD address. It is planned before
the stochastic map transform, sensing, localization and any policy outcome.
"""
import numpy as np
from camera_renderer import camera_frame, EXTRINSIC

def planned_gimbal(nominal_mesh, planned_pose, exp):
    """Aim at a CAD patch using only the prescribed engineering route and map."""
    body=exp(planned_pose[3:])
    origin=planned_pose[:3]+body@EXTRINSIC
    _, ix=nominal_mesh.prior.tree.query(origin)
    aim=nominal_mesh.prior.points[ix]-origin
    forward=aim/np.linalg.norm(aim)
    side=np.cross(np.array([0.,0.,1.]),forward)
    if np.linalg.norm(side)<1e-8:side=np.cross(np.array([0.,1.,0.]),forward)
    side/=np.linalg.norm(side)
    up=np.cross(forward,side)
    world=np.column_stack([forward,side,up])
    return body.T@world

def plan_targets(nominal_mesh, planned_pose, exp, focal_px=1800., target_radius_px=128.,gimbal_R=None):
    origin, R = camera_frame(planned_pose, exp,gimbal_R)
    offsets = np.array([(u, v) for u in (-1., -.5, 0., .5, 1.)
                        for v in (-.75, 0., .75)]) * target_radius_px
    ray = np.c_[np.ones(len(offsets)), -offsets / focal_px]
    ray /= np.linalg.norm(ray, axis=1)[:, None]
    direction = ray @ R.T
    distance, faces = nominal_mesh.cast(np.repeat(origin[None, :], len(ray), axis=0), direction)
    valid = (faces >= 0) & np.isfinite(distance) & (distance > .3)
    faces = faces[valid]
    points = origin + direction[valid] * distance[valid, None]
    triangle = nominal_mesh.v[nominal_mesh.f[faces]]
    bary = []
    for t, p in zip(triangle, points):
        pair = np.linalg.lstsq((t[1:] - t[0]).T, p - t[0], rcond=None)[0]
        bary.append([1 - pair.sum(), *pair])
    return dict(faces=faces, bary=np.array(bary).reshape(-1, 3),
                cad_points=points, planned_offsets_px=offsets[valid])

def target_geometry(mesh, targets, pose, map_t, map_R, exp, focal_px, speed_m_s, exposure_s,gimbal_R=None):
    """Pure task quantities independent of raster ROI and selected policy."""
    origin, R = camera_frame(pose, exp,gimbal_R)
    faces = targets['faces']
    triangle = mesh.v[mesh.f[faces]]
    local = np.einsum('ni,nij->nj', targets['bary'], triangle)
    world = local @ map_R.T + map_t
    delta = world - origin
    distance = np.linalg.norm(delta, axis=1)
    rays = delta / np.maximum(distance[:, None], 1e-12)
    incidence = np.abs(np.einsum('ij,ij->i', mesh.n[faces] @ map_R.T, rays))
    gsd = distance / (focal_px * np.maximum(incidence, 1e-12))
    rel = delta @ R
    xy = -focal_px * rel[:, 1:] / np.maximum(rel[:, :1], 1e-12)
    d, hit = mesh.cast(np.repeat(((origin-map_t) @ map_R)[None, :], len(faces), axis=0),
                       rays @ map_R)
    visible = np.isfinite(d) & (np.abs(d-distance) < .003) & (rel[:, 0] > .3)
    # Fixed-target GSD and blur depend on target geometry, not on ROI coverage.
    return dict(local=local, world=world, xy=xy, visible=visible, gsd=gsd,
                blur=speed_m_s*exposure_s/np.maximum(gsd, 1e-12), distance=distance)

def score_image(frame, geometry, width, height):
    xy = geometry['xy']
    inside = (np.abs(xy[:, 0]) < width/2-.5) & (np.abs(xy[:, 1]) < height/2-.5)
    seen = geometry['visible'] & inside
    # Pixel evidence is checked at the projected target; successful geometry
    # alone cannot produce an acquired-image success without actual pixels.
    pixel_count = 0
    for p, okay in zip(xy, seen):
        if okay:
            col = int(np.floor(p[0]+width/2))
            row = int(np.floor(p[1]+height/2))
            if frame['valid'][row, col]:
                pixel_count += 1
    count = len(xy)
    return dict(gsd_m=float(np.max(geometry['gsd'])) if count else np.inf,
                blur_px=float(np.max(geometry['blur'])) if count else np.inf,
                coverage=pixel_count/count if count else 0., targets=count,
                acquired_targets=pixel_count)

def score_association(state, targets, geometry, exp, width, height, focal_px,gimbal_R=None):
    """Predict CAD-target pixels using the active causal localization state."""
    pose = np.r_[state.t, np.zeros(3)]
    # camera_frame takes a pose rotation vector; supply the state matrix directly.
    def state_exp(_): return state.R
    origin, R = camera_frame(pose, state_exp,gimbal_R)
    predicted = targets['cad_points'] @ state.mR.T + state.mt
    rel = (predicted-origin) @ R
    xy = -focal_px*rel[:, 1:] / np.maximum(rel[:, :1], 1e-12)
    inside = (np.abs(geometry['xy'][:, 0]) < width/2-.5) & (np.abs(geometry['xy'][:, 1]) < height/2-.5)
    valid = geometry['visible'] & inside & (rel[:, 0] > .3)
    if not len(xy) or not np.any(valid):
        return {'reprojection_px':np.inf, 'association_m':np.inf}
    pixel_error = np.linalg.norm(xy-geometry['xy'], axis=1)
    # Surface association error is the predicted target's displacement from
    # its physical counterpart, not pixel error multiplied by guessed GSD.
    spatial_error = np.linalg.norm(predicted-geometry['world'], axis=1)
    return dict(reprojection_px=float(np.max(pixel_error[valid])),
                association_m=float(np.max(spatial_error[valid])))
