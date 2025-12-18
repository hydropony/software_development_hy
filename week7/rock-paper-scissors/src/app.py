from flask import Flask, render_template, request, jsonify, session
from referee import Referee
from rps_factory import create_game

app = Flask(__name__)
app.secret_key = 'rock-paper-scissors-secret-key'

# Map web AI types to factory game types
AI_TYPE_MAP = {
    'basic': 'b',
    'improved': 'c'
}

# Store game states per session
games = {}


def get_game_state(session_id):
    """Get or create game state for a session."""
    if session_id not in games:
        games[session_id] = {
            'referee': Referee(),
            'ai': None,
            'ai_type': None
        }
    return games[session_id]


def reset_game(session_id, ai_type='basic'):
    """Reset the game with specified AI type."""
    factory_type = AI_TYPE_MAP.get(ai_type, 'b')
    game = create_game(factory_type)
    
    games[session_id] = {
        'referee': Referee(),
        'ai': game.ai,
        'ai_type': ai_type
    }
    return games[session_id]


@app.route('/')
def index():
    """Render the main game page."""
    if 'session_id' not in session:
        import uuid
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')


@app.route('/api/start', methods=['POST'])
def start_game():
    """Start a new game with the specified AI type."""
    session_id = session.get('session_id', 'default')
    data = request.get_json() or {}
    ai_type = data.get('ai_type', 'basic')
    
    reset_game(session_id, ai_type)
    
    return jsonify({
        'status': 'started',
        'ai_type': ai_type,
        'message': f'Game started against {"Improved AI" if ai_type == "improved" else "Basic AI"}!',
        'wins_needed': WINS_TO_END
    })


WINS_TO_END = 3


@app.route('/api/play', methods=['POST'])
def play():
    """Play a move and get the AI's response."""
    session_id = session.get('session_id', 'default')
    game_state = get_game_state(session_id)
    
    if game_state['ai'] is None:
        reset_game(session_id, 'basic')
        game_state = get_game_state(session_id)
    
    referee = game_state['referee']
    
    # Check if game is already over
    if referee.first_player_points >= WINS_TO_END or referee.second_player_points >= WINS_TO_END:
        return jsonify({
            'error': 'Game is over. Start a new game.',
            'game_over': True,
            'winner': 'player' if referee.first_player_points >= WINS_TO_END else 'ai'
        }), 400
    
    data = request.get_json()
    player_move = data.get('move', '').lower()
    
    if player_move not in ['r', 'p', 's']:
        return jsonify({'error': 'Invalid move. Use r, p, or s.'}), 400
    
    # Get AI's move
    ai_move = game_state['ai'].get_move()
    
    # For improved AI, record the player's move
    game_state['ai'].set_move(player_move)
    
    # Record the moves in the referee
    referee.record_move(player_move, ai_move)
    
    # Determine round result
    if player_move == ai_move:
        result = 'draw'
    elif referee._first_wins(player_move, ai_move):
        result = 'win'
    else:
        result = 'lose'
    
    # Check if game is now over
    game_over = False
    winner = None
    if referee.first_player_points >= WINS_TO_END:
        game_over = True
        winner = 'player'
    elif referee.second_player_points >= WINS_TO_END:
        game_over = True
        winner = 'ai'
    
    move_names = {'r': 'Rock', 'p': 'Paper', 's': 'Scissors'}
    
    return jsonify({
        'player_move': move_names[player_move],
        'ai_move': move_names[ai_move],
        'result': result,
        'score': {
            'player': referee.first_player_points,
            'ai': referee.second_player_points,
            'draws': referee.draws
        },
        'game_over': game_over,
        'winner': winner,
        'wins_needed': WINS_TO_END
    })


@app.route('/api/score', methods=['GET'])
def get_score():
    """Get the current score."""
    session_id = session.get('session_id', 'default')
    game_state = get_game_state(session_id)
    referee = game_state['referee']
    
    game_over = referee.first_player_points >= WINS_TO_END or referee.second_player_points >= WINS_TO_END
    winner = None
    if referee.first_player_points >= WINS_TO_END:
        winner = 'player'
    elif referee.second_player_points >= WINS_TO_END:
        winner = 'ai'
    
    return jsonify({
        'player': referee.first_player_points,
        'ai': referee.second_player_points,
        'draws': referee.draws,
        'ai_type': game_state.get('ai_type', 'none'),
        'game_over': game_over,
        'winner': winner,
        'wins_needed': WINS_TO_END
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
