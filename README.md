# terminal-rpg
The demo of an RPG made from scratch using the MacOS terminal enhanced with the ncurses library. Uses ASCII art for the character models.

## Installation

The game uses the the curses library that can be install using [brew](https://brew.sh/index_ro).

```bash
brew install ncurses
```

The Python version used for this project is 3.7

For the installation of the required packages [conda](https://www.anaconda.com/products/individual) or [pip](https://pypi.org/project/pip/) can be used.

For instance, create a conda environment for the game:

```bash
conda create -n terminal-rpg python=3.7
```
After that, activate the environment using the following command:

```bash
conda activate terminal-rpg
```
While inside the environment, you need to install playsound and pyobjc using the following:

```bash
pip3 install playsound
pip3 install -U pyobjc
```
After the completion of the installation, you can play the game by typing ```bash python3 test.py``` inside the source folder.

To exit the game you can use the Flee command from the main game menu.

After closing the game, you can deactivate the environment by simply typing: ```bash conda deactivate terminal-rpg```

## Screenshots
