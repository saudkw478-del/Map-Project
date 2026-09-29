execute store result score #r got_g run random value 1..5
execute if score #r got_g matches 1 run tellraw @a[distance=..10] [{"text": "<Northman> ", "color": "aqua"}, {"text": "Winter is coming. Keep your sword sharp and your torch lit.", "color": "white"}]
execute if score #r got_g matches 2 run tellraw @a[distance=..10] [{"text": "<Northman> ", "color": "aqua"}, {"text": "The Stark words are true - the lone wolf dies, but the pack survives. Fight beside your friends.", "color": "white"}]
execute if score #r got_g matches 3 run tellraw @a[distance=..10] [{"text": "<Northman> ", "color": "aqua"}, {"text": "Type /trigger got_go to see every castle you can travel to.", "color": "white"}]
execute if score #r got_g matches 4 run tellraw @a[distance=..10] [{"text": "<Northman> ", "color": "aqua"}, {"text": "Winterfell has held for a thousand years. Hold it for a few waves more, and it will hold forever.", "color": "white"}]
execute if score #r got_g matches 5 run tellraw @a[distance=..10] [{"text": "<Northman> ", "color": "aqua"}, {"text": "Stand on the walls with a bow. The gate is easier to hold from above.", "color": "white"}]
playsound minecraft:entity.villager.ambient master @a[distance=..10]
