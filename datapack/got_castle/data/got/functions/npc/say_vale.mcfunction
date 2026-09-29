execute store result score #r got_g run random value 1..5
execute if score #r got_g matches 1 run tellraw @a[distance=..10] [{"text": "<Valeman> ", "color": "white"}, {"text": "As High as Honor. The Eyrie has never been taken by force.", "color": "white"}]
execute if score #r got_g matches 2 run tellraw @a[distance=..10] [{"text": "<Valeman> ", "color": "white"}, {"text": "It is a long climb to the Eyrie. Mind the edge!", "color": "white"}]
execute if score #r got_g matches 3 run tellraw @a[distance=..10] [{"text": "<Valeman> ", "color": "white"}, {"text": "The Mountains of the Moon are full of clansmen. Do not go alone.", "color": "white"}]
execute if score #r got_g matches 4 run tellraw @a[distance=..10] [{"text": "<Valeman> ", "color": "white"}, {"text": "The winds up here would blow a dragon off course.", "color": "white"}]
execute if score #r got_g matches 5 run tellraw @a[distance=..10] [{"text": "<Valeman> ", "color": "white"}, {"text": "If you can hold the Eyrie against the mountain clans, you can hold any castle.", "color": "white"}]
playsound minecraft:entity.villager.ambient master @a[distance=..10]
