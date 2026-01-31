import google.generativeai as genai
import json
import random
import os
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT, get_user_prompt

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

class GameState:
    """Manages the game state"""
    def __init__(self):
        self.round_number = 0
        self.bomb_used_by_user = False
        self.bomb_used_by_bot = False
        self.user_score = 0
        self.bot_score = 0
        self.draws = 0
        self.game_history = []
    
    def add_round(self, user_move, bot_move, winner, reason):
        """Add a round to history"""
        self.round_number += 1
        self.game_history.append({
            'round': self.round_number,
            'user_move': user_move,
            'bot_move': bot_move,
            'winner': winner,
            'reason': reason
        })
        
        # Update scores
        if winner == 'user':
            self.user_score += 1
        elif winner == 'bot':
            self.bot_score += 1
        elif winner == 'draw':
            self.draws += 1

def generate_bot_move(game_state):
    """Generate a random valid move for the bot"""
    valid_moves = ['rock', 'paper', 'scissors']
    
    # Bot can use bomb if not used yet
    if not game_state.bomb_used_by_bot:
        # 20% chance to use bomb if available
        if random.random() < 0.2:
            game_state.bomb_used_by_bot = True
            return 'bomb'
    
    return random.choice(valid_moves)

def call_ai_judge(user_input, bot_move, game_state):
    """Call Gemini API to judge the move"""
    try:
        # Create the model
        model = genai.GenerativeModel('gemini-flash-latest')
        
        # Build the full prompt
        user_prompt = get_user_prompt(
            user_input=user_input,
            bot_move=bot_move,
            bomb_used_by_user=game_state.bomb_used_by_user,
            round_number=game_state.round_number + 1
        )
        
        full_prompt = SYSTEM_PROMPT + "\n\n" + user_prompt
        
        # Call the API
        response = model.generate_content(full_prompt)
        
        # Parse JSON response
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith('```'):
            response_text = response_text.split('```')[1]
            if response_text.startswith('json'):
                response_text = response_text[4:]
            response_text = response_text.strip()
        
        judgment = json.loads(response_text)
        
        return judgment
        
    except Exception as e:
        print(f"Error calling AI Judge: {e}")
        print(f"Response text: {response.text if 'response' in locals() else 'No response'}")
        return None

def display_round_result(round_num, user_input, user_move, bot_move, winner, reason):
    """Display the result of a round"""
    print("\n" + "="*60)
    print(f"ROUND {round_num} RESULT")
    print("="*60)
    print(f"Your input: '{user_input}'")
    print(f"Your move: {user_move.upper()}")
    print(f"Bot's move: {bot_move.upper()}")
    print(f"Winner: {winner.upper()}")
    print(f"Reason: {reason}")
    print("="*60)

def display_final_results(game_state):
    """Display final game results"""
    print("\n" + "="*60)
    print("FINAL GAME RESULTS")
    print("="*60)
    print(f"Total Rounds Played: {game_state.round_number}")
    print(f"Your Score: {game_state.user_score}")
    print(f"Bot Score: {game_state.bot_score}")
    print(f"Draws: {game_state.draws}")
    print()
    
    if game_state.user_score > game_state.bot_score:
        print("🎉 YOU WIN THE GAME! 🎉")
    elif game_state.bot_score > game_state.user_score:
        print("🤖 BOT WINS THE GAME! 🤖")
    else:
        print("🤝 IT'S A DRAW! 🤝")
    
    print("="*60)
    
    # Show round-by-round history
    print("\nROUND-BY-ROUND HISTORY:")
    for record in game_state.game_history:
        print(f"Round {record['round']}: {record['user_move']} vs {record['bot_move']} → {record['winner']}")

def play_game(num_rounds=5):
    """Main game loop"""
    print("="*60)
    print("WELCOME TO ROCK-PAPER-SCISSORS-PLUS!")
    print("="*60)
    print("\nRules:")
    print("- Valid moves: rock, paper, scissors, bomb")
    print("- Bomb beats everything but can only be used ONCE")
    print("- Type your move in natural language")
    print("- Type 'quit' to exit\n")
    
    game_state = GameState()
    
    for _ in range(num_rounds):
        print(f"\n--- Round {game_state.round_number + 1} of {num_rounds} ---")
        
        # Get user input
        user_input = input("Your move: ").strip()
        
        if user_input.lower() == 'quit':
            print("Game ended early.")
            break
        
        if not user_input:
            print("Empty input! Please enter a move.")
            continue
        
        # Generate bot move
        bot_move = generate_bot_move(game_state)
        
        # Call AI Judge
        judgment = call_ai_judge(user_input, bot_move, game_state)
        
        if judgment is None:
            print("Error getting judgment. Skipping round.")
            continue
        
        # Extract judgment details
        move_interpreted = judgment.get('move_interpreted', 'invalid')
        move_status = judgment.get('move_status', 'INVALID')
        reason = judgment.get('reason', 'No reason provided')
        round_winner = judgment.get('round_winner', 'none')

        # Update bomb usage if the user successfully used bomb
        if move_status == "VALID" and move_interpreted == "bomb":
           game_state.bomb_used_by_user = True
        
        
        # Add round to history
        game_state.add_round(
            user_move=move_interpreted,
            bot_move=bot_move,
            winner=round_winner,
            reason=reason
        )
        
        # Display round result
        display_round_result(
            round_num=game_state.round_number,
            user_input=user_input,
            user_move=move_interpreted,
            bot_move=bot_move,
            winner=round_winner,
            reason=reason
        )
    
    # Display final results
    display_final_results(game_state)

if __name__ == "__main__":
    play_game(num_rounds=5)