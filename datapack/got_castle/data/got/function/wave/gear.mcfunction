execute if score #gear got_g matches 0..2 run item replace entity @s armor.head with minecraft:leather_helmet
execute if score #gear got_g matches 3..4 run item replace entity @s armor.head with minecraft:chainmail_helmet
execute if score #gear got_g matches 3..4 run item replace entity @s armor.chest with minecraft:chainmail_chestplate
execute if score #gear got_g matches 5..6 run item replace entity @s armor.head with minecraft:iron_helmet
execute if score #gear got_g matches 5..6 run item replace entity @s armor.chest with minecraft:iron_chestplate
execute if score #gear got_g matches 7..99 run item replace entity @s armor.head with minecraft:diamond_helmet
execute if score #gear got_g matches 7..99 run item replace entity @s armor.chest with minecraft:diamond_chestplate
execute if entity @s[type=minecraft:zombie] if score #gear got_g matches 3..5 run item replace entity @s weapon.mainhand with minecraft:iron_sword
execute if entity @s[type=minecraft:zombie] if score #gear got_g matches 6.. run item replace entity @s weapon.mainhand with minecraft:diamond_sword
execute if entity @s[type=minecraft:husk] if score #gear got_g matches 3..5 run item replace entity @s weapon.mainhand with minecraft:iron_sword
execute if entity @s[type=minecraft:husk] if score #gear got_g matches 6.. run item replace entity @s weapon.mainhand with minecraft:diamond_sword
