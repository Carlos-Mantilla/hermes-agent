"""La próxima corrida usa la zona IANA, no el offset de hoy.

`0 9 7 * *` calculado el 17-oct (EDT, -04) tiene que caer a las 09:00-05:00
el 7-nov. En marzo 2027, calculado el 1-mar (EST, -05), el 20 cae a las
09:00-04:00. croniter, si recibe el datetime de hoy, se queda con el offset
de hoy y mueve la hora una hora.
"""
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

pytest.importorskip("croniter")

from cron.jobs import compute_next_run

NY = ZoneInfo("America/New_York")


def test_7_nov_es_las_9_en_hora_estandar(monkeypatch):
    ahora = datetime(2026, 10, 17, 15, 0, tzinfo=NY)
    monkeypatch.setattr("cron.jobs._hermes_now", lambda: ahora)
    got = compute_next_run({"kind": "cron", "expr": "0 9 7 * *"})
    assert got == "2026-11-07T09:00:00-05:00"


def test_marzo_2027_no_hereda_el_offset_de_invierno(monkeypatch):
    ahora = datetime(2027, 3, 1, 12, 0, tzinfo=NY)
    monkeypatch.setattr("cron.jobs._hermes_now", lambda: ahora)
    got = compute_next_run({"kind": "cron", "expr": "0 9 20 * *"})
    assert got == "2027-03-20T09:00:00-04:00"
