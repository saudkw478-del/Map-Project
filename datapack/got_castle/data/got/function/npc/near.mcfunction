execute positioned 395 64 470 if entity @s[distance=..70] unless score #npc_white_harbor got_g matches 1 unless score #cs_white_harbor got_g matches 2 run function got:npc/spawn_white_harbor
execute positioned 96 64 850 if entity @s[distance=..70] unless score #npc_lannisport got_g matches 1 unless score #cs_lannisport got_g matches 2 run function got:npc/spawn_lannisport
execute positioned 138 64 1155 if entity @s[distance=..70] unless score #npc_oldtown got_g matches 1 unless score #cs_oldtown got_g matches 2 run function got:npc/spawn_oldtown
execute positioned 560 64 668 if entity @s[distance=..70] unless score #npc_gulltown got_g matches 1 unless score #cs_gulltown got_g matches 2 run function got:npc/spawn_gulltown
execute positioned 302 64 480 if entity @s[distance=..70] unless score #npc_kingsroad_inn_1 got_g matches 1 unless score #cs_kingsroad_inn_1 got_g matches 2 run function got:npc/spawn_kingsroad_inn_1
execute positioned 215 64 452 if entity @s[distance=..70] unless score #npc_winter_town got_g matches 1 unless score #cs_winter_town got_g matches 2 run function got:npc/spawn_winter_town
execute positioned 360 64 868 if entity @s[distance=..70] unless score #npc_kl_city got_g matches 1 unless score #cs_kl_city got_g matches 2 run function got:npc/spawn_kl_city
execute positioned 250 64 236 if entity @s[distance=..70] unless score #npc_castle_black got_g matches 1 unless score #cs_castle_black got_g matches 2 run function got:npc/spawn_castle_black
execute positioned 250 64 236 if entity @s[distance=..70] if score #cs_castle_black got_g matches 2 run kill @e[tag=got_grp_castle_black,distance=..90]
execute positioned 270 64 350 if entity @s[distance=..70] unless score #npc_winterfell got_g matches 1 unless score #cs_winterfell got_g matches 2 run function got:npc/spawn_winterfell
execute positioned 270 64 350 if entity @s[distance=..70] if score #cs_winterfell got_g matches 2 run kill @e[tag=got_grp_winterfell,distance=..90]
execute positioned 215 64 720 if entity @s[distance=..70] unless score #npc_riverrun got_g matches 1 unless score #cs_riverrun got_g matches 2 run function got:npc/spawn_riverrun
execute positioned 215 64 720 if entity @s[distance=..70] if score #cs_riverrun got_g matches 2 run kill @e[tag=got_grp_riverrun,distance=..90]
execute positioned 500 124 690 if entity @s[distance=..70] unless score #npc_eyrie got_g matches 1 unless score #cs_eyrie got_g matches 2 run function got:npc/spawn_eyrie
execute positioned 500 124 690 if entity @s[distance=..70] if score #cs_eyrie got_g matches 2 run kill @e[tag=got_grp_eyrie,distance=..90]
execute positioned 405 64 880 if entity @s[distance=..70] unless score #npc_kings_landing got_g matches 1 unless score #cs_kings_landing got_g matches 2 run function got:npc/spawn_kings_landing
execute positioned 405 64 880 if entity @s[distance=..70] if score #cs_kings_landing got_g matches 2 run kill @e[tag=got_grp_kings_landing,distance=..90]
execute positioned 140 64 800 if entity @s[distance=..70] unless score #npc_casterly_rock got_g matches 1 unless score #cs_casterly_rock got_g matches 2 run function got:npc/spawn_casterly_rock
execute positioned 140 64 800 if entity @s[distance=..70] if score #cs_casterly_rock got_g matches 2 run kill @e[tag=got_grp_casterly_rock,distance=..90]
execute positioned 215 64 1030 if entity @s[distance=..70] unless score #npc_highgarden got_g matches 1 unless score #cs_highgarden got_g matches 2 run function got:npc/spawn_highgarden
execute positioned 215 64 1030 if entity @s[distance=..70] if score #cs_highgarden got_g matches 2 run kill @e[tag=got_grp_highgarden,distance=..90]
execute positioned 480 64 1005 if entity @s[distance=..70] unless score #npc_storms_end got_g matches 1 unless score #cs_storms_end got_g matches 2 run function got:npc/spawn_storms_end
execute positioned 480 64 1005 if entity @s[distance=..70] if score #cs_storms_end got_g matches 2 run kill @e[tag=got_grp_storms_end,distance=..90]
execute positioned 470 64 1235 if entity @s[distance=..70] unless score #npc_sunspear got_g matches 1 unless score #cs_sunspear got_g matches 2 run function got:npc/spawn_sunspear
execute positioned 470 64 1235 if entity @s[distance=..70] if score #cs_sunspear got_g matches 2 run kill @e[tag=got_grp_sunspear,distance=..90]
execute positioned 250 64 236 if entity @s[distance=..70] if score #cs_castle_black got_g matches 2 unless score #wt_castle_black got_g matches 1 run function got:camp/wights_castle_black
execute positioned 270 64 350 if entity @s[distance=..70] if score #cs_winterfell got_g matches 2 unless score #wt_winterfell got_g matches 1 run function got:camp/wights_winterfell
execute positioned 215 64 720 if entity @s[distance=..70] if score #cs_riverrun got_g matches 2 unless score #wt_riverrun got_g matches 1 run function got:camp/wights_riverrun
execute positioned 500 124 690 if entity @s[distance=..70] if score #cs_eyrie got_g matches 2 unless score #wt_eyrie got_g matches 1 run function got:camp/wights_eyrie
execute positioned 405 64 880 if entity @s[distance=..70] if score #cs_kings_landing got_g matches 2 unless score #wt_kings_landing got_g matches 1 run function got:camp/wights_kings_landing
execute positioned 140 64 800 if entity @s[distance=..70] if score #cs_casterly_rock got_g matches 2 unless score #wt_casterly_rock got_g matches 1 run function got:camp/wights_casterly_rock
execute positioned 215 64 1030 if entity @s[distance=..70] if score #cs_highgarden got_g matches 2 unless score #wt_highgarden got_g matches 1 run function got:camp/wights_highgarden
execute positioned 480 64 1005 if entity @s[distance=..70] if score #cs_storms_end got_g matches 2 unless score #wt_storms_end got_g matches 1 run function got:camp/wights_storms_end
execute positioned 470 64 1235 if entity @s[distance=..70] if score #cs_sunspear got_g matches 2 unless score #wt_sunspear got_g matches 1 run function got:camp/wights_sunspear
