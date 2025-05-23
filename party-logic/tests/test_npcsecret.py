import pytest
from simulation.npcsecret import NPCSecret

def test_npcsecret_initialization():
    secret = NPCSecret()
    assert isinstance(secret.id, str)
    assert secret.text == ''
    assert isinstance(secret.conceal_score, (int, float))
    assert secret.subject_ids == []

def test_npcsecret_initialization_with_values():
    secret = NPCSecret(
        id="test123",
        text="Test secret",
        conceal_score=500,
        subject_ids=["person1", "person2"]
    )
    assert secret.id == "test123"
    assert secret.text == "Test secret"
    assert secret.conceal_score == 500
    assert secret.subject_ids == ["person1", "person2"]

def test_npcsecret_initialization_with_randomize_stats():
    base_conceal = 500
    randomize_stats = 50
    secret = NPCSecret(conceal_score=base_conceal, randomize_stats=randomize_stats)
    assert base_conceal - randomize_stats <= secret.conceal_score <= base_conceal + randomize_stats

def test_npcsecret_from_json():
    secret = NPCSecret(from_json="npcsecret-test-npcsecret-1.json")
    assert secret.id == "test-secret-1"
    assert secret.text == "This is a test secret"
    assert secret.conceal_score == 500
    assert secret.subject_ids == ["test-person-1", "test-person-2"]

def test_npcsecret_pretty_print(capsys):
    secret = NPCSecret(id="test123", text="Test secret")
    secret.pretty_print()
    captured = capsys.readouterr()
    assert "NPCSecret:" in captured.out
    assert "ID: test123" in captured.out
    assert "Text: Test secret" in captured.out 