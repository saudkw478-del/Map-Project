title @a[distance=..12] title {"text": "\u0643\u064f\u0634\u0641 \u0627\u0644\u0648\u062c\u0647 \u0627\u0644\u062e\u0641\u064a!", "color": "dark_red", "bold": true}
tellraw @a[distance=..12] [{"text": "<\u0627\u0644\u0642\u0627\u062a\u0644> ", "color": "dark_gray", "bold": true}, {"text": "...\u0643\u064a\u0641 \u0639\u0631\u0641\u062a\u064e\u061f! \u0644\u0646 \u062a\u0646\u062c\u0648!", "color": "red"}]
summon minecraft:vindicator ~ ~ ~ {Tags:["got_assassin","got_assassin_new"],PersistenceRequired:1b}
execute as @e[tag=got_assassin_new] run item replace entity @s armor.head with minecraft:iron_helmet
execute as @e[tag=got_assassin_new] run item replace entity @s armor.chest with minecraft:iron_chestplate
tag @e[tag=got_assassin_new] remove got_assassin_new
scoreboard players add @p[distance=..8] got_gold 15
scoreboard players add @p[distance=..8] got_renown 5
playsound minecraft:entity.evoker.prepare_summon master @a[distance=..20]
kill @s
