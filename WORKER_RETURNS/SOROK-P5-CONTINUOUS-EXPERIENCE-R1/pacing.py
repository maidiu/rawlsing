"""Translate admitted P5 conduct into the received S46 interval contract."""


class CoPresentProduct:
    """Keep S46's BP4 writer, adding the user to actual repair observers."""

    def __init__(self, session):
        self.session = session
        self.product = session.product

    def __getattr__(self, name):
        return getattr(self.product, name)

    def repair(self, actor):
        result = self.product.repair(actor=actor)
        if result.get("status") == "OK" and self.session.scene_open():
            event = self.session.event(result["event_id"])
            self.session._perceive_if_present(event, self.session.meta["user_actor"])
        return result


class ObservedInterval:
    """S46 session adapter. The received producer still owns time and writes."""

    def __init__(self, session):
        self.session = session
        self.product = CoPresentProduct(session)

    def __getattr__(self, name):
        return getattr(self.session, name)


def advance_for_action(fanin, action):
    # Bounded workshop ticks. A glance or short remark occupies one beat;
    # examining the work occupies three. No gaze input reaches this seam.
    span = {"ATTEND": 1, "SAY": 1, "INSPECT": 3, "INSPECT_EDGE": 3}[action["operation"]]
    session = fanin.session
    start = session.clock()
    # A deliberately sustained examination delegates two bounded work
    # periods. S46 decides whether its independent work can proceed in each.
    segments = ((start, start + span),)
    if action.get("thorough"):
        segments += ((start + span, start + 2 * span),)
    end = segments[-1][1]
    root = session.read_root()
    domain = fanin.deps["make_domain"](
        mode="ACTUAL", start=start, end=end, segments=segments,
        actor_id=root["actor_ids"][0], branch_id=session.branch_id,
    )
    from s46.producer import produce_interval

    return produce_interval(ObservedInterval(session), domain)
