# جدول أحداث الافتتاحية (المنفّذ: اللاعب؛ nh_intro = رقم الـ tick)
execute if score @s nh_intro matches 1 run tellraw @s [{"text":"للتخطي اكتب ","color":"gray"},{"text":"/trigger nh_start set 1","color":"yellow","clickEvent":{"action":"run_command","value":"/trigger nh_start set 1"},"click_event":{"action":"run_command","command":"/trigger nh_start set 1"}},{"text":" (أو اضغط هنا)","color":"gray"}]
execute if score @s nh_intro matches 1 run function nahas:fx/wind
execute if score @s nh_intro matches 8 run title @s times 10 50 10
execute if score @s nh_intro matches 8 run title @s subtitle {"text":"في ليالي ألف ليلةٍ وليلة...","color":"yellow"}
execute if score @s nh_intro matches 8 run title @s title {"text":" ","color":"gold","bold":true}
execute if score @s nh_intro matches 40 run function nahas:fx/whisper
execute if score @s nh_intro matches 70 run title @s times 10 50 10
execute if score @s nh_intro matches 70 run title @s subtitle {"text":"رُويَ أنّ في قلب الصحراء مدينةً كلّها من نحاس...","color":"yellow"}
execute if score @s nh_intro matches 70 run title @s title {"text":" ","color":"gold","bold":true}
execute if score @s nh_intro matches 100 run function nahas:fx/thunder_far
execute if score @s nh_intro matches 135 run title @s times 10 45 10
execute if score @s nh_intro matches 135 run title @s subtitle {"text":"أهلُها ناموا... وصاروا تماثيل","color":"yellow"}
execute if score @s nh_intro matches 135 run title @s title {"text":" ","color":"gold","bold":true}
execute if score @s nh_intro matches 185 run function nahas:fx/thunder
execute if score @s nh_intro matches 185 run function nahas:fx/flash
execute if score @s nh_intro matches 205 run function nahas:fx/text_clear
execute if score @s nh_intro matches 205 run execute at @s run function nahas:fx/text {msg:"الليلةَ... تستيقظ مدينةُ النحاس",color:"gold"}
execute if score @s nh_intro matches 260 run function nahas:fx/text_clear
execute if score @s nh_intro matches 260 run execute at @s run function nahas:fx/text {msg:"عاصفةُ رمالٍ ابتلعت قافلتكم",color:"yellow"}
execute if score @s nh_intro matches 260 run function nahas:fx/thunder_far
execute if score @s nh_intro matches 320 run function nahas:fx/text_clear
execute if score @s nh_intro matches 320 run execute at @s run function nahas:fx/text {msg:"وفي الحطام... فانوسٌ قديم يهمس بأسمائكم",color:"aqua"}
execute if score @s nh_intro matches 380 run function nahas:fx/text_clear
execute if score @s nh_intro matches 380 run execute at @s run function nahas:fx/text {msg:"سبعةُ أختامٍ من نحاس... تُنقذ النائمين",color:"gold"}
execute if score @s nh_intro matches 380 run function nahas:fx/thunder
execute if score @s nh_intro matches 380 run function nahas:fx/flash
execute if score @s nh_intro matches 410 run function nahas:fx/text_clear
execute if score @s nh_intro matches 414 run effect give @s minecraft:blindness 2 0 true
execute if score @s nh_intro matches 420 run function nahas:fx/lantern_spawn
execute if score @s nh_intro matches 440 run function nahas:fx/text_clear
execute if score @s nh_intro matches 440 run execute at @s run function nahas:fx/text {msg:"افتحوا عيونكم يا مسافرون",color:"white"}
execute if score @s nh_intro matches 470 run function nahas:fx/text_clear
execute if score @s nh_intro matches 470 run execute at @s run function nahas:fx/text {msg:"اشتعل الفانوس!",color:"yellow"}
execute if score @s nh_intro matches 470 run function nahas:fx/lantern_on
execute if score @s nh_intro matches 520 run function nahas:fx/text_clear
execute if score @s nh_intro matches 520 run function nahas:fx/thunder
execute if score @s nh_intro matches 520 run title @s times 20 80 30
execute if score @s nh_intro matches 520 run title @s subtitle {"text":"ليلة الفانوس","color":"yellow"}
execute if score @s nh_intro matches 520 run title @s title {"text":"مدينة النحاس","color":"gold","bold":true}
execute if score @s nh_intro matches 520 run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
execute if score @s nh_intro matches 520 run execute positioned 300 72 2050 run function nahas:fx/fireworks_ring
execute if score @s nh_intro matches 565 run function nahas:fx/text_clear
execute if score @s nh_intro matches 565 run execute at @s run function nahas:fx/text {msg:"اكتبوا /trigger nh_help لتعرفوا كيف تلعبون",color:"green"}
execute if score @s nh_intro matches 595 run function nahas:fx/text_clear
execute if score @s nh_intro matches 610 run function nahas:intro/end
