kill @e[tag=got_origin]
kill @e[tag=got_gate]
kill @e[tag=got_center]
execute align xyz run summon minecraft:marker ~ ~ ~ {Tags:["got_origin"]}
tellraw @a {"text": "Building the castle... stay near the center for ~20 seconds.", "color": "yellow"}
execute at @e[tag=got_origin,limit=1] run forceload add ~-60 ~-60 ~60 ~60
schedule function got:build/s1_ground 40t
