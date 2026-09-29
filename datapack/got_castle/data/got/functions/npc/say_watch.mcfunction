execute store result score #r got_g run random value 1..5
execute if score #r got_g matches 1 run tellraw @a[distance=..10] [{"text": "<Night's Watchman> ", "color": "dark_gray"}, {"text": "Night gathers, and now my watch begins. Stay clear of the Wall's edge, friend.", "color": "white"}]
execute if score #r got_g matches 2 run tellraw @a[distance=..10] [{"text": "<Night's Watchman> ", "color": "dark_gray"}, {"text": "The Wall is 78 blocks high. Climb the ladders by the tunnel - the view is worth it.", "color": "white"}]
execute if score #r got_g matches 3 run tellraw @a[distance=..10] [{"text": "<Night's Watchman> ", "color": "dark_gray"}, {"text": "The wildlings come at dusk. Stand inside the castle and type /trigger got_battle to call the fight.", "color": "white"}]
execute if score #r got_g matches 4 run tellraw @a[distance=..10] [{"text": "<Night's Watchman> ", "color": "dark_gray"}, {"text": "Beyond the Wall the dead walk. Bring a bow, a torch, and someone who can fight.", "color": "white"}]
execute if score #r got_g matches 5 run tellraw @a[distance=..10] [{"text": "<Night's Watchman> ", "color": "dark_gray"}, {"text": "The armory chests hold better steel than we have. Open them before the battle!", "color": "white"}]
playsound minecraft:entity.villager.ambient master @a[distance=..10]
