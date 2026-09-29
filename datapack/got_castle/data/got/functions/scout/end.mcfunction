tag @s add got_me
spectate
gamemode survival @s
execute as @e[type=minecraft:marker,tag=got_back] if score @s got_id = @a[tag=got_me,limit=1] got_id at @s run tp @a[tag=got_me,limit=1] @s
execute as @e[type=minecraft:marker,tag=got_back] if score @s got_id = @a[tag=got_me,limit=1] got_id run kill @s
execute as @e[type=minecraft:bat,tag=got_eye] if score @s got_id = @a[tag=got_me,limit=1] got_id run kill @s
tag @s remove got_scouting
tag @s remove got_me
title @s actionbar {"text": "\u0639\u0627\u062f \u0627\u0644\u063a\u0631\u0627\u0628.", "color": "gray"}
