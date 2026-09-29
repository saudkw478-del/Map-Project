scoreboard players remove @s nh_gold 120
loot give @s loot nahas:shop/amulet
tellraw @s ["",{"text":"اشتريت: ","color":"green"},{"text":"تميمة الحماية","color":"gold"},{"text":"  باقي ذهبك: ","color":"green"},{"score":{"name":"@s","objective":"nh_gold"},"color":"yellow"}]
playsound minecraft:entity.villager.trade master @s ~ ~ ~ 1 1
advancement grant @s only nahas:shop
