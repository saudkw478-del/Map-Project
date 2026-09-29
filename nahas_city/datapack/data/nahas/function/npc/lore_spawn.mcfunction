# حجر حكاية: كتلة + عنوان عائم (ماكرو). الموضع الثابت مبني على ارتفاع أرض المواقع في SPEC.
$setblock $(x) $(y) $(z) minecraft:chiseled_polished_blackstone
$execute if score #textmode nh_story matches 0 run summon minecraft:text_display $(x) $(yt) $(z) {Tags:["nh_fx","nh_lore_$(id)"],billboard:"center",alignment:"center",shadow:1b,see_through:0b,text:'{"text":"$(name)","color":"gold","bold":true}'}
$execute if score #textmode nh_story matches 1 run summon minecraft:text_display $(x) $(yt) $(z) {Tags:["nh_fx","nh_lore_$(id)"],billboard:"center",alignment:"center",shadow:1b,see_through:0b,text:{text:"$(name)",color:"gold",bold:true}}
