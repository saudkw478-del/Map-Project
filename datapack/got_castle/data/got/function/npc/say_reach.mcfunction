execute store result score #r got_g run random value 1..5
execute if score #r got_g matches 1 run tellraw @a[distance=..10] [{"text": "<Reach Farmer> ", "color": "green"}, {"text": "Growing Strong! The roses are in bloom, if you can call them that.", "color": "white"}]
execute if score #r got_g matches 2 run tellraw @a[distance=..10] [{"text": "<Reach Farmer> ", "color": "green"}, {"text": "Highgarden feeds half the realm. Do not trample the flowers.", "color": "white"}]
execute if score #r got_g matches 3 run tellraw @a[distance=..10] [{"text": "<Reach Farmer> ", "color": "green"}, {"text": "The Tyrells fight with flowers and gold. You should bring a sword too.", "color": "white"}]
execute if score #r got_g matches 4 run tellraw @a[distance=..10] [{"text": "<Reach Farmer> ", "color": "green"}, {"text": "If you are hungry, there is bread in the armory chests.", "color": "white"}]
execute if score #r got_g matches 5 run tellraw @a[distance=..10] [{"text": "<Reach Farmer> ", "color": "green"}, {"text": "Storm clouds gather in the east. Stay alert.", "color": "white"}]
playsound minecraft:entity.villager.ambient master @a[distance=..10]
