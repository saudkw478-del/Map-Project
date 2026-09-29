advancement revoke @s only got:npc_talk
execute if score @s got_talkcd matches 1.. run return 0
scoreboard players set @s got_talkcd 30
execute as @e[type=minecraft:villager,tag=got_npc,sort=nearest,limit=1,distance=..8] at @s run function got:npc/speak
execute unless score @s got_gift matches 1.. run function got:npc/maybe_gift
