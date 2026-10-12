"""Source-bound use of sealed compiled plans; no change to numerical events."""
from dataclasses import dataclass
from event_semantics import digest

@dataclass(frozen=True)
class TrustedSource:
    scope: str
    seal: str
    profile: str
    study: str

class ReceiptGate:
    def __init__(self,method,shared_history=None):
        self.method=method
        self.history={} if shared_history is None else shared_history

    @staticmethod
    def packet(plan,source):
        return dict(source=source.scope,source_seal=source.seal,profile=source.profile,
            study=source.study,policy=plan['policy'],event_id=plan['event_id'],
            plan_seal=digest(plan),card=plan.get('card'))

    def issue(self,plan,source,packet):
        key=(self.method,source.scope)
        if plan['status']!='AUTHORIZED':return dict(issued=False,status='REFUSED',upper=None)
        expected=self.packet(plan,source)
        if self.method=='ProceduralCoverValidated':
            valid=(packet.get('source')==source.scope and packet.get('source_seal')==source.seal
              and packet.get('profile')==source.profile and packet.get('study')==source.study
              and packet.get('policy')==plan['policy'] and packet.get('event_id')==plan['event_id']
              and packet.get('plan_seal')==expected['plan_seal'] and packet.get('card')==plan.get('card'))
        else:
            valid=all(packet.get(k)==v for k,v in expected.items())
        valid=bool(valid and (source.profile,source.study)==(plan['profile'],plan['study']))
        self.history[key]=self.history.get(key,True) and valid
        if not self.history[key]:return dict(issued=False,status='PROVISIONAL',upper=None)
        return dict(issued=True,status='AUTHORIZED',upper=plan['upper'])
