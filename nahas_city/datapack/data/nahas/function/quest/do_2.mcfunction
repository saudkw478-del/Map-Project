tag @s add nh_q2
scoreboard players add @s nh_gold 100
advancement grant @s only nahas:quest
tellraw @s ["",{"text":"أنجزت المهمة! +100 ذهب","color":"green"}]
playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1
loot give @s loot nahas:shop/heal
