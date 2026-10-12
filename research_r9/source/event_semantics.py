"""Typed event containment. This module does not infer distribution invariance."""
from dataclasses import dataclass
import hashlib, json, math
import numpy as np
from scipy.stats import beta

UNITS = {'m': ('length', 1.), 'mm': ('length', .001), 'cm': ('length', .01),
         's': ('time', 1.), 'ms': ('time', .001), 'px': ('pixel', 1.),
         'ratio': ('ratio', 1.)}
METRICS = {'gsd_m': 'length', 'association_m': 'length', 'reprojection_px': 'pixel',
           'blur_px': 'pixel', 'coverage': 'ratio', 'report_delay_s': 'time',
           'image_age_s': 'time', 'localization_ready':'ratio'}

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                    allow_nan=False).encode()).hexdigest()

@dataclass(frozen=True)
class Atom:
    metric: str
    lower: float | None = None
    upper: float | None = None

    def __post_init__(self):
        if self.metric not in METRICS or (self.lower is None and self.upper is None):
            raise ValueError('Unknown metric or empty predicate')
        for value in (self.lower, self.upper):
            if value is not None and (isinstance(value, bool) or not isinstance(value,(int,float)) or not math.isfinite(value)):
                raise ValueError('Thresholds must be finite numbers')
        if self.lower is not None and self.upper is not None and self.lower > self.upper:
            raise ValueError('Empty admissible interval')

    @classmethod
    def quantity(cls, metric, unit, lower=None, upper=None):
        if any(v is not None and (isinstance(v,bool) or not isinstance(v,(int,float))) for v in (lower,upper)):
            raise ValueError('Quantities require numeric, non-Boolean thresholds')
        dimension, scale = UNITS[unit]
        if METRICS.get(metric) != dimension:
            raise ValueError('Incompatible engineering units')
        return cls(metric, None if lower is None else lower*scale,
                   None if upper is None else upper*scale)

@dataclass(frozen=True)
class Event:
    atoms: tuple[Atom, ...]

    def __post_init__(self):
        if not all(isinstance(a,Atom) for a in self.atoms):
            raise ValueError('Event requires typed atoms')
        if not self.atoms or len({a.metric for a in self.atoms}) != len(self.atoms):
            raise ValueError('Use one canonical interval per required metric')
        object.__setattr__(self, 'atoms', tuple(sorted(self.atoms, key=lambda a:a.metric)))

    @property
    def identity(self):
        return digest([(a.metric, a.lower, a.upper) for a in self.atoms])

    def failure(self, metrics):
        result = None
        for atom in self.atoms:
            if atom.metric not in metrics:
                raise ValueError('Required measured/scored quantity is absent')
            x = np.asarray(metrics[atom.metric], dtype=float)
            bad = ~np.isfinite(x)
            if atom.lower is not None:
                bad |= x < atom.lower
            if atom.upper is not None:
                bad |= x > atom.upper
            result = bad.copy() if result is None else result | bad
        return result

def containment(anchor: Event, requested: Event):
    """Witness that Failure(requested) is a subset of Failure(anchor)."""
    available = {a.metric:a for a in anchor.atoms}
    witness = []
    for target in requested.atoms:
        source = available.get(target.metric)
        if source is None:
            return None
        lo_a = -math.inf if source.lower is None else source.lower
        lo_t = -math.inf if target.lower is None else target.lower
        hi_a = math.inf if source.upper is None else source.upper
        hi_t = math.inf if target.upper is None else target.upper
        if lo_a < lo_t or hi_a > hi_t:
            return None
        witness.append((target.metric, source.lower, source.upper, target.lower, target.upper))
    return tuple(witness)

def procedural_contains(anchor: Event, requested: Event):
    """Independent complete procedural baseline; does not call containment()."""
    bounds = {a.metric:(a.lower,a.upper) for a in anchor.atoms}
    for atom in requested.atoms:
        if atom.metric not in bounds:
            return False
        old_min, old_max = bounds[atom.metric]
        if atom.lower is not None and (old_min is None or old_min < atom.lower):
            return False
        if atom.upper is not None and (old_max is None or old_max > atom.upper):
            return False
    return True

def cp_upper(k, n, alpha):
    if isinstance(k, bool) or isinstance(n, bool) or not isinstance(k, int) or not isinstance(n, int):
        raise ValueError('Calibration counts must be integers')
    if n < 1 or not 0 <= k <= n or not 0 < alpha < 1:
        raise ValueError('Invalid calibration counts or error budget')
    return 1. if k == n else float(beta.isf(alpha, k+1, n-k))

@dataclass(frozen=True)
class Card:
    event_id: str
    producer_id: str
    population_id: str
    calibration_manifest: str
    n: int
    k: int
    alpha: float
    upper: float

    def valid(self):
        try:
            computed = cp_upper(self.k, self.n, self.alpha)
            return bool(self.event_id and self.producer_id and self.population_id
                        and self.calibration_manifest and math.isfinite(self.upper)
                        and 0 <= self.upper <= 1 and abs(self.upper-computed) < 1e-12)
        except (TypeError, ValueError):
            return False

def authorize(card, anchor, request, trusted_producer, trusted_population, allowance,
              observation_dependent=False):
    """A before-sensing request; source-conditional claims are not authorized."""
    if not math.isfinite(allowance) or not 0 < allowance < 1:
        return {'status':'REFUSED', 'reason':'invalid_allowance'}
    if observation_dependent:
        return {'status':'REFUSED', 'reason':'needs_common_or_union_cover'}
    if not card.valid() or card.event_id != anchor.identity:
        return {'status':'REFUSED', 'reason':'invalid_card_or_event'}
    if (card.producer_id, card.population_id) != (trusted_producer, trusted_population):
        return {'status':'REFUSED', 'reason':'producer_or_population_change'}
    witness = containment(anchor, request)
    if witness is None:
        return {'status':'RECERTIFY', 'reason':'event_not_covered'}
    if card.upper > allowance:
        return {'status':'REFUSED', 'reason':'insufficient_risk_margin', 'upper':card.upper}
    return {'status':'AUTHORIZED', 'upper':card.upper, 'witness':witness,
            'calibration_manifest':card.calibration_manifest}
