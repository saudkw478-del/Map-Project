scoreboard players remove @s nh_gold 80
loot give @s loot nahas:shop/bottle
tellraw @s ["",{"text":"اشتريت: ","color":"green"},{"text":"قارورة الجني","color":"gold"},{"text":"  باقي ذهبك: ","color":"green"},{"score":{"name":"@s","objective":"nh_gold"},"color":"yellow"}]
playsound minecraft:entity.villager.trade master @s ~ ~ ~ 1 1
advancement grant @s only nahas:shop
