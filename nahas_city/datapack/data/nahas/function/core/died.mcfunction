scoreboard players set @s nh_dead 0
tellraw @s {"text":"لا تخف، الجني يعيدك إلى الحياة. حاول مرة أخرى!","color":"yellow"}
function nahas:hook/player_death
