execute store result score #r got_g run random value 1..5
execute if score #r got_g matches 1 run tellraw @a[distance=..10] [{"text": "<Smallfolk of King's Landing> ", "color": "red"}, {"text": "The Iron Throne is made of a thousand swords. Do not sit on it - it bites.", "color": "white"}]
execute if score #r got_g matches 2 run tellraw @a[distance=..10] [{"text": "<Smallfolk of King's Landing> ", "color": "red"}, {"text": "I hear green fire will burn on the water when the Blackwater battle comes.", "color": "white"}]
execute if score #r got_g matches 3 run tellraw @a[distance=..10] [{"text": "<Smallfolk of King's Landing> ", "color": "red"}, {"text": "Creepers are the wildfire of this age. Keep your distance!", "color": "white"}]
execute if score #r got_g matches 4 run tellraw @a[distance=..10] [{"text": "<Smallfolk of King's Landing> ", "color": "red"}, {"text": "The Red Keep has a great hall. Stand before the throne and remember: hold the gate.", "color": "white"}]
execute if score #r got_g matches 5 run tellraw @a[distance=..10] [{"text": "<Smallfolk of King's Landing> ", "color": "red"}, {"text": "Trade is slow, war is loud. Be brave, be quick.", "color": "white"}]
playsound minecraft:entity.villager.ambient master @a[distance=..10]
