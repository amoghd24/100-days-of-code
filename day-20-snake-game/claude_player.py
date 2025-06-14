import os
import anthropic
from dotenv import load_dotenv
from typing import Optional, Dict, Any

# Load environment variables
load_dotenv()

class ClaudeSnakePlayer:
    def __init__(self):
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        # Use native Anthropic SDK
        self.client = anthropic.Anthropic(
            api_key=api_key
        )
        self.model = "claude-sonnet-4-20250514"  # Claude model name
        self.moves_queue = []  # Store planned moves
        
    def get_ai_move(self, game_state: Dict[str, Any]) -> Optional[str]:
        """Use native Anthropic SDK to get the next move for the snake"""
        # If we have planned moves, use the next one
        if self.moves_queue:
            return self.moves_queue.pop(0)
            
        try:
            # Create the system prompt and user message
            system_prompt = "You are an expert Snake game AI player. Analyze the game state carefully and plan a sequence of 10 optimal moves to survive and collect food. Always respond with exactly 10 words separated by spaces: UP, DOWN, LEFT, or RIGHT."
            user_prompt = self.create_game_prompt(game_state)
            
            message = self.client.messages.create(
                model=self.model,
                max_tokens=50,  # Increased for 10 moves
                temperature=0.1,
                system=system_prompt,
                messages=[
                    {
                        "role": "user", 
                        "content": user_prompt
                    }
                ]
            )
            
            # Parse Claude's response
            moves = message.content[0].text.strip().upper().split()
            
            # Validate the moves
            valid_moves = ["UP", "DOWN", "LEFT", "RIGHT"]
            valid_sequence = [move for move in moves if move in valid_moves]
            
            if valid_sequence:
                # Store all moves except the first one
                self.moves_queue = valid_sequence[1:]
                return valid_sequence[0]
            else:
                print(f"Invalid Claude moves: {moves}")
                return None
                
        except Exception as e:
            print(f"Claude API Error: {e}")
            return None
    
    def create_game_prompt(self, game_state: Dict[str, Any]) -> str:
        """Create a strategic prompt optimized for Claude's reasoning capabilities"""
        snake_head = game_state['snake_head']
        food_pos = game_state['food_position']
        snake_body = game_state['snake_body']
        current_dir = self.heading_to_direction(game_state['current_direction'])
        
        # Calculate distance to food
        dx = food_pos['x'] - snake_head['x']
        dy = food_pos['y'] - snake_head['y']
        distance_to_food = abs(dx) + abs(dy)  # Manhattan distance
        
        return f"""SNAKE GAME ANALYSIS - PLAN 10 MOVES:

CURRENT STATE:
• Snake head: ({snake_head['x']}, {snake_head['y']})
• Moving direction: {current_dir}
• Food target: ({food_pos['x']}, {food_pos['y']})
• Distance to food: {distance_to_food} units
• Snake length: {len(snake_body) + 1} segments
• Boundaries: x,y must stay within ±295

SNAKE BODY SEGMENTS:
{self.format_snake_body(snake_body)}

STRATEGIC CONSIDERATIONS:
1. SURVIVAL: Avoid walls (±295 boundary) and body collision
2. FOOD PURSUIT: Plan complete path to food (10 moves)
3. SPACE MANAGEMENT: Don't create dead-end situations
4. MOVEMENT RULES: Cannot reverse direction (e.g., if going RIGHT, cannot go LEFT)

DISTANCE TO FOOD:
• Horizontal: {food_pos['x'] - snake_head['x']} pixels {'(go RIGHT)' if food_pos['x'] > snake_head['x'] else '(go LEFT)' if food_pos['x'] < snake_head['x'] else '(aligned)'}
• Vertical: {food_pos['y'] - snake_head['y']} pixels {'(go UP)' if food_pos['y'] > snake_head['y'] else '(go DOWN)' if food_pos['y'] < snake_head['y'] else '(aligned)'}

IMMEDIATE DANGER CHECK:
{self.analyze_dangers(snake_head, snake_body, current_dir)}

PLANNING INSTRUCTIONS:
1. Plan a complete sequence of 10 moves
2. Consider both horizontal and vertical movement
3. Choose the path that:
   • Minimizes moves to reach food
   • Leaves space for future moves
   • Avoids getting trapped
4. Think about the entire sequence, not just individual moves

Respond with exactly 10 words separated by spaces: UP DOWN LEFT RIGHT (in the order you want to move)"""

    def analyze_dangers(self, snake_head: Dict, snake_body: list, current_dir: str) -> str:
        """Analyze immediate dangers in each direction"""
        head_x, head_y = snake_head['x'], snake_head['y']
        dangers = []
        
        # Check wall dangers
        if head_x >= 275: dangers.append("RIGHT leads to wall")
        if head_x <= -275: dangers.append("LEFT leads to wall")  
        if head_y >= 275: dangers.append("UP leads to wall")
        if head_y <= -275: dangers.append("DOWN leads to wall")
        
        # Check body collision dangers
        for segment in snake_body:
            seg_x, seg_y = segment['x'], segment['y']
            if abs(seg_x - (head_x + 20)) < 15 and abs(seg_y - head_y) < 15:
                dangers.append("RIGHT leads to body collision")
            if abs(seg_x - (head_x - 20)) < 15 and abs(seg_y - head_y) < 15:
                dangers.append("LEFT leads to body collision")
            if abs(seg_x - head_x) < 15 and abs(seg_y - (head_y + 20)) < 15:
                dangers.append("UP leads to body collision")
            if abs(seg_x - head_x) < 15 and abs(seg_y - (head_y - 20)) < 15:
                dangers.append("DOWN leads to body collision")
        
        return "\n".join(dangers) if dangers else "No immediate dangers detected"

    def heading_to_direction(self, heading: float) -> str:
        """Convert turtle heading degrees to readable direction"""
        heading = int(heading % 360)
        directions = {0: "RIGHT", 90: "UP", 180: "LEFT", 270: "DOWN"}
        return directions.get(heading, f"ANGLE_{heading}")
    
    def format_snake_body(self, snake_body: list) -> str:
        """Format snake body positions for Claude's analysis"""
        if not snake_body:
            return "• No body segments (snake just started)"
        
        # Show relevant segments for collision analysis
        segments_to_show = snake_body[:6]  # Show first 6 segments
        formatted = []
        
        for i, seg in enumerate(segments_to_show):
            formatted.append(f"• Segment {i+1}: ({int(seg['x'])}, {int(seg['y'])})")
        
        if len(snake_body) > 6:
            formatted.append(f"• ... plus {len(snake_body) - 6} more segments")
            
        return "\n".join(formatted)
    
    def get_safe_fallback_move(self, snake_head, current_direction, wall_distance=295) -> str:
        """Provide a safe fallback move if Claude fails"""
        head_x, head_y = snake_head['x'], snake_head['y']
        
        # Advanced collision avoidance logic
        safe_moves = []
        
        # Check each direction for safety with larger margin
        if head_y < wall_distance - 30:  # Can go UP
            safe_moves.append("UP")
        if head_y > -wall_distance + 30:  # Can go DOWN
            safe_moves.append("DOWN")
        if head_x > -wall_distance + 30:  # Can go LEFT
            safe_moves.append("LEFT")
        if head_x < wall_distance - 30:  # Can go RIGHT
            safe_moves.append("RIGHT")
        
        # Return the safest move
        if safe_moves:
            return safe_moves[0]
        else:
            # Emergency: try to continue current direction
            return self.heading_to_direction(current_direction) 