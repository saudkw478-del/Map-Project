# يُستدعى كل tick من CORE (إن وُجد)
# أداء: الأوامر أدناه لا تعمل فعليًا إلا عند وجود لاعب في مشهد سينمائي أو تسلسل نشط.
execute if score #cityseq nh_story matches 0.. run function nahas:story/city_tick
scoreboard players enable @a[scores={nh_intro=0..}] nh_start
execute as @a[scores={nh_intro=0..,nh_start=9}] run function nahas:intro/skip
execute as @a[scores={nh_intro=0..,nh_scene=1}] at @s run function nahas:intro/tick
execute as @a[scores={nh_intro=0..,nh_scene=2}] at @s run function nahas:intro/ending_tick
# مؤقّت الأمان: أي مشهد يتجاوز 1500 tick يُنهى قسرًا ويُعاد وضع اللعب
execute as @a[scores={nh_intro=1500..}] run function nahas:intro/end
scoreboard players remove @a[scores={nh_askcd=1..}] nh_askcd 1
execute as @a[scores={nh_ask=1..}] run function nahas:npc/ask_request
