tag @s add nh_q4
scoreboard players add @s nh_gold 80
advancement grant @s only nahas:quest
tellraw @s ["",{"text":"أنجزت المهمة! +80 ذهب","color":"green"}]
playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1
