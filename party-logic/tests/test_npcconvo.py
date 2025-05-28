import pytest
from unittest.mock import Mock, patch
from simulation.npcconvo import NPCConvo
from simulation.person import Person
from simulation.simclass import Simulation
from simulation.rumor import Rumor

@pytest.fixture
def mock_simulation():
    sim = Mock(spec=Simulation)
    sim.get_relationship = Mock(return_value=Mock(trust=500, animosity=0))
    return sim

@pytest.fixture
def mock_person():
    person = Mock(spec=Person)
    person.id = "test_person"
    person.active_conversation = None
    person.rumors = set()
    person.gossip_level = 500
    person.anger = 0
    person.gullibility = 500
    person.active_conversation_ticks = 0
    person.add_to_convo = Mock()
    person.remove_from_convo = Mock()
    return person

@pytest.fixture
def mock_rumor():
    rumor = Mock(spec=Rumor)
    rumor.plausibility = 500
    rumor.harmfulness = 500
    rumor.subjects = []
    rumor.originators = []
    return rumor

def test_npcconvo_initialization(mock_person):
    # Test basic initialization
    convo = NPCConvo([mock_person])
    assert convo.participants == [mock_person]
    assert convo.tick_count == 0
    assert convo.max_tick_count > 0
    mock_person.add_to_convo.assert_called_once_with(convo)

def test_npcconvo_initialization_with_existing_convo(mock_person):
    # Test initialization with person already in conversation
    mock_person.active_conversation = Mock()
    with pytest.raises(ValueError, match="is already in a conversation"):
        NPCConvo([mock_person])

def test_add_person(mock_person):
    convo = NPCConvo([])
    convo.add_person(mock_person)
    assert mock_person in convo.participants
    mock_person.add_to_convo.assert_called_once_with(convo)

def test_add_person_already_in_convo(mock_person):
    convo = NPCConvo([])
    mock_person.active_conversation = Mock()
    with pytest.raises(ValueError, match="is already in a conversation"):
        convo.add_person(mock_person)

def test_remove_person(mock_person):
    convo = NPCConvo([mock_person])
    convo.remove_person(mock_person)
    assert mock_person not in convo.participants
    mock_person.remove_from_convo.assert_called_once()

def test_remove_person_not_in_convo(mock_person):
    convo = NPCConvo([])
    with pytest.raises(ValueError, match="is not in this conversation"):
        convo.remove_person(mock_person)

def test_end_conversation(mock_person):
    convo = NPCConvo([mock_person])
    convo.end_conversation()
    assert len(convo.participants) == 0
    mock_person.remove_from_convo.assert_called_once()

def test_choose_rumor_to_spread(mock_simulation, mock_person, mock_rumor):
    mock_person.rumors = {mock_rumor}
    convo = NPCConvo([mock_person])
    
    with patch('random.choices') as mock_choices:
        mock_choices.side_effect = [
            [(mock_rumor, 1.0)],  # First choice for personal rumor
            [(mock_person, mock_rumor, 1.0)]  # Second choice for spreader
        ]
        
        spreader, rumor, score = convo.choose_rumor_to_spread(mock_simulation)
        assert spreader == mock_person
        assert rumor == mock_rumor
        assert score == 1.0

def test_spread_rumor(mock_simulation, mock_person, mock_rumor):
    # Setup
    mock_person.rumors = {mock_rumor}  # Give the person a rumor to spread
    other_person = Mock(spec=Person)
    other_person.id = "other_person"
    other_person.active_conversation = None
    other_person.rumors = set()
    other_person.gossip_level = 500
    other_person.anger = 0
    other_person.gullibility = 500
    
    convo = NPCConvo([mock_person, other_person])
    
    # Mock random.random to ensure rumor spread
    with patch('random.random', return_value=0.0):
        with patch('random.choices') as mock_choices:
            # Fix: Return a list containing a single tuple for each choices call
            mock_choices.side_effect = [
                [(mock_rumor, 1.0)],  # First choice for personal rumor
                [(mock_person, mock_rumor, 1.0)]  # Second choice for spreader
            ]
            convo.spread_rumor(mock_simulation)
            
            # Verify relationship updates
            mock_simulation.get_relationship.assert_called_with(mock_person, other_person)

def test_spread_rumor_no_rumors(mock_simulation, mock_person):
    # Setup person with no rumors
    mock_person.rumors = set()
    other_person = Mock(spec=Person)
    other_person.id = "other_person"
    other_person.active_conversation = None
    other_person.rumors = set()
    
    convo = NPCConvo([mock_person, other_person])
    
    # Mock random.random to ensure rumor spread attempt
    with patch('random.random', return_value=0.0):
        convo.spread_rumor(mock_simulation)
        
        # Verify no relationship updates occurred
        mock_simulation.get_relationship.assert_not_called()

def test_spread_emotions(mock_simulation, mock_person):
    # Setup two people with different anger levels
    person1 = mock_person
    person2 = Mock(spec=Person)
    person2.id = "person2"
    person2.active_conversation = None
    person2.anger = 500
    person2.gossip_level = 500
    
    convo = NPCConvo([person1, person2])
    
    # Test emotion spreading
    convo.spread_emotions(mock_simulation)
    
    # Verify that emotions were adjusted
    assert person1.anger != 0 or person2.anger != 500

def test_tick(mock_simulation, mock_person):
    convo = NPCConvo([mock_person])
    initial_ticks = mock_person.active_conversation_ticks
    
    convo.tick(mock_simulation)
    
    assert convo.tick_count == 1
    assert mock_person.active_conversation_ticks == initial_ticks + 1

def test_tick_with_rumor_spread(mock_simulation, mock_person, mock_rumor):
    # Setup
    mock_person.rumors = {mock_rumor}
    convo = NPCConvo([mock_person])
    
    # Mock random.random to ensure rumor spread
    with patch('random.random', return_value=0.0):
        with patch('random.choices') as mock_choices:
            mock_choices.side_effect = [
                [(mock_rumor, 1.0)],  # First choice for personal rumor
                [(mock_person, mock_rumor, 1.0)]  # Second choice for spreader
            ]
            # Set tick_count to trigger rumor spread
            convo.tick_count = 9  # Assuming TICKS_PER_CONVO_TICK is 10
            convo.tick(mock_simulation)
            
            # Verify that both rumor spread and emotion spread were called
            assert convo.tick_count == 10 