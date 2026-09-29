execute store result score #r got_g run random value 1..5
execute if score #r got_g matches 1 run tellraw @a[distance=..10] [{"text": "<Riverlander> ", "color": "blue"}, {"text": "Family, Duty, Honor. The Tullys never break a promise... but others do.", "color": "white"}]
execute if score #r got_g matches 2 run tellraw @a[distance=..10] [{"text": "<Riverlander> ", "color": "blue"}, {"text": "The Trident runs cold and fast. Cross by the bridges, not the water.", "color": "white"}]
execute if score #r got_g matches 3 run tellraw @a[distance=..10] [{"text": "<Riverlander> ", "color": "blue"}, {"text": "Riverrun's hall has good steel in the armory. Take a shield before you go out.", "color": "white"}]
execute if score #r got_g matches 4 run tellraw @a[distance=..10] [{"text": "<Riverlander> ", "color": "blue"}, {"text": "I heard something about a wedding. I would not go, if I were you.", "color": "white"}]
execute if score #r got_g matches 5 run tellraw @a[distance=..10] [{"text": "<Riverlander> ", "color": "blue"}, {"text": "The Kingsroad is long. Type /trigger got_kit set 2 for wings and a horse egg.", "color": "white"}]
playsound minecraft:entity.villager.ambient master @a[distance=..10]
