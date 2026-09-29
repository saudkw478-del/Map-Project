execute store result score #r got_g run random value 1..5
execute if score #r got_g matches 1 run tellraw @a[distance=..10] [{"text": "<Dornishman> ", "color": "gold"}, {"text": "Unbowed, Unbent, Unbroken! Welcome to Sunspear, traveler.", "color": "white"}]
execute if score #r got_g matches 2 run tellraw @a[distance=..10] [{"text": "<Dornishman> ", "color": "gold"}, {"text": "The sand snakes are quick. Watch for the ones who wear the scarves.", "color": "white"}]
execute if score #r got_g matches 3 run tellraw @a[distance=..10] [{"text": "<Dornishman> ", "color": "gold"}, {"text": "Drink water often. The sun here is a harsh master.", "color": "white"}]
execute if score #r got_g matches 4 run tellraw @a[distance=..10] [{"text": "<Dornishman> ", "color": "gold"}, {"text": "Sunspear is easy to hold if you keep the gate. Type /trigger got_battle to begin.", "color": "white"}]
execute if score #r got_g matches 5 run tellraw @a[distance=..10] [{"text": "<Dornishman> ", "color": "gold"}, {"text": "Beyond the Red Mountains lies the Reach. Bring a horse - the desert is long.", "color": "white"}]
playsound minecraft:entity.villager.ambient master @a[distance=..10]
