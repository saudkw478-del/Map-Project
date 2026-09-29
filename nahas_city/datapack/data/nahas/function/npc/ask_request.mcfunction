# طلب تلميح من الجني (الذكاء الاصطناعي): يضع nh_askq=1 ليلتقطه جسر ai_bridge عبر RCON.
# يُستدعى من hook/tick عند استعمال nh_ask، ويمكن لـ CORE استدعاؤه مباشرة.
execute if score @s nh_askcd matches 1.. run return 0
scoreboard players set @s nh_askq 1
scoreboard players set @s nh_askcd 200
title @s actionbar {"text":"الجني الحكيم يفكّر في سؤالك...","color":"aqua"}
playsound minecraft:block.amethyst_block.chime master @s ~ ~ ~ 1 1.2
