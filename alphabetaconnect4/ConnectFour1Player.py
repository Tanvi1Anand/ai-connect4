import ConnectFourRandomAI
import ConnectFourMinimaxAI

import ConnectFourEngine

if __name__ == '__main__':
    # Initialise the game engine
    # Modify these parameters to tweak the game
    app = ConnectFourEngine.ConnectFour(
            ai_delay = 0,
            red_player = None,
            blue_player = ConnectFourMinimaxAI.AIcheck,
            rewards = [ 0, 10, 50, 10000, 10000, 10000, 10000, 10000 ],
            winscore = 10000
            )
    # start the game engine
    app.game_loop()
