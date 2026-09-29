tag @s add nh_q5
scoreboard players add @s nh_gold 150
advancement grant @s only nahas:quest
tellraw @s ["",{"text":"أنجزت المهمة! +150 ذهب","color":"green"}]
playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1
loot give @s loot nahas:items/amulet
