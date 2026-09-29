function nahas:core/triggers
function nahas:portal/tick
function nahas:items/tick
scoreboard players add #tk nh_g 1
execute if score #tk nh_g matches 20.. run function nahas:core/second
function nahas:hook/tick
