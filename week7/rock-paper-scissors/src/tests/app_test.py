import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['session_id'] = 'test-session'
        yield client


class TestIndexRoute:
    def test_index_returns_200(self, client):
        """Test that the index page loads successfully."""
        response = client.get('/')
        assert response.status_code == 200

    def test_index_contains_game_title(self, client):
        """Test that the index page contains the game title."""
        response = client.get('/')
        assert b'Rock Paper Scissors' in response.data


class TestStartGameAPI:
    def test_start_game_basic_ai(self, client):
        """Test starting a game with basic AI."""
        response = client.post('/api/start', 
                               json={'ai_type': 'basic'},
                               content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'started'
        assert data['ai_type'] == 'basic'

    def test_start_game_improved_ai(self, client):
        """Test starting a game with improved AI."""
        response = client.post('/api/start',
                               json={'ai_type': 'improved'},
                               content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'started'
        assert data['ai_type'] == 'improved'

    def test_start_game_default_ai(self, client):
        """Test starting a game without specifying AI type defaults to basic."""
        response = client.post('/api/start',
                               json={},
                               content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['ai_type'] == 'basic'


class TestPlayAPI:
    def test_play_rock(self, client):
        """Test playing rock."""
        # Start a game first
        client.post('/api/start', json={'ai_type': 'basic'})
        
        response = client.post('/api/play',
                               json={'move': 'r'},
                               content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['player_move'] == 'Rock'
        assert data['ai_move'] in ['Rock', 'Paper', 'Scissors']
        assert data['result'] in ['win', 'lose', 'draw']

    def test_play_paper(self, client):
        """Test playing paper."""
        client.post('/api/start', json={'ai_type': 'basic'})
        
        response = client.post('/api/play',
                               json={'move': 'p'},
                               content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['player_move'] == 'Paper'

    def test_play_scissors(self, client):
        """Test playing scissors."""
        client.post('/api/start', json={'ai_type': 'basic'})
        
        response = client.post('/api/play',
                               json={'move': 's'},
                               content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['player_move'] == 'Scissors'

    def test_play_invalid_move(self, client):
        """Test that invalid moves return an error."""
        client.post('/api/start', json={'ai_type': 'basic'})
        
        response = client.post('/api/play',
                               json={'move': 'x'},
                               content_type='application/json')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_play_updates_score(self, client):
        """Test that playing updates the score."""
        client.post('/api/start', json={'ai_type': 'basic'})
        
        response = client.post('/api/play',
                               json={'move': 'r'},
                               content_type='application/json')
        data = response.get_json()
        
        # Score should have changed (either player, ai, or draws increased)
        total_score = data['score']['player'] + data['score']['ai'] + data['score']['draws']
        assert total_score == 1


class TestScoreAPI:
    def test_get_score(self, client):
        """Test getting the score."""
        client.post('/api/start', json={'ai_type': 'basic'})
        
        response = client.get('/api/score')
        assert response.status_code == 200
        data = response.get_json()
        assert 'player' in data
        assert 'ai' in data
        assert 'draws' in data

    def test_score_starts_at_zero(self, client):
        """Test that score starts at zero after new game."""
        client.post('/api/start', json={'ai_type': 'basic'})
        
        response = client.get('/api/score')
        data = response.get_json()
        assert data['player'] == 0
        assert data['ai'] == 0
        assert data['draws'] == 0


class TestGameLogic:
    def test_multiple_rounds(self, client):
        """Test playing multiple rounds without triggering game over."""
        client.post('/api/start', json={'ai_type': 'basic'})
        
        # Play a few rounds (less than 5 wins for either side)
        rounds_played = 0
        for _ in range(2):
            response = client.post('/api/play',
                                   json={'move': 'r'},
                                   content_type='application/json')
            if response.status_code == 200:
                rounds_played += 1
        
        # We should have played at least some rounds
        response = client.get('/api/score')
        data = response.get_json()
        total = data['player'] + data['ai'] + data['draws']
        assert total >= 1

    def test_new_game_resets_score(self, client):
        """Test that starting a new game resets the score."""
        client.post('/api/start', json={'ai_type': 'basic'})
        
        # Play some rounds
        for _ in range(2):
            client.post('/api/play', json={'move': 'r'})
        
        # Start new game
        client.post('/api/start', json={'ai_type': 'basic'})
        
        # Score should be reset
        response = client.get('/api/score')
        data = response.get_json()
        assert data['player'] == 0
        assert data['ai'] == 0
        assert data['draws'] == 0


class TestGameOver:
    def test_game_ends_at_3_wins(self, client):
        """Test that the game ends when a player reaches 3 wins."""
        client.post('/api/start', json={'ai_type': 'basic'})
        
        # Keep playing until game is over
        game_over = False
        rounds = 0
        max_rounds = 50  # Safety limit
        
        while not game_over and rounds < max_rounds:
            response = client.post('/api/play',
                                   json={'move': 'r'},
                                   content_type='application/json')
            data = response.get_json()
            
            if data.get('game_over'):
                game_over = True
                # Verify winner has 5 wins
                if data['winner'] == 'player':
                    assert data['score']['player'] == 3
                else:
                    assert data['score']['ai'] == 3
            rounds += 1
        
        assert game_over, "Game should end when someone reaches 3 wins"

    def test_cannot_play_after_game_over(self, client):
        """Test that you cannot play after the game is over."""
        client.post('/api/start', json={'ai_type': 'basic'})
        
        # Play until game over
        for _ in range(50):
            response = client.post('/api/play', json={'move': 'r'})
            data = response.get_json()
            if data.get('game_over'):
                break
        
        # Try to play again - should get error
        response = client.post('/api/play', json={'move': 'r'})
        assert response.status_code == 400
        data = response.get_json()
        assert data.get('game_over') == True

    def test_response_includes_game_over_status(self, client):
        """Test that play response includes game_over field."""
        client.post('/api/start', json={'ai_type': 'basic'})
        
        response = client.post('/api/play', json={'move': 'r'})
        data = response.get_json()
        
        assert 'game_over' in data

    def test_start_game_includes_wins_needed(self, client):
        """Test that start game response includes wins_needed."""
        response = client.post('/api/start', json={'ai_type': 'basic'})
        data = response.get_json()
        
        assert 'wins_needed' in data
        assert data['wins_needed'] == 3
