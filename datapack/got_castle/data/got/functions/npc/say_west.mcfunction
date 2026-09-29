execute store result score #r got_g run random value 1..5
execute if score #r got_g matches 1 run tellraw @a[distance=..10] [{"text": "<Westerman> ", "color": "gold"}, {"text": "Hear me roar! A Lannister always pays his debts.", "color": "white"}]
execute if score #r got_g matches 2 run tellraw @a[distance=..10] [{"text": "<Westerman> ", "color": "gold"}, {"text": "Casterly Rock has more gold than the rest of the kingdom together. Sadly, none for you.", "color": "white"}]
execute if score #r got_g matches 3 run tellraw @a[distance=..10] [{"text": "<Westerman> ", "color": "gold"}, {"text": "Take the golden armor from the chests. It suits you.", "color": "white"}]
execute if score #r got_g matches 4 run tellraw @a[distance=..10] [{"text": "<Westerman> ", "color": "gold"}, {"text": "The Goldroad is safe from bandits - as long as the army stands.", "color": "white"}]
execute if score #r got_g matches 5 run tellraw @a[distance=..10] [{"text": "<Westerman> ", "color": "gold"}, {"text": "Fight in the courtyard, not the gate. The rock is behind you.", "color": "white"}]
playsound minecraft:entity.villager.ambient master @a[distance=..10]
