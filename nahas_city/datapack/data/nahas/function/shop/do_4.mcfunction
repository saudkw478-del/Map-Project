scoreboard players remove @s nh_gold 20
loot give @s loot nahas:shop/torches
tellraw @s ["",{"text":"اشتريت: ","color":"green"},{"text":"مشاعل ×١٦","color":"gold"},{"text":"  باقي ذهبك: ","color":"green"},{"score":{"name":"@s","objective":"nh_gold"},"color":"yellow"}]
playsound minecraft:entity.villager.trade master @s ~ ~ ~ 1 1
advancement grant @s only nahas:shop
