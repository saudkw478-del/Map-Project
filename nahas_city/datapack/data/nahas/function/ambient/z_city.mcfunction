# أجواء: مدينة النحاس (1200,1200) نصف القطر 170
particle minecraft:dust{color:[0.9,0.55,0.2],scale:1.2} ~ ~2 ~ 12 4 12 0.05 12 normal @s
execute if score #night nh_story matches 1 if score #r nh_story matches 1..8 run playsound minecraft:block.bell.resonate master @s ~ ~ ~ 0.3 0.5
execute if score #night nh_story matches 1 if score #r nh_story matches 9..14 run function nahas:fx/whisper
