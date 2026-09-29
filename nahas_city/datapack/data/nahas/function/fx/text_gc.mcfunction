# تنظيف النصوص القديمة (كل ثانية): أي نص وسمه nh_txt يُحذف بعد 15 ثانية
scoreboard players add @e[type=minecraft:text_display,tag=nh_txt] nh_ttl 1
kill @e[type=minecraft:text_display,tag=nh_txt,scores={nh_ttl=15..}]
