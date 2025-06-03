import pytest
from simulation.rumor import Rumor

def test_rumor_initialization():
    rumor = Rumor()
    assert rumor.id is not None
    assert rumor.is_really_true is True
    assert rumor.text == ''
    assert rumor.hash_text == ''
    assert rumor.plausibility == 500
    assert rumor.harmfulness == 500
    assert rumor.self_conceal_score == 500
    assert rumor.subjects == []
    assert rumor.originators == []

def test_rumor_initialization_with_values():
    rumor = Rumor(
        id="test-rumor-123",
        is_really_true=False,
        text="This is a test rumor",
        hash_text="Test hash",
        plausibility=300,
        harmfulness=700,
        self_conceal_score=600,
        subjects=["person1", "person2"],
        originators=["person3"]
    )
    assert rumor.id == "test-rumor-123"
    assert rumor.is_really_true is False
    assert rumor.text == "This is a test rumor"
    assert rumor.hash_text == "Test hash"
    assert rumor.plausibility == 300
    assert rumor.harmfulness == 700
    assert rumor.self_conceal_score == 600
    assert rumor.subjects == ["person1", "person2"]
    assert rumor.originators == ["person3"]

def test_rumor_from_json():
    # Create a mock subject to pass in
    class MockPerson:
        def __init__(self, id):
            self.id = id
    
    mock_subject = MockPerson("test-person")
    rumor = Rumor(from_json="rumor-test-secret-1.json", subjects=[mock_subject])
    assert rumor.id == "test-secret-1"
    assert rumor.is_really_true is True
    assert rumor.text == "This is a test secret"
    assert rumor.plausibility == 500
    assert rumor.harmfulness == 300
    assert rumor.self_conceal_score == 500
    assert rumor.subjects == [mock_subject]
    assert rumor.originators == []  # Always empty when loading from JSON

def test_rumor_from_json_no_subjects():
    # Test loading without passing subjects
    rumor = Rumor(from_json="rumor-test-secret-1.json")
    assert rumor.subjects == []  # Should be empty if no subjects passed
    assert rumor.originators == []  # Always empty when loading from JSON

def test_rumor_pretty_print(capsys):
    rumor = Rumor(id="test123", text="Test rumor", plausibility=600, harmfulness=400)
    rumor.pretty_print()
    captured = capsys.readouterr()
    assert "Rumor:" in captured.out
    assert "ID: test123" in captured.out
    assert "Text: Test rumor" in captured.out
    assert "Plausibility: 600" in captured.out
    assert "Harmfulness: 400" in captured.out
    assert "Subjects: None" in captured.out
    assert "Originators: None" in captured.out 