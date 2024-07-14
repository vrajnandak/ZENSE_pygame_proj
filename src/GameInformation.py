import pygame

#This file contains the game information such as the dialogs, quests etc.

#Each dialog has a condition and only if the condition has been fullfilled, the dialog will be played.

Scientist1={
    'dialog':{ 'before_clearing_all_enemies': [['Please Find the key to this cell.'],
                                                ['I Think the key should be somewhere here. Can you check around'],
                                                ['Hmmm, Maybe the cage will unlock if you destroy all the enemies in this room.'],
                                                ['Can you please help me.']
                                              ],
                'after_clearing_all_enemies': [['Thank you so much for saving me.'],
                                               ['Can you also save the other 2.'],
                                               ['I think each of us got taken into different ruins'],
                                               ['I wish you best of luck']]
            }
}