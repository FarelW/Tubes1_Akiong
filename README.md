<h1 align="center">Tugas Besar 1 IF2211 Strategi Algoritma</h1>
<h1 align="center">Kelompok 9 - Akiong</h3>
<h3 align="center">Greedy Algorithm Implementation in Etimo Diamond Game</p>

## Table of Contents

- [Overview](#overview)
- [Abstraction](#abstraction)
- [Built With](#built-with)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Links](#links)


## Overview
![Screenshot 2023-11-19 153812]()
Our Team members :
- 13522019 - Wilson Yusda
- 13522047 - Farel Winalda
- 10023500 - Mifathul Jannah

<p>Our Lecturer : Dr. Ir. Rinaldi Munir, M.T.</p>

Here is the purpose of making this project :
- To fulfill the requirements of the first big assignment for the course IF2211 Algorithm Strategy.
- To implement Greedy Algorithm in chasing the diamonds in Etimo Game.
- To Get the best algorithm to gain the most diamonds in Etimo Game.

## Abstraction

In the project of creating a bot for the game Etimo Diamonds, we are using a greedy algorithm to acquire as many diamonds as possible in the most efficient way. We apply a greedy approach by considering efficiency through emptying the inventory back to the base without wasting any remaining diamonds in the inventory and by considering the presence of clusters (groups of diamonds). We are also contemplating the use of teleportation to reach targets more quickly and employing a red button if there are no more clusters or only a few diamonds left.

## Built With

- [Python](https://www.python.org/)
- [Node](https://nodejs.org/en)
- [Etimo](https://diamonds.etimo.se/)
- [Docker](https://www.docker.com/)

## Prerequisites

To run this project, you will need to perform several installations, including:
- `Python3` : Python3 is programming language that used to implement the bot and handle all the logic in this game
- `Node.js` : Node.js is essential for running JavaScript on the server-side and for managing JavaScript-based build processes, including those used in React applications.
- `npm` (Node package manager) : npm is indeed the package manager for JavaScript and is used to install and manage JavaScript packages and libraries in this project.
- `docker` : docker is really important because this contains the database and all the package in one container

## Installation

If you want to run this program you will have 2 terminal opened for the GameEngine and Bot

1. Clone this repository :
```shell
git clone https://github.com/FarelW/Tubes1_Akiong
```

2. Open directory : 
```shell
cd Tubes1_Akiong/src
```

Game Engine
1. Clone this repository :
```shell
git clone https://github.com/haziqam/tubes1-IF2211-game-engine
```

2. Yarn download :
```shell
cd tubes1-IF2211-game-engine
npm install --global yarn
```

3. Install all the packages :
```shell
yarn
./scripts/copy-env.bat
```

4. Setup local database with docker (make sure to open docker desktop) :
``` shell
docker compose up -d database
./scripts/setup-db-prisma.bat
```

5. Build the application :
``` shell
npm run build
```

6. Start the application :
``` shell
npm run start
```

Bot
1. Install requirements :
```shell
cd Bot
pip install -r requirements.txt
```

2. Running The bot solo:
```shell
python main.py --logic Random --email=your_email@example.com --name=your_name --password=your_password --team etimo
```

3. Running The bot batch:
```shell
./run-bots.bat
```

If you want to edit or fix the bot code you can do
1. Open Logic Folder :
```shell
cd Bot/game/logic
```

2. Create your own logic or edit the available logic :
modify main.py
```
CONTROLLERS = {
    "YourLogic":YourLogic,
}
```

and create YourLogic.py
```
from game.logic.base import BaseLogic
class AkiongLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
    def next_move(self, board_bot: GameObject, board: Board):
        #start your logic here by determined the delta_x and delta_y
        return delta_x, delta_y
```

Here is the plain package to start this game :
- [Bot](https://github.com/haziqam/tubes1-IF2211-bot-starter-pack/releases/tag/v1.0.1)
- [Game Engine](https://github.com/haziqam/tubes1-IF2211-game-engine/releases/tag/v1.1.0)

Or you can read the full documentation of  [Etimo](https://docs.google.com/document/d/1L92Axb89yIkom0b24D350Z1QAr8rujvHof7-kXRAp7c/edit) here

## Links
- Repository : https://github.com/FarelW/Tubes1_Akiong
- Issue tracker :
   - If you encounter any issues with the program, come across any disruptive bugs, or have any suggestions for improvement, please don't hesitate to tell the author
- Github main contributor :
   - Contributor 1 (Wilson Yusda) - https://github.com/Razark-Y
   - Contributor 2 (Farel Winalda) - https://github.com/FarelW
   - Contributor 3 (Mifathul Jannah) - https://github.com/miftahstudy
