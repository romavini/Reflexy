# Reflexy
![version](https://img.shields.io/badge/relise-v1.0.0-darkred)
### *A pixel-art pygame project*

##  🚨&nbsp;🕷 &nbsp; Concept
A samurai battling a bunch of robotic spiders that shoot deadly lasers, anyway, just another day in the life of a samurai...

![Spider Arena](Reflexy.gif)

## 🤖&nbsp;🦾 &nbsp; **Genetic Algorithm** and **Artificial Neural Network**
This project is also a sandbox to work with handmade IA algorithms. The intent is to create a model to guide the actions of the spiders, making them act in the group in a smart way.

The next GIF show the *vision* of the player and the spiders. Both the characters have a multiple of 36 lines of sight around, 10° apart. Every 36 lines are destined to identify a certain object, returning `1` if seen, or `0` if not.

![Spider Arena AI](Reflexy-logic.gif)

The characters of spiders have 4 groups of 36 lines of sights, each one identify below, in order of priority:
 - <span style="color:red">Red lines: </span> Enemy (player) detected.
 - <span style="color:blue">Blue lines: </span> Laser detected.
 - <span style="color:green">Green lines: </span> Ally (spiders) detected.
 - <span style="color:black">Black lines: </span> Wall detected.

In case none of the items above is identified, the line is present in silver.
 - <span style="color:silver">Silver lines: </span> Nothing detected.

The character of the player doesn't have the group of lines of sight destined to allies.

Also, the two classes of characters have an extra "line" of sight in format of a square, as a mean to prevent lasers coming from a blindspot.

## 📦&nbsp;🕹 &nbsp; Dependencies
 - [![pygame](https://img.shields.io/badge/pygame-v0.1.0-darkgreen)](https://www.pygame.org/)

## 🛠&nbsp;🧰 &nbsp; Run and Test
### Enviroment
```
$ # Create and activate a virtual environment
$ pip install requirements.txt # Install the dependencies
```
### Running
```
$ python reflexy/main.py
```
### Testing
```
$ pip install -r requirements-dev.txt # Install the dependencies
$ pytest reflexy
```
