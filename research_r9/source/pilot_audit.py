"""Read back actual paired raster outputs; counts are unique pilot seeds."""
import json
import numpy as np
from runtime import HERE
from prospective_protocol import sha

def main():
    folder=HERE/'data/pilot_v4'
    manifest=json.loads((folder/'manifest.json').read_text())
    for name,h in manifest['files'].items():
        if sha(folder/name)!=h:raise RuntimeError('Changed pilot asset: '+name)
    records=[json.loads(p.read_text()) for p in sorted(folder.glob('12*.json'))]
    differences=[];paired=[]
    for r in records:
        seed=r['seed']
        with np.load(folder/f'{seed}_native_roi.npz') as old,np.load(folder/f'{seed}_wide_roi.npz') as new:
            assert np.array_equal(old['target_faces'],new['target_faces'])
            assert np.array_equal(old['target_bary'],new['target_bary'])
            assert np.array_equal(old['target_cad'],new['target_cad'])
            differences.append(float(np.max(np.abs(old['target_gsd']-new['target_gsd']))) if len(old['target_gsd']) else 0.)
            assert old['rgb'].shape==(144,192,3) and new['rgb'].shape==(216,288,3)
        a,b=r['cameras'];paired.append(dict(seed=seed,mesh=r['mesh'],native_coverage=a['coverage'],
            wide_coverage=b['coverage'],native_cpu_s=a['cpu_s'],wide_cpu_s=b['cpu_s']))
    assert len({r['seed'] for r in records})==48
    audit=dict(status='PASS',unique_pilot_seeds=48,excluded_from_inference=True,
        pilot_archive_files=len(manifest['files']),paired_fixed_target_GSD_max_difference=max(differences),
        target_identity_unchanged=True,actual_RGB_raster_shapes_verified=True,
        native_coverage_median=float(np.median([r['native_coverage'] for r in paired])),
        wide_coverage_median=float(np.median([r['wide_coverage'] for r in paired])),
        timing_resolution_note='Native Windows thread/process CPU counter samples show 15.625-ms quantization. '
            'Pilot medians characterize the declared simulation clock only; not embedded runtime guarantees.',
        formal_calibration_inputs=0,formal_confirmation_inputs=0,paired=paired)
    (HERE/'audits/pilot_v4_audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in audit.items() if k!='paired'}),flush=True)

if __name__=='__main__':main()
