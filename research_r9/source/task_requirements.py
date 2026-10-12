"""Declared synthetic service requirements; not physical inspection standards."""
from event_semantics import Atom,Event,digest

TASKS=('acquisition','association','report')
VARIANTS=('full','coarser_gsd','more_blur','partial','partial_relaxed',
          'stricter','late_report','single_service')
POLICIES=('Fixed2','Fixed4','Final','FlatCART','FlatRF','KG1','ContractRF','OldRAVC')
ALLOWANCES=(.10,.15,.20,.25)
ANCHORS=('full','partial','single_service')

def requirement(task,variant):
    if task not in TASKS or variant not in VARIANTS:raise ValueError('Undeclared request')
    gsd,blur,coverage,pixel,spatial,delay,age=.020,.50,.50,30.,.10,2.,1.8
    if variant=='coarser_gsd':gsd=.040
    if variant=='more_blur':blur=.75
    if variant in ('partial','partial_relaxed'):
        gsd,blur,coverage,pixel,spatial,delay,age=.040,.75,.20,50.,.15,3.,2.8
    if variant=='partial_relaxed':gsd=None;pixel=None;delay,age=4.,3.8
    if variant=='stricter':gsd,blur,coverage,pixel,spatial,delay,age=.010,.35,.70,15.,.06,1.,.8
    if variant=='late_report':delay,age=4.,3.8
    atoms={}
    if task in ('acquisition','report'):
        if gsd is not None:atoms['gsd_m']=Atom('gsd_m',upper=gsd)
        atoms['blur_px']=Atom('blur_px',upper=blur)
        atoms['coverage']=Atom('coverage',lower=coverage)
    if task in ('association','report'):
        if pixel is not None:atoms['reprojection_px']=Atom('reprojection_px',upper=pixel)
        atoms['association_m']=Atom('association_m',upper=spatial)
        atoms['localization_ready']=Atom('localization_ready',lower=1.)
        atoms['coverage']=Atom('coverage',lower=coverage)
    if task=='report':
        atoms['report_delay_s']=Atom('report_delay_s',upper=delay)
        atoms['image_age_s']=Atom('image_age_s',upper=age)
    if variant=='single_service':
        if task=='acquisition':atoms={k:Atom(k,upper=v) for k,v in [('gsd_m',.040),('blur_px',.75)]}
        elif task=='association':atoms={'association_m':Atom('association_m',upper=.15),
                                       'localization_ready':Atom('localization_ready',lower=1.)}
        else:atoms={'report_delay_s':Atom('report_delay_s',upper=3.),
                    'image_age_s':Atom('image_age_s',upper=2.8)}
    return Event(tuple(atoms.values()))

# Static functional dependencies for the frozen producer: these express known
# program data flow, not a statistical test for real-world distribution drift.
DEPENDENCIES={
 'gsd_m':('target_plan','geometry_sampler','focal_px'),
 'blur_px':('target_plan','geometry_sampler','focal_px','exposure_s','motion_sampler'),
 'coverage':('target_plan','geometry_sampler','focal_px','exposure_s','motion_sampler',
             'roi','renderer','detector','pixel_noise'),
 'reprojection_px':('target_plan','geometry_sampler','focal_px','exposure_s','motion_sampler',
                    'roi','renderer','detector','pixel_noise','localization','capture_sampler'),
 'association_m':('target_plan','geometry_sampler','localization','capture_sampler',
                  'roi','renderer','detector','pixel_noise','exposure_s','focal_px','motion_sampler'),
 'localization_ready':('localization','capture_sampler'),
 'report_delay_s':('localization','capture_sampler','camera_clock','report_queue'),
 'image_age_s':('localization','capture_sampler','camera_clock','report_queue')}

def event_capsule(event,context):
    keys=sorted({key for a in event.atoms for key in DEPENDENCIES[a.metric]})
    if any(k not in context for k in keys):raise ValueError('Missing trusted component')
    return digest({k:context[k] for k in keys})

def procedural_capsule_equal(event,old,new):
    # Independently written baseline walks the complete published dependency
    # specification; no baseline is denied any engineering knowledge.
    for atom in event.atoms:
        for field in DEPENDENCIES[atom.metric]:
            if field not in old or field not in new or old[field]!=new[field]:return False
    return True

def context(study,policy,service,clock):
    return {'target_plan':'fixed CAD face/barycentric address, 5x3 angular grid; gimbal aims at prior CAD patch',
            'geometry_sampler':'R8 retained independent mixture and stochastic map transform',
            'focal_px':1800.,'exposure_s':.006,'motion_sampler':'retained route sampler',
            'roi':(192,144) if study=='A' else (288,216),
            'renderer':'R9 frozen BVH raster and synthetic fiducial version',
            'detector':'R9 nearest-palette pixel decoder, no truth coordinates',
            'pixel_noise':'independent Gaussian pixel noise, SD 0.8 intensity',
            'localization':(policy,service,'R8 frozen models, solver and operation clock'),
            'capture_sampler':'independent uniform ticks 1,2,3 before sensing',
            'camera_clock':clock[study]['total_s'],'report_queue':.05}
