# تسلسل فتح المدينة (يعمل من hook/tick بعدّاد #cityseq)
scoreboard players add #cityseq nh_story 1
execute if score #cityseq nh_story matches 1 run title @a times 10 80 30
execute if score #cityseq nh_story matches 1 run title @a subtitle {"text":"ستة أختام تُضيء... والبوّابة تتحرّك","color":"yellow"}
execute if score #cityseq nh_story matches 1 run title @a title {"text":"انفتحت مدينة النحاس!","color":"gold","bold":true}
execute if score #cityseq nh_story matches 1 as @a at @s run function nahas:fx/bell
execute if score #cityseq nh_story matches 1 as @a at @s run playsound minecraft:entity.lightning_bolt.thunder master @s ~ ~ ~ 3 0.7
execute if score #cityseq nh_story matches 40 run tellraw @a {"text":"دوّى في الأفق صوتُ جرسٍ عظيم... واهتزّت الرمال تحت أقدامكم.","color":"yellow"}
execute if score #cityseq nh_story matches 100 run tellraw @a {"text":"تحرّكت البوّابةُ الجنوبيةُ لمدينة النحاس ببطء، وخرج منها ضوءٌ ذهبي.","color":"gold"}
execute if score #cityseq nh_story matches 100..220 if score #cityseq nh_story matches 100 run playsound minecraft:block.beacon.activate master @a ~ ~ ~ 1 0.7
execute if score #cityseq nh_story matches 100..220 positioned 1200 72 1350 run function nahas:fx/gate_fx
execute if score #cityseq nh_story matches 160 positioned 1200 80 1345 run function nahas:fx/fireworks_ring
execute if score #cityseq nh_story matches 200 run tellraw @a [{"text":"اذهبوا إلى قلب المدينة، إلى ساحة القصر. ","color":"white"},{"text":"الحارس النحاسي ينتظركم هناك.","color":"red"}]
execute if score #cityseq nh_story matches 260.. run scoreboard players set #cityseq nh_story -1
