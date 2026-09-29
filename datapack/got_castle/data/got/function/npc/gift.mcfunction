scoreboard players set @s got_gift 2400
loot give @s loot got:reward/supplies
tellraw @s {"text": "The villager presses some supplies into your hands.", "color": "green", "italic": true}
playsound minecraft:entity.villager.celebrate master @s
