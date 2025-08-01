from unittest.mock import mock_open, patch

import pytest
from attendance_m2 import User, AttendanceSystem, FileLoader

def test():
    assert True

def test_user_attendance_and_points():
    user = User("alice")
    user.add_attendance(0, 1)
    user.add_attendance(2, 3)
    user.add_attendance(5, 2)

    assert user.attendance_user == [1, 0, 1, 0, 0, 1, 0]
    assert user.points == 6
    assert user.weekday_count == 1
    assert user.weekend_count == 1

def test_user_bonus_and_grade():
    user = User("bob")
    for _ in range(10):
        user.add_attendance(3, 1)

    for _ in range(5):
        user.add_attendance(5, 2)
        user.add_attendance(6, 2)

    user.apply_bonus()
    user.evaluate_grade()

    assert user.points == 50
    assert user.grade == "GOLD"

def test_attendance_system_record_and_finalize():
    system = AttendanceSystem()
    system.record_attendance("alice", "monday")

    assert len(system.users) == 1
    system.finalize()

    alice = system.users["alice"]
    assert alice.grade in ("NORMAL", "SILVER", "GOLD")


def test_inactive():
    user = User("cho")
    user.add_attendance(0, 1)
    user.evaluate_grade()
    assert user.is_inactive() is True

