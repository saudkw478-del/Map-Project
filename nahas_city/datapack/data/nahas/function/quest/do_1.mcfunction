tag @s add nh_q1
scoreboard players add @s nh_gold 30
advancement grant @s only nahas:quest
tellraw @s ["",{"text":"أنجزت المهمة! +30 ذهب","color":"green"}]
playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1
