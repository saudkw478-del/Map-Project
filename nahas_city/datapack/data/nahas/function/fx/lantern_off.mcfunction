# يزيل عرض الفانوس وكتلة الضوء المؤقتة
kill @e[type=minecraft:item_display,tag=nh_lantern]
execute in minecraft:overworld if block 300 76 2050 minecraft:light run setblock 300 76 2050 minecraft:air
