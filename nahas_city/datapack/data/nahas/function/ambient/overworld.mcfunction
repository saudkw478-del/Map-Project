# أجواء العالم العادي حسب المنطقة
execute if score #night nh_story matches 1 run function nahas:ambient/night
execute if entity @s[x=300,y=70,z=2050,distance=..90] run function nahas:ambient/z_spawn
execute if entity @s[x=600,y=70,z=1650,distance=..80] run function nahas:ambient/z_hub
execute if entity @s[x=1000,y=70,z=1900,distance=..80] run function nahas:ambient/z_t1
execute if entity @s[x=1800,y=70,z=1850,distance=..80] run function nahas:ambient/z_t2
execute if entity @s[x=2100,y=70,z=1300,distance=..80] run function nahas:ambient/z_t3
execute if entity @s[x=1700,y=70,z=450,distance=..80] run function nahas:ambient/z_t4
execute if entity @s[x=1000,y=70,z=350,distance=..70] run function nahas:ambient/z_g_star
execute if entity @s[x=300,y=70,z=900,distance=..70] run function nahas:ambient/z_g_ember
execute if entity @s[x=1200,y=70,z=1200,distance=..170] run function nahas:ambient/z_city
