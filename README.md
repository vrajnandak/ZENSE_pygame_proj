Time Rift Rescue

game-lore: In a world with advanced technology, evil organizations, adventurers and more, 3 scientists are curious about the recently discovered ruins which are rumored to hold an ancient device, capable of travelling through space and time. Intrigued by these rumors, the scientists decide to explore the ruins before anyone else and try to unlock the secrets to time-travelling. They bring with them a famous adventurer, who has survived all by himself in many islands and discovered hidden treasures. To their surprise however, they lose each other while exploring the island and each gets sent to a different ruin entrance. The protagonist, an old friend of theirs and the number one adventurer in the world(who's now retired), gets a call from one of these scientist's colleagues asking him to rescue to them. The protagonist, with no hesitation, sets out to the island in hopes of rescuing them.

Gameplay: The ruins are numbered 1,2,3 and the protagonist has to figure out the correct way of rescuing them by discovering the code on the map(The code is pretty visible when u look at the map after zooming out, it is on the seashore where the rocks are placed as the code). Once the protagonist enters this code, the first ruin in that order gets unlocked. Here he has to kill all the zombies and find the key to rescue his friend from where he is locked.
After rescuing this friend, he gets told to go back to the helicopter and this scientist number 1 goes back.
Now, in the second ruin lies another scientist who is knocked out and needs a medicine to wake up. Luckily, there is a recipe in that room but the adventure has to find the secret area in the same room and press 'E' to get the recipe.(Player can just spam 'E' whlie roaming around the room). After getting the recipe, a monster spawns in the island outside and the protagonist has to defeat that monster to get a drop-item from that monster. Then, the protagonist crafts the potion(with a minecraft like 'crafting' thing) and thus rescues the second scientist as well.
Now, in the third ruin, he finds 2 zombies standing as guard near the ruin entrance. He ponders why they're standing as guards and goes inside after defeating them. After going inside, he finds the 3rd scientist near a table and hears cackling laughter and calls him out. The protagonist would've never guessed that the third scientist had been secretly been working for the 'sekai-seifuku' organization (the world's most evil-organization) and was sent to this island inorder to kill the protagonist here. The protagonist has to then kill the adventurer, that tagged along with the 3 scientists and who had now turned into a zombie, inorder to save himself. After killing the adventurer and knocking the 3rd scientist unconsious, the protagonist falls into a cave and finds the hidden treasure. He has to unlock the chest however, inorder to take this hidden treasure(surprise, surprise, the password is the number whose digits are the number of zombies in every ruin).
Now, the protagonist escapes from this island, never caring to find the time machine, and becomes famous yet again.
(A monkey that slipped in when the door was opened by the protagonist, finds the time machine and presses the "red button". This activates the time machine and we go back to the start of the game).

SOFTWARES USED:
1. GIMP (2.10.30) to make sprites.
2. Tiled to make map layouts, manage different levels with csv files.
3. VS code for writing the pygame code.
4. pygame  (pip install pygame).
5. pathfinding (pip install pygame) for finding the shortest paths.


TO RUN THE GAME:
1. Open the 'ZENSE_PROJECT_PYGAME' folder in VScode and not any other folder. This is because 'os.getcwd()' is used in 'Settings.py' file and all the paths will fail if this folder is not the working directory.


CONTROLS: 
1. Player movement: [up-arrow, down-arrow, left-arrow, right-arrow] and [w,a,s,d].
2. Camera movement: [hovering mouse towards end of screen] and [i(top),j(left),k(down),l(right)]. Holding [b] will use the Box-camera instead of the default camera movement(player-centered camera). [u] to reset the camera back to the player. The box-camera cannot be used alongside the keyboard and mouse camera (There is a bit of a problem with the player's movement when using the box-camera as well).
3. Attack: [space]
4. Healing: [left control]
5. Pause Screen: [esc]


Naming formats:
1. The names of the different images of obstacles(rocks, trees, etc) will be '<name_of_obstacle>_<elem_id_in_Tiled_map>_<img_width>_<img_height>.png' where 'elem_id_in_Tiled_map' is the id of the element in the csv file obtained from Tiled software, the rest of the fields are as implied.
    ==>The 'invisible boundary' blocks that restrict the player's movement in the map must have the same id(will have id='1000'). This is to make the code easy to write. When you get the csv file from Tiled, it is best to manually change every occurance of the invisible tile to '1000' and '1001', etc as needed. This will make it easy to load graphics since different images in tiled can have same id's
    ==>The Portal images have a naming convention of <x> where 'x' represents the frame number in the portal's animation. The size of portals is fixed to 96x96.
    ==>The csv file should also have id '500' whenever an object is placed(in the Tiled map) having size more than one tile. This is to set the values of the detection tiles properly in the level instance.
2. The additional hidden rooms or extra rooms will be named in the following format: 'Ruin<x>_<extra_type><num>'. The 'extra_type' can be from ['hidden', 'extension'] only where 'hidden' represents the map to be discovered (can be opened only after protagonist unlocks the room, like the treasure room), 'extension' represents the doorway to other rooms which are basically open and don't need a special lock(They are loaded when the level itself is loaded).
    ex: 'Ruin2_hidden2', 'Ruin2_extension2'


RUINS:
1. Ruin0 - Is the main island.
2. Ruin1 - Is the 1st ruin that the protagonist has to conquer.
3. Ruin2 - Is the 2nd ruin that the protagonist has to conquer.
4. Ruin3 - Is the 3rd ruin that the protagonist has to conquer.


DESCRIPTION OF FILES:
->Hierarchy of folders:
1. Settings.py: Contains the basic settings like dimensions(screen sizes, player sizes, basic units, basic colors, movement speeds etc)
2. Helpers.py: Contains the helper functions like loading graphics, parsing sizes etc.
3. Quests.py: Contains the Quest items for the game.


EXTRAS:
->PATH TO PLAYER: Whenever the player is in the range of the enemy's attack radius, the enemy sprite uses a path finder(using the AStarFinder finder) to find the shortest path to the player. Inorder to be able to freely move the enemy even when close to the obstacles, the detection_tiles of the level instance(used for making the grid for finding the path) are filled with 0's where the obstacles are and even their boundaries are filled with 0. This is done so that the path found by the pathfinder will ensure that the enemy sprite moves a bit away from the obstacle sprites. However, as the speeds of the enemies don't match in line with the BASE_SIZE and the enemy is allowed to move diagonally, there is a possibility that an enemy sprite may sometime bug out when trying to move as the sprite may not exactly fit in with the cells of the detection_tiles.
->OFFSETS: The same offset value is used for all sprites, player etc.
    ->The way the get_player_based_offset() works: The below diagram is the level. For the player, the offsets are abvious. The below values are for the images. Both the offsets are obviously the same.
         ___________________________________
        |__|_____________________________|__|           ==>Offset_y will be '0' in this row. This height is the 'SCREEN_HEIGHT//2'
        |  |                             |  | 
        |  |                             |  | 
        |  |                             |  | 
        |  |                             |  |
        |  |                             |  | 
        |  |                             |  | 
        |  |                             |  | 
        |__|_____________________________|__|
        |__|_____________________________|__|           ==>Offset_y should be capped at 'LEVEL_HEIGHT'-'SCREEN_HEIGHT//2'

         ||                               ||  
         \/                               \/  
        This col will have              This col will have
        offset_x '0'                    offset_x as 'LEVEL_WIDTH-SCREEN_WIDTH//2'
    ->The way the get_keyboard_based_offset() works: The idea is to maintain a counter, one for [j,l](keyboard keys for left, right camera movement) and another for [i,k](keyboard keys for up, down camera movement). This offset will be maintained so that the use can move the player itself and also the camera at the same time. The offset caused by keyboard keys are added to the final offset being used for blitting the sprites. If you remove the extra conditions(based on the offset.x, offset.y values in the if statements), then suppose you go to the right most side of the screen and then try to go more right using keyboard controls. Then you would notice that on trying to go left, it would take a bit of time and this is because the counter accumulates instead of not counting at that point of time. Hence, the extra conditions based on those offset vals are important.
    ->The way the get_mouse_based_offset() works: The idea is to again maintain a counter, one for x-axis movement, and another for y-axis movement. When the mouse hits the set mouse limit positions of the screen, these counters will be incremented/decremented as needed and this offset value will be added to the final offset used for blitting the sprites. This is an additional functionality that the user may use if he doesn't want to use the keyboard keys.


IMAGE REFERENCES:
https://elthen.itch.io/2d-pixel-art-archaeologist

YOUTUBE REFERENCES:
https://www.youtube.com/watch?v=QU1pPzEGrqw
https://www.youtube.com/watch?v=Rvcyf4HsWiw
https://www.youtube.com/watch?v=fo4e3njyGy0






CHATGPT DESCRIPTION BASED ON ABOVE DESCRIPTION:
{
Title: Time Rift Rescue

Game Overview:
In Time Rift Rescue, players take on the role of the protagonist, a legendary adventurer who comes out of retirement to rescue three scientists trapped in mysterious ruins. These ruins hold the key to an ancient device rumored to control time itself. As the protagonist explores the island, they encounter various challenges, puzzles, and enemies guarding each ruin.

Gameplay Mechanics:

Exploration and Rescue Missions: Players must navigate through three distinct ruins, each with its own set of challenges and puzzles. Each ruin is guarded by undead creatures and traps.

Puzzle Solving: To progress through each ruin and rescue the scientists, players must solve puzzles related to the environment, ancient mechanisms, and clues left behind by the scientists.

Combat and Survival: Combat involves battling zombies, monsters, and other supernatural entities. Players use various weapons and tools they find throughout the ruins to fend off enemies.

Crafting and Item Management: In one of the ruins, players encounter a scientist who needs a special potion to wake up. They must gather ingredients, defeat a powerful monster for a necessary drop, and then craft the potion using a simple crafting mechanic.

Plot Twists and Narrative Choices: The game features a compelling storyline with unexpected twists. Players uncover secrets about the scientists, the ancient device, and the true nature of their mission as they progress.

Time Travel Mechanic: At a crucial point in the story, the protagonist inadvertently activates the ancient time machine hidden within the ruins. This triggers a time loop, sending the protagonist back to the beginning of their adventure with newfound knowledge and abilities, creating a Groundhog Day-like scenario where each playthrough builds upon the previous.

Multiple Endings: Depending on the player's choices throughout the game and their interactions with the scientists, different endings are unlocked, revealing the consequences of their actions and decisions.

Key Features:

Rich, atmospheric environments with detailed ruins to explore.
Engaging storyline with deep lore and character development.
Challenging puzzles and strategic combat encounters.
Dynamic time loop mechanic that adds replayability and depth to the narrative.
Mix of traditional adventure gameplay with modern crafting and survival elements.
Conclusion:
Time Rift Rescue offers players a thrilling adventure through ancient ruins filled with mystery, danger, and the potential to alter time itself. With its blend of exploration, puzzle-solving, combat, and narrative depth, the game promises an immersive experience where every decision matters in uncovering the secrets of the island and saving the scientists.
}