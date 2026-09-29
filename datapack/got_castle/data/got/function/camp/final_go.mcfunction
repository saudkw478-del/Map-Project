execute if score #cs_castle_black got_g matches 3 run summon minecraft:iron_golem 264 64 372 {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}
execute if score #cs_castle_black got_g matches 3 run summon minecraft:iron_golem 267 64 374 {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}
execute if score #cs_riverrun got_g matches 3 run summon minecraft:iron_golem 276 64 372 {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}
execute if score #cs_riverrun got_g matches 3 run summon minecraft:iron_golem 261 64 376 {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}
execute if score #cs_eyrie got_g matches 3 run summon minecraft:iron_golem 279 64 376 {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}
execute if score #cs_eyrie got_g matches 3 run summon minecraft:iron_golem 270 64 377 {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}
execute if score #cs_kings_landing got_g matches 3 run summon minecraft:iron_golem 264 64 372 {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}
execute if score #cs_kings_landing got_g matches 3 run summon minecraft:iron_golem 267 64 374 {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}
execute if score #cs_casterly_rock got_g matches 3 run summon minecraft:iron_golem 270 64 372 {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}
execute if score #cs_casterly_rock got_g matches 3 run summon minecraft:iron_golem 273 64 374 {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}
execute if score #cs_highgarden got_g matches 3 run summon minecraft:iron_golem 276 64 372 {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}
execute if score #cs_highgarden got_g matches 3 run summon minecraft:iron_golem 261 64 376 {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}
execute if score #cs_storms_end got_g matches 3 run summon minecraft:iron_golem 279 64 376 {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}
execute if score #cs_storms_end got_g matches 3 run summon minecraft:iron_golem 270 64 377 {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}
execute if score #cs_sunspear got_g matches 3 run summon minecraft:iron_golem 264 64 372 {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}
execute if score #cs_sunspear got_g matches 3 run summon minecraft:iron_golem 267 64 374 {Tags:["got_ally"],PlayerCreated:1b,PersistenceRequired:1b}
scoreboard players set #camp_battle got_g 1
function got:battle/start_winterfell
title @a title {"text": "\u0645\u0644\u0643 \u0627\u0644\u0644\u064a\u0644 \u0642\u0627\u062f\u0645!", "color": "dark_red", "bold": true}
title @a subtitle {"text": "\u0647\u0630\u0647 \u0647\u064a \u0627\u0644\u0645\u0639\u0631\u0643\u0629 \u0627\u0644\u0623\u062e\u064a\u0631\u0629", "color": "gray"}
tellraw @a [{"text": "\u062d\u0644\u0641\u0627\u0624\u0643\u0645: ", "color": "green", "bold": true}, {"score": {"name": "#held", "objective": "got_g"}, "color": "green"}, {"text": " \u0642\u0644\u0639\u0629 \u0635\u0627\u0645\u062f\u0629 | \u0623\u0639\u062f\u0627\u0624\u0643\u0645 \u0632\u0627\u062f\u0648\u0627 \u0628\u0633\u0628\u0628 ", "color": "gray"}, {"score": {"name": "#fallen", "objective": "got_g"}, "color": "red"}, {"text": " \u0642\u0644\u0639\u0629 \u0633\u0627\u0642\u0637\u0629", "color": "red"}]
