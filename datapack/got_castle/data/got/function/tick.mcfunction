scoreboard players enable @a got_go
scoreboard players enable @a got_battle
scoreboard players enable @a got_kit
execute as @a[tag=!got_seen] run function got:player/first_join
execute as @a[scores={got_go=1..}] run function got:travel/handle
execute as @a[scores={got_battle=1..}] run function got:battle/handle
execute as @a[scores={got_kit=1..}] run function got:kit/handle
scoreboard players add #rt got_g 1
execute if score #rt got_g matches 20.. run function got:region/check
execute if score #state got_g matches 1..2 run function got:game/loop
