# يُضيء الفانوس ويشتعل
execute as @e[type=minecraft:item_display,tag=nh_lantern] run data merge entity @s {start_interpolation:0,interpolation_duration:40,glow_color_override:16766720,Glowing:1b,transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.5f,0f],scale:[2.4f,2.4f,2.4f]}}
execute in minecraft:overworld if block 300 76 2050 minecraft:air run setblock 300 76 2050 minecraft:light[level=15]
execute in minecraft:overworld run particle minecraft:end_rod 300 76 2050 2 2 2 0.1 80 force
execute in minecraft:overworld run particle minecraft:flame 300 76 2050 1 1 1 0.05 60 force
execute in minecraft:overworld run particle minecraft:soul_fire_flame 300 76 2050 1.5 1 1.5 0.05 40 force
playsound minecraft:block.beacon.activate master @s ~ ~ ~ 2 1
playsound minecraft:block.respawn_anchor.charge master @s ~ ~ ~ 2 1
