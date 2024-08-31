# Flappy-Bird-NEAT
This project is a Python implementation of a Flappy Bird clone, where the AI is trained using NEAT (NeuroEvolution of Augmenting Topologies) to learn how to play the game. The AI evolves over generations, improving its gameplay through reinforcement learning. 
Flappy Bird NEAT AI
This project demonstrates the application of the NEAT (NeuroEvolution of Augmenting Topologies) algorithm to train an AI to play the Flappy Bird game. The AI learns how to navigate through the pipes and optimize its behavior to achieve higher scores.

Table of Contents
Installation
Usage
How It Works
Files
Dependencies
Contributing
License
Installation

Clone the repository:
git clone https://github.com/your-username/Flappy-Bird-Neat
cd flappy-bird-neat

Set up a Python virtual environment (optional but recommended):
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the required dependencies:
pip install -r requirements.txt

Ensure you have the necessary images in the imgs folder:
bird1.png, bird2.png, bird3.png
pipe.png
base.png
bg.png

Run the program:
bash
Copy code
python flappy_bird.py
Usage
Once the game starts, the AI will begin training itself to play the game. The training process uses NEAT to evolve the neural networks that control the birds.

Key Features:
You can quit the game at any time by closing the window.

How It Works
Bird Class: Represents the flappy bird, including movement, jumping, and collision logic.
Pipe Class: Handles the creation, movement, and collision detection of pipes.
Base Class: Manages the scrolling ground at the bottom of the screen.
NEAT Algorithm: The core of the AI, NEAT evolves neural networks to control the bird. The neural networks learn from their performance in the game and gradually improve over generations.

Files
flappy_bird.py: Main script to run the game and training.
config-feedforward.txt: Configuration file for the NEAT algorithm.
imgs/: Folder containing images for the game.

Dependencies
pygame: Used for rendering the game.
neat-python: Implementation of the NEAT algorithm.

Install dependencies via:
bash
Copy code
pip install -r requirements.txt
Contributing
Feel free to fork this repository, make improvements, and submit a pull request. Contributions are welcome!
