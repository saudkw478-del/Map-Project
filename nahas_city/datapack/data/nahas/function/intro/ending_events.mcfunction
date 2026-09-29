# جدول أحداث النهاية الكبرى
execute if score @s nh_intro matches 20 run function nahas:fx/text_clear
execute if score @s nh_intro matches 20 run execute at @s run function nahas:fx/text {msg:"سقط الحارسُ النحاسي... وانكسر السحر",color:"gold"}
execute if score @s nh_intro matches 20 run title @s times 10 70 20
execute if score @s nh_intro matches 20 run title @s subtitle {"text":"سقط الحارس النحاسي","color":"yellow"}
execute if score @s nh_intro matches 20 run title @s title {"text":"انتصرتم!","color":"gold","bold":true}
execute if score @s nh_intro matches 25 run execute positioned 1200 74 1200 run function nahas:fx/fireworks_ring
execute if score @s nh_intro matches 25 run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
execute if score @s nh_intro matches 90 run function nahas:fx/text_clear
execute if score @s nh_intro matches 90 run execute at @s run function nahas:fx/text {msg:"ارتجفت التماثيل في كل الشوارع... ثم تنفّست",color:"aqua"}
execute if score @s nh_intro matches 90 run playsound minecraft:block.beacon.activate master @s ~ ~ ~ 2 0.8
execute if score @s nh_intro matches 150 run execute positioned 1200 74 1200 run function nahas:fx/fireworks_ring
execute if score @s nh_intro matches 150 run function nahas:fx/bell
execute if score @s nh_intro matches 170 run function nahas:fx/weather_clear
execute if score @s nh_intro matches 170 run function nahas:fx/set_dawn
execute if score @s nh_intro matches 200 run function nahas:fx/text_clear
execute if score @s nh_intro matches 200 run execute at @s run function nahas:fx/text {msg:"وعاد أهلُ المدينة إلى الحياة بعد ألف ليلةٍ وليلة",color:"yellow"}
execute if score @s nh_intro matches 260 run execute positioned 1200 74 1200 run function nahas:fx/fireworks_ring
execute if score @s nh_intro matches 260 run execute positioned 1230 74 1170 run function nahas:fx/fireworks_ring
execute if score @s nh_intro matches 320 run function nahas:fx/text_clear
execute if score @s nh_intro matches 320 run execute at @s run function nahas:fx/text {msg:"بفضل شجاعتكم يا أبطال القافلة",color:"green"}
execute if score @s nh_intro matches 380 run execute positioned 1200 74 1200 run function nahas:fx/fireworks_ring
execute if score @s nh_intro matches 380 run function nahas:fx/bell
execute if score @s nh_intro matches 440 run function nahas:fx/text_clear
execute if score @s nh_intro matches 440 run execute at @s run function nahas:fx/text {msg:"وأدرك شهرزادَ الصباح... فسكتت عن الكلام المباح",color:"light_purple"}
execute if score @s nh_intro matches 500 run function nahas:fx/text_clear
execute if score @s nh_intro matches 500 run title @s times 20 80 30
execute if score @s nh_intro matches 500 run title @s subtitle {"text":"شكرًا لكم أيها الأبطال","color":"yellow"}
execute if score @s nh_intro matches 500 run title @s title {"text":"النهاية","color":"gold","bold":true}
execute if score @s nh_intro matches 540 run tellraw @s [{"text":"الأبطال: ","color":"gold","bold":true},{"selector":"@a"}]
execute if score @s nh_intro matches 600 run execute positioned 1200 74 1200 run function nahas:fx/fireworks_ring
execute if score @s nh_intro matches 600 run execute positioned 1170 74 1230 run function nahas:fx/fireworks_ring
execute if score @s nh_intro matches 600 run execute positioned 1230 74 1230 run function nahas:fx/fireworks_ring
execute if score @s nh_intro matches 680 run function nahas:fx/text_clear
execute if score @s nh_intro matches 680 run execute at @s run function nahas:fx/text {msg:"وبدايةُ حكايةٍ جديدة... فالصحراء ما زالت مليئة بالأسرار",color:"white"}
execute if score @s nh_intro matches 740 run function nahas:fx/text_clear
execute if score @s nh_intro matches 755 run function nahas:intro/end
