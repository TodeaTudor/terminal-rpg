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
![Alt text](https://user-images.githubusercontent.com/57226483/111079616-5f961700-8503-11eb-8117-85f3a25b15d2.png)
![Alt text](https://user-images.githubusercontent.com/57226483/111079619-602ead80-8503-11eb-8f54-25a35a5c517d.png)
![Alt text](https://user-images.githubusercontent.com/57226483/111079634-7177ba00-8503-11eb-8a26-12575c9fa252.png)
![Alt text](https://user-images.githubusercontent.com/57226483/111079618-602ead80-8503-11eb-9772-d12ffccdca3d.png)
![Alt text](https://user-images.githubusercontent.com/57226483/111079614-5efd8080-8503-11eb-92eb-0e03bb352714.png)
