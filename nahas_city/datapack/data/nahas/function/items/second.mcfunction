execute if items entity @s weapon.* minecraft:lantern[minecraft:custom_data={nh:"lantern"}] run function nahas:items/lantern_aura
execute if items entity @s weapon.* minecraft:netherite_sword[minecraft:custom_data={nh:"scimitar"}] run effect give @s minecraft:speed 3 0 true
execute if items entity @s weapon.mainhand minecraft:golden_sword[minecraft:custom_data={nh:"dagger"}] run effect give @s minecraft:haste 3 0 true
execute if items entity @s hotbar.* minecraft:totem_of_undying[minecraft:custom_data={nh:"amulet"}] run effect give @s minecraft:luck 3 0 true
