# Time Rift Rescue

## Game Overview

In **Time Rift Rescue**, players step into the shoes of a legendary adventurer who is called out of retirement to rescue three scientists trapped in mysterious ruins. These ruins are said to contain an ancient device capable of manipulating time. As players explore the island, they will face numerous challenges, puzzles, and enemies guarding each ruin.

## Gameplay Mechanics

- **Exploration and Rescue Missions:** Traverse through three unique ruins, each presenting its own set of challenges and puzzles. Each ruin is guarded by undead creatures and traps.
- **Puzzle Solving:** Solve environmental puzzles, ancient mechanisms, and clues left by the scientists to advance and rescue them.
- **Combat and Survival:** Engage in combat with zombies, monsters, and other supernatural entities. Use various weapons and tools found throughout the ruins.
- **Crafting and Item Management:** In one of the ruins, players must craft a potion needed to wake a knocked-out scientist. Gather ingredients, defeat a powerful monster for a crucial drop, and use a simple crafting mechanic.
- **Plot Twists and Narrative Choices:** Uncover secrets about the scientists, the ancient device, and the true nature of your mission. Experience unexpected twists in the storyline.
- **Time Travel Mechanic:** Activate the ancient time machine, which triggers a time loop, sending the protagonist back to the beginning with new knowledge and abilities. This creates a Groundhog Day-like scenario where each playthrough builds on the previous one.
- **Multiple Endings:** Make choices that lead to different endings, revealing the consequences of your actions and decisions.

## Key Features

- Rich, atmospheric environments with detailed ruins to explore.
- Engaging storyline with deep lore and character development.
- Challenging puzzles and strategic combat encounters.
- Dynamic time loop mechanic for added replayability and depth.
- A blend of traditional adventure gameplay with modern crafting and survival elements.

## Game-Lore

Three scientists, intrigued by recently discovered ruins rumored to house an ancient time-travel device, set out to explore them. They are accompanied by a famous adventurer. However, they become separated within the ruins and end up at different entrances. The protagonist, a retired legendary adventurer and old friend of the scientists, is called upon to rescue them.

## Gameplay Walkthrough

1. **Find and Enter the Ruins:**
   - Locate the map to decode the sequence required to unlock the ruins.
   - Ruins are numbered 1, 2, and 3.

2. **Ruin 1:**
   - Defeat zombies and find the key to rescue the first scientist.
   - Return to the helicopter with the rescued scientist.

3. **Ruin 2:**
   - Retrieve a recipe from the room to craft a potion for the second scientist.
   - Defeat a monster outside to obtain a necessary drop-item.
   - Craft the potion and rescue the second scientist.

4. **Ruin 3:**
   - Battle two zombie guards at the entrance.
   - Discover the third scientist's allegiance to the Sekai-Seifuku organization.
   - Defeat the transformed adventurer and knock out the third scientist.
   - Unlock a hidden treasure chest using a password derived from the number of zombies in each ruin.

5. **Escape and Time Loop:**
   - Escape from the island and achieve fame once again.
   - A monkey accidentally activates the time machine, initiating a time loop that resets the adventure.

## Controls

- **Player Movement:** [Up Arrow], [Down Arrow], [Left Arrow], [Right Arrow] or [W], [A], [S], [D].
- **Camera Movement:** [Mouse Movement], [I] (up), [J] (left), [K] (down), [L] (right). Hold [B] for Box-camera mode (disables keyboard and mouse camera controls). Press [U] to reset to player-centered camera.
- **Attack:** [Space]
- **Magic:** [Left Control]
- **Pause Screen:** [Esc]
- **Switch Weapons:** [N] (next weapon), [P] (previous weapon)
- **Switch Magic:** [M] (next magic), [O] (previous magic)
- **View Dialogs:** [G] to view the log of all dialogs. Click on a visible log to display the dialog box.
- **Inventory Box:** [V] to open the inventory. Use [T], [Y] to navigate the inventory box. Press [E] to use the selected inventory item.

## Image Naming Conventions

- **Obstacles:** `<name_of_obstacle>_<elem_id_in_Tiled_map>_<img_width>_<img_height>.png`
  - Example: `rock_1001_64_64.png`
- **Invisible Boundaries:** Use ID `1000` and `1001` for easy coding.
- **Portals:** Named `<x>` where 'x' represents the frame number (fixed size: 96x96).
- **Objects Larger than One Tile:** Use ID `500`.

## Description of Files

- **Settings.py:** Basic settings like screen dimensions, player sizes, colors, and movement speeds.
- **Helpers.py:** Helper functions for loading graphics, parsing sizes, etc.
- **Quests.py:** Contains quest items and related mechanics.

## Extras

- **Pathfinding:** Enemies use A* pathfinding to navigate towards the player, avoiding obstacles. Detection tiles are adjusted to ensure smooth movement.
- **Offsets:**
  - **Player Offset:** Maintains visual consistency with sprite positioning.
  - **Camera Offset:** Allows for keyboard and mouse-based camera movement with counters to manage screen boundaries.



## License

[MIT](https://choosealicense.com/licenses/mit/)

