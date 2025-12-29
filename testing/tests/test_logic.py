import pytest
from app.logic import can_vote


def test_over_age():
    assert can_vote(21,"Nepal")==True

def test_under_age():
    assert can_vote(13,"India")==False

def test_wrong_country():
    assert can_vote(45,"India")==False
