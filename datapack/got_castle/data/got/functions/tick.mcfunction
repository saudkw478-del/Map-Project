scoreboard players enable @a got_go
scoreboard players enable @a got_battle
scoreboard players enable @a got_kit
scoreboard players enable @a got_house
scoreboard players enable @a got_power
scoreboard players enable @a got_shop
scoreboard players enable @a got_scout
scoreboard players enable @a got_quest
scoreboard players enable @a got_start
scoreboard players enable @a got_accuse
execute as @a[tag=!got_seen] run function got:player/first_join
execute as @a[scores={got_go=1..}] run function got:travel/handle
execute as @a[scores={got_battle=1..}] run function got:battle/handle
execute as @a[scores={got_kit=1..}] run function got:kit/handle
execute as @a[scores={got_house=1..}] run function got:house/handle
execute as @a[scores={got_power=1..}] run function got:power/handle
execute as @a[scores={got_shop=1..}] run function got:shop/handle
execute as @a[scores={got_scout=1..}] run function got:scout/handle
execute as @a[scores={got_quest=1..}] run function got:quest/handle
execute as @a[scores={got_start=1..}] run function got:camp/handle
execute as @a[scores={got_accuse=1..}] run function got:npc/accuse_handle
scoreboard players add #t got_g 1
execute if score #t got_g matches 20.. run function got:second
