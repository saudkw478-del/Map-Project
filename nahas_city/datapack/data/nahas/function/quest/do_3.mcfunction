tag @s add nh_q3
scoreboard players add @s nh_gold 60
advancement grant @s only nahas:quest
tellraw @s ["",{"text":"أنجزت المهمة! +60 ذهب","color":"green"}]
playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1
loot give @s loot nahas:gift/traveler
