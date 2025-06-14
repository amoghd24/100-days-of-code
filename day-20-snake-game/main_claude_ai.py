from turtle import Screen
import time
from snake import Snake
from food import Food
from score import Scoreboard
from claude_player import ClaudeSnakePlayer

WALL_DISTANCE = 295

# Game setup
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("🤖 Claude AI Snake Game - Powered by Anthropic")
screen.tracer(0)

# Initialize game objects
snake = Snake()
food = Food()
scoreboard = Scoreboard()

# Initialize Claude AI player
print("🚀 Initializing Claude AI Snake Player...")
try:
    claude_player = ClaudeSnakePlayer()
    print("✅ Claude AI Player ready!")
except Exception as e:
    print(f"❌ Failed to initialize Claude AI Player: {e}")
    print("Make sure your .env file contains ANTHROPIC_API_KEY")
    exit(1)

# Game state tracking
game_is_on = True
move_counter = 0
decisions_made = 0
successful_decisions = 0

print("\n🐍 Claude AI Snake Game Starting...")
print("Watch Claude play Snake using Anthropic's native API!")
print("Close the window or press space to exit.\n")

# Add click to exit functionality
screen.listen()
screen.onkey(lambda: exit(), "space")

while game_is_on:
    screen.update()
    time.sleep(0.25)  # Slightly slower for Claude's processing and visualization
    
    # Get Claude decision every 2 frames to optimize API usage
    if move_counter % 2 == 0:  # Make decision every 2 frames
        # Prepare game state for Claude
        game_state = {
            "snake_head": {
                "x": round(snake.head.xcor()), 
                "y": round(snake.head.ycor())
            },
            "snake_body": [
                {"x": round(seg.xcor()), "y": round(seg.ycor())} 
                for seg in snake.segments[1:]
            ],
            "food_position": {
                "x": round(food.xcor()), 
                "y": round(food.ycor())
            },
            "current_direction": snake.head.heading(),
            "screen_bounds": WALL_DISTANCE
        }
        
        # Get Claude's decision
        decisions_made += 1
        print(f"🧠 Claude thinking... (Decision #{decisions_made})")
        
        claude_decision = claude_player.get_ai_move(game_state)
        
        if claude_decision:
            successful_decisions += 1
            print(f"✅ Claude decides: {claude_decision}")
            
            # Apply Claude's decision to snake movement
            if claude_decision == "UP":
                snake.up()
            elif claude_decision == "DOWN":
                snake.down()
            elif claude_decision == "LEFT":
                snake.left()
            elif claude_decision == "RIGHT":
                snake.right()
        else:
            print("⚠️  Claude decision failed, using safety fallback")
            # Use fallback safety move
            fallback_move = claude_player.get_safe_fallback_move(
                game_state["snake_head"], 
                game_state["current_direction"]
            )
            print(f"🛡️  Fallback move: {fallback_move}")
            
            if fallback_move == "UP":
                snake.up()
            elif fallback_move == "DOWN":
                snake.down()
            elif fallback_move == "LEFT":
                snake.left()
            elif fallback_move == "RIGHT":
                snake.right()
    
    # Move snake
    snake.move()
    move_counter += 1
    
    # Check food collision
    if snake.head.distance(food) < 15:
        food.refresh()
        scoreboard.update_score()
        snake.extend()
        print(f"🍎 Food eaten! Score: {scoreboard.score}")
    
    # Check wall collision
    if (snake.head.xcor() > WALL_DISTANCE or snake.head.xcor() < -WALL_DISTANCE or 
        snake.head.ycor() > WALL_DISTANCE or snake.head.ycor() < -WALL_DISTANCE):
        game_is_on = False
        scoreboard.game_over()
        print(f"\n💥 Game Over - Hit Wall!")
        print(f"📊 Final Score: {scoreboard.score}")
        print(f"🤖 Claude Success Rate: {successful_decisions}/{decisions_made} ({(successful_decisions/decisions_made*100):.1f}%)")
    
    # Check self collision
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            game_is_on = False
            scoreboard.game_over()
            print(f"\n🐍 Game Over - Snake bit itself!")
            print(f"📊 Final Score: {scoreboard.score}")
            print(f"🤖 Claude Success Rate: {successful_decisions}/{decisions_made} ({(successful_decisions/decisions_made*100):.1f}%)")

print("\n🎮 Game finished! Click anywhere to close.")
screen.exitonclick() 