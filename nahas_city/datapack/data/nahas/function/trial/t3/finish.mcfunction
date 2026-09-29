clear @a minecraft:paper[minecraft:custom_data={nh:"page"}]
kill @e[tag=nh_t3,distance=..120]
tellraw @a[distance=..100] ["",{"text":"الصفحات الثلاث اكتملت! الكتب تعود إلى مكانها.","color":"green"}]
function nahas:trial/complete_3
