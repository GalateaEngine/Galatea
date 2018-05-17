import pytest
from classifier import classify


def test_answer():
    assert classify(123) == ""
    assert classify(0.2) == ""