from turtle import Screen
import time
from snake import Snake
from food import Food
from score import Scoreboard
from ai_player import AISnakePlayer

WALL_DISTANCE = 295

# Game setup
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("🤖 AI Snake Game - Powered by OpenAI")
screen.tracer(0)

# Initialize game objects
snake = Snake()
food = Food()
scoreboard = Scoreboard()

# Initialize AI player
print("🚀 Initializing AI Snake Player...")
try:
    ai_player = AISnakePlayer()
    print("✅ AI Player ready!")
except Exception as e:
    print(f"❌ Failed to initialize AI Player: {e}")
    print("Make sure your .env file contains OPENAI_API_KEY")
    exit(1)

# Game state tracking
game_is_on = True
move_counter = 0
decisions_made = 0
successful_decisions = 0

print("\n🐍 AI Snake Game Starting...")
print("Watch the AI play Snake using OpenAI Responses API!")
print("Close the window or press any key to exit.\n")

# Add click to exit functionality
screen.listen()
screen.onkey(lambda: exit(), "space")

while game_is_on:
    screen.update()
    time.sleep(0.1)  # Slightly slower for AI processing and visualization
    
    # Get AI decision every 3 frames to optimize API usage and game performance
    if move_counter % 2 == 0:  # Make decision every 2 frames
        # Prepare game state for AI
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
        
        # Get AI decision
        decisions_made += 1
        print(f"🧠 AI thinking... (Decision #{decisions_made})")
        
        ai_decision = ai_player.get_ai_move(game_state)
        
        if ai_decision:
            successful_decisions += 1
            print(f"✅ AI decides: {ai_decision}")
            
            # Apply AI decision to snake movement
            if ai_decision == "UP":
                snake.up()
            elif ai_decision == "DOWN":
                snake.down()
            elif ai_decision == "LEFT":
                snake.left()
            elif ai_decision == "RIGHT":
                snake.right()
        else:
            print("⚠️  AI decision failed, using safety fallback")
            # Use fallback safety move
            fallback_move = ai_player.get_safe_fallback_move(
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
        print(f"🤖 AI Success Rate: {successful_decisions}/{decisions_made} ({(successful_decisions/decisions_made*100):.1f}%)")
    
    # Check self collision
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            game_is_on = False
            scoreboard.game_over()
            print(f"\n🐍 Game Over - Snake bit itself!")
            print(f"📊 Final Score: {scoreboard.score}")
            print(f"🤖 AI Success Rate: {successful_decisions}/{decisions_made} ({(successful_decisions/decisions_made*100):.1f}%)")

print("\n🎮 Game finished! Click anywhere to close.")
screen.exitonclick() 