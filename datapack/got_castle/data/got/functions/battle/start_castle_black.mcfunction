kill @e[tag=got_origin]
summon minecraft:marker 250 64 236 {Tags:["got_origin"]}
scoreboard players set #site got_g 1
scoreboard players set #theme got_g 1
scoreboard players set #base got_g 0
scoreboard players set #total got_g 4
tellraw @a [{"text": "[BATTLE] ", "color": "red", "bold": true}, {"text": "Castle Black: The Night's Watch holds the Wall against the wildlings.", "color": "white"}]
function got:battle/begin
