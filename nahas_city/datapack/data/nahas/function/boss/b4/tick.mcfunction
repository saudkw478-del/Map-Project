bossbar set nahas:boss4 players @a[distance=..100]
execute store result score #hp nh_g run data get entity @s Health
execute store result bossbar nahas:boss4 value run data get entity @s Health
scoreboard players operation #pct nh_g = #hp nh_g
scoreboard players operation #pct nh_g *= #100 nh_g
scoreboard players operation #pct nh_g /= #bmax4 nh_g
scoreboard players set #np nh_g 1
execute if score #pct nh_g matches ..66 run scoreboard players set #np nh_g 2
execute if score #pct nh_g matches ..33 run scoreboard players set #np nh_g 3
execute unless score #np nh_g = #b4_ph nh_g run function nahas:boss/b4/phase
scoreboard players add #b4_t nh_g 1
execute if score #b4_t nh_g matches 5.. run function nahas:boss/b4/act
