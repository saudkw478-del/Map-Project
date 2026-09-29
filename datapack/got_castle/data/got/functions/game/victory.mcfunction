scoreboard players set #state got_g 4
title @a title {"text": "VICTORY!", "color": "gold", "bold": true}
title @a subtitle {"text": "The castle is held!", "color": "aqua"}
effect give @a minecraft:regeneration 30 2 true
xp add @a 30 levels
loot give @a loot got:reward/trophy
playsound minecraft:ui.toast.challenge_complete master @a
scoreboard players add Victories got_g 1
execute if score #site got_g matches 1 run scoreboard players set #won_castle_black got_g 1
execute if score #site got_g matches 2 run scoreboard players set #won_winterfell got_g 1
execute if score #site got_g matches 3 run scoreboard players set #won_riverrun got_g 1
execute if score #site got_g matches 4 run scoreboard players set #won_eyrie got_g 1
execute if score #site got_g matches 5 run scoreboard players set #won_kings_landing got_g 1
execute if score #site got_g matches 6 run scoreboard players set #won_casterly_rock got_g 1
execute if score #site got_g matches 7 run scoreboard players set #won_highgarden got_g 1
execute if score #site got_g matches 8 run scoreboard players set #won_storms_end got_g 1
execute if score #site got_g matches 9 run scoreboard players set #won_sunspear got_g 1
tellraw @a [{"text": "Castles conquered: ", "color": "gold"}, {"score": {"name": "Victories", "objective": "got_g"}, "color": "white"}, {"text": " of 9", "color": "gold"}]
execute if score #won_winterfell got_g matches 1 if score #won_kings_landing got_g matches 1 if score #won_castle_black got_g matches 1 run tellraw @a {"text": "The realm is saved! The Long Night is over and the Iron Throne is safe.", "color": "yellow", "bold": true}
tellraw @a {"text": "Start another battle with /trigger got_battle (or travel with /trigger got_go).", "color": "gray"}
