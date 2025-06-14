import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional, Dict, Any

# Load environment variables
load_dotenv()

class AISnakePlayer:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "o4-mini"
        self.moves_queue = []  # Store planned moves
        
    def get_ai_move(self, game_state: Dict[str, Any]) -> Optional[str]:
        """Use OpenAI Responses API to get the next move for the snake"""
        # If we have planned moves, use the next one
        if self.moves_queue:
            return self.moves_queue.pop(0)
            
        try:
            response = self.client.responses.create(
                model=self.model,
                input=self.create_game_prompt(game_state)
            )
            
            # Parse the AI's response
            moves = response.output_text.strip().upper().split()
            
            # Validate the moves
            valid_moves = ["UP", "DOWN", "LEFT", "RIGHT"]
            valid_sequence = [move for move in moves if move in valid_moves]
            
            if valid_sequence:
                # Store all moves except the first one
                self.moves_queue = valid_sequence[1:]
                return valid_sequence[0]
            else:
                print(f"Invalid AI moves: {moves}")
                return None
                
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            return None
    
    def create_game_prompt(self, game_state: Dict[str, Any]) -> str:
        """Create a detailed prompt for the AI to make the best move"""
        snake_head = game_state['snake_head']
        food_pos = game_state['food_position']
        snake_body = game_state['snake_body']
        current_dir = self.heading_to_direction(game_state['current_direction'])
        
        # Calculate distance to food
        dx = food_pos['x'] - snake_head['x']
        dy = food_pos['y'] - snake_head['y']
        distance_to_food = abs(dx) + abs(dy)  # Manhattan distance
        
        return f"""You are playing Snake game. Plan a sequence of 10 moves to reach the food and avoid obstacles.

CURRENT GAME STATE:
- Snake head position: x={snake_head['x']}, y={snake_head['y']}
- Currently moving: {current_dir}
- Food location: x={food_pos['x']}, y={food_pos['y']}
- Distance to food: {distance_to_food} units
- Snake body has {len(snake_body)} segments
- Screen boundaries: ±295 pixels from center

SNAKE BODY POSITIONS:
{self.format_snake_body(snake_body)}

GAME RULES:
1. Avoid hitting walls (stay within x: -295 to +295, y: -295 to +295)
2. Don't collide with your own body segments
3. Plan a sequence that leads to the food
4. Consider the entire path, not just the next move

STRATEGY TIPS:
- Plan a complete path to the food
- Consider both horizontal and vertical movement
- Avoid creating situations where you trap yourself
- If multiple paths exist, choose the one that:
  * Minimizes the number of moves to reach food
  * Leaves more space for future moves
  * Avoids getting trapped by the snake's body
- Think about the entire sequence, not just individual moves

Respond with exactly 10 words separated by spaces: UP DOWN LEFT RIGHT (in the order you want to move)"""

    def heading_to_direction(self, heading: float) -> str:
        """Convert turtle heading degrees to readable direction"""
        heading = int(heading % 360)
        directions = {0: "RIGHT", 90: "UP", 180: "LEFT", 270: "DOWN"}
        return directions.get(heading, f"ANGLE_{heading}")
    
    def format_snake_body(self, snake_body: list) -> str:
        """Format snake body positions for better AI understanding"""
        if not snake_body:
            return "Snake has no body segments yet (just started)"
        
        # Show first few segments to avoid overwhelming the AI
        segments_to_show = snake_body[:8]  # Show max 8 segments
        formatted = []
        
        for i, seg in enumerate(segments_to_show):
            formatted.append(f"Segment {i+1}: ({seg['x']}, {seg['y']})")
        
        if len(snake_body) > 8:
            formatted.append(f"... and {len(snake_body) - 8} more segments")
            
        return "\n".join(formatted)
    
    def get_safe_fallback_move(self, snake_head, current_direction, wall_distance=295) -> str:
        """Provide a safe fallback move if AI fails"""
        head_x, head_y = snake_head['x'], snake_head['y']
        
        # Simple collision avoidance logic
        safe_moves = []
        
        # Check each direction for immediate wall collision
        if head_y < wall_distance - 20:  # Can go UP
            safe_moves.append("UP")
        if head_y > -wall_distance + 20:  # Can go DOWN
            safe_moves.append("DOWN")
        if head_x > -wall_distance + 20:  # Can go LEFT
            safe_moves.append("LEFT")
        if head_x < wall_distance - 20:  # Can go RIGHT
            safe_moves.append("RIGHT")
        
        # Return a safe move or continue current direction
        if safe_moves:
            return safe_moves[0]
        else:
            return self.heading_to_direction(current_direction) 