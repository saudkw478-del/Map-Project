#!/usr/bin/env python3
"""CORE datapack generator for "مدينة النحاس" (namespace nahas).
Owns: function/{core,trial,items,shop,portal,boss,role,quest}, selftest, loot_table, advancement, dimension,
minecraft tags load/tick, pack.mcmeta.  Run:  python3 datapack_gen_core.py
"""
import json, os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
DP = os.path.join(ROOT, "datapack")
NS = os.path.join(DP, "data", "nahas")
FN = os.path.join(NS, "function")
F, LT, ADV = {}, {}, {}

# ---------------------------------------------------------------- helpers
def J(o):
    return json.dumps(o, ensure_ascii=False, separators=(",", ":"))

def T(text, color="white", **kw):
    d = {"text": text, "color": color}
    d.update(kw)
    return d

def CK(text, cmd, color="aqua", tip=None):
    d = {"text": text, "color": color,
         "clickEvent": {"action": "run_command", "value": cmd},
         "click_event": {"action": "run_command", "command": cmd}}
    if tip:
        d["hoverEvent"] = {"action": "show_text", "contents": T(tip, "gray")}
        d["hover_event"] = {"action": "show_text", "value": T(tip, "gray")}
    return d

def SC(name, obj, color="yellow"):
    return {"score": {"name": name, "objective": obj}, "color": color}

def comp(parts):
    out = [""]
    for p in parts:
        out.append(T(p) if isinstance(p, str) else p)
    return J(out)

def tw(sel, *parts):
    return "tellraw %s %s" % (sel, comp(parts))

def say(sel, text, color="yellow"):
    return "tellraw %s %s" % (sel, J(T(text, color)))

def title(sel, main, sub=None, color="gold", subcolor="yellow", times="10 70 20"):
    r = ["title %s times %s" % (sel, times)]
    if sub:
        r.append("title %s subtitle %s" % (sel, J(T(sub, subcolor))))
    r.append("title %s title %s" % (sel, J(T(main, color))))
    return r

def bar(sel, *parts):
    return "title %s actionbar %s" % (sel, comp(parts))

def flat(x):
    out = []
    for i in x:
        if isinstance(i, (list, tuple)):
            out.extend(flat(i))
        else:
            out.append(i)
    return out

def fn(name, *lines):
    lst = F.setdefault(name, [])
    for l in lines:
        if isinstance(l, (list, tuple)):
            lst.extend(l)
        else:
            lst.append(l)

def mob(ent, dx, dy, dz, tags, extra=""):
    t = ",".join('"%s"' % x for x in tags)
    return "summon %s ~%s ~%s ~%s {Tags:[%s],PersistenceRequired:1b%s}" % (ent, dx, dy, dz, t, extra)

def dmg(sel, n, kind="minecraft:magic"):
    return ["execute unless score #kids nh_g matches 1 as %s run damage @s %d %s" % (sel, n, kind),
            "execute if score #kids nh_g matches 1 as %s run damage @s %d %s" % (sel, max(1, n // 2), kind)]

DO, DS, DE = "minecraft:overworld", "nahas:star_sea", "nahas:ember"

# id: (dim, x, y, z, arabic name, discover radius)
POI = {
    "spawn": (DO, 300, 70, 2050, "معسكر القافلة المهجور", 70),
    "hub": (DO, 600, 70, 1650, "واحة الدلال", 70),
    "t1": (DO, 1000, 70, 1900, "معبد الواحة", 70),
    "t2": (DO, 1800, 70, 1850, "وادي العقارب", 70),
    "t3": (DO, 2100, 70, 1300, "المكتبة الغارقة", 70),
    "t4": (DO, 1700, 120, 450, "قلعة الريح", 70),
    "star": (DO, 1000, 70, 350, "بوابة النجوم", 60),
    "ember": (DO, 300, 70, 900, "بوابة الجمر", 60),
    "city": (DO, 1200, 70, 1200, "مدينة النحاس", 200),
    "starsea": (DS, 600, 100, 600, "بحر النجوم", 700),
    "embersea": (DE, 500, 64, 500, "أرض الجمر", 400),
}
GO = [  # nh_go value -> poi id
    (1, "spawn"), (2, "hub"), (3, "t1"), (4, "t2"), (5, "t3"), (6, "t4"), (7, "star"), (8, "ember"),
    (9, "city"), (10, "starsea"), (11, "embersea")]
TP_OFF = {"starsea": (0, 1, 5), "embersea": (0, 1, 5), "star": (0, 1, 6), "ember": (0, 1, 6)}  # arrival offset (portal at centre)
DISC_ADV = {"hub": "disc_hub", "t1": "disc_t1", "t2": "disc_t2", "t3": "disc_t3", "t4": "disc_t4",
            "star": "disc_star", "ember": "disc_ember", "city": "disc_city",
            "starsea": "star_sea", "embersea": "ember_realm"}

# ---------------------------------------------------------------- items
def lore(lines):
    return [{"text": l, "color": "gray", "italic": False} for l in lines]

ITEMS = {
    "lantern": dict(base="minecraft:lantern", name="فانوس الجني", color="gold",
                    lore=["فانوس مسحور يضيء ظلام الصحراء", "احمله في يدك ليكشف الأشباح القريبة"], glint=True),
    "scimitar": dict(base="minecraft:netherite_sword", name="سيف الجن", color="red",
                     lore=["سيف مصنوع من نار الجن", "يمنح حامله خفة في الحركة"], glint=True,
                     ench={"minecraft:sharpness": 5, "minecraft:fire_aspect": 1, "minecraft:sweeping_edge": 3,
                           "minecraft:unbreaking": 3}),
    "carpet": dict(base="minecraft:elytra", name="بساط الريح", color="light_purple",
                   lore=["البسه على صدرك ثم اقفز وحلّق", "يسرّع الطيران ويحميك من السقوط"], glint=True,
                   extra={"minecraft:unbreakable": {}}),
    "bottle": dict(base="minecraft:potion", name="قارورة الجني", color="aqua",
                   lore=["اشربها فتشعر بقوة الجني"], glint=True,
                   extra={"minecraft:potion_contents": {"custom_color": 5636095, "custom_effects": [
                       {"id": "minecraft:regeneration", "duration": 200, "amplifier": 1},
                       {"id": "minecraft:absorption", "duration": 1200, "amplifier": 1},
                       {"id": "minecraft:speed", "duration": 600, "amplifier": 0}]}}),
    "bow": dict(base="minecraft:bow", name="قوس الصحراء", color="yellow",
                lore=["قوس أهل القوافل القدماء"], glint=False,
                ench={"minecraft:power": 4, "minecraft:punch": 1, "minecraft:unbreaking": 3}),
    "dagger": dict(base="minecraft:golden_sword", name="خنجر الظل", color="dark_gray",
                   lore=["سريع وخفيف كالظل"], glint=False,
                   ench={"minecraft:sharpness": 3, "minecraft:knockback": 1, "minecraft:unbreaking": 2}),
    "amulet": dict(base="minecraft:totem_of_undying", name="تميمة الحماية", color="green",
                   lore=["احملها في يدك الثانية", "فتنقذك من الموت مرة واحدة"], glint=True),
    "key": dict(base="minecraft:tripwire_hook", name="مفتاح البوابة", color="gold",
                lore=["مفتاح مدينة النحاس القديم"], glint=True),
}
SEALN = ["الأول", "الثاني", "الثالث", "الرابع", "الخامس", "السادس", "السابع"]
for i in range(1, 8):
    ITEMS["seal_%d" % i] = dict(base="minecraft:copper_ingot", name="ختم النحاس %s" % SEALN[i - 1], color="gold",
                                lore=["واحد من سبعة أختام تفتح مدينة النحاس"], glint=True)
ASTRO_TARGETS = [  # index -> (dimension, x,y,z, name)
    (DO, 600, 70, 1650, "واحة الدلال"), (DO, 1000, 70, 1900, "معبد الواحة"), (DO, 1800, 70, 1850, "وادي العقارب"),
    (DO, 2100, 70, 1300, "المكتبة الغارقة"), (DO, 1700, 120, 450, "قلعة الريح"),
    (DO, 1000, 70, 350, "بوابة النجوم"), (DO, 300, 70, 900, "بوابة الجمر"), (DO, 1200, 70, 1200, "مدينة النحاس")]

def item_entry(key, count=None, extra_funcs=None):
    it = ITEMS[key]
    comps = {"minecraft:item_model": "nahas:" + key.split("#")[0],
             "minecraft:custom_name": {"text": it["name"], "color": it["color"], "italic": False},
             "minecraft:lore": lore(it["lore"]),
             "minecraft:custom_data": {"nh": key}}
    if it.get("glint"):
        comps["minecraft:enchantment_glint_override"] = True
    comps.update(it.get("extra", {}))
    funcs = [{"function": "minecraft:set_components", "components": comps}]
    if it.get("ench"):
        funcs.append({"function": "minecraft:set_enchantments", "enchantments": it["ench"]})
    return {"type": "minecraft:item", "name": it["base"], "functions": funcs}

def pool(entries, rolls=1, bonus=None):
    p = {"rolls": rolls, "entries": entries}
    if bonus is not None:
        p["bonus_rolls"] = bonus
    return p

def E(name, w=1, cnt=None, funcs=None):
    e = {"type": "minecraft:item", "name": "minecraft:" + name, "weight": w}
    fs = []
    if cnt is not None:
        c = cnt if isinstance(cnt, int) else {"type": "minecraft:uniform", "min": cnt[0], "max": cnt[1]}
        fs.append({"function": "minecraft:set_count", "count": c})
    if funcs:
        fs.extend(funcs)
    if fs:
        e["functions"] = fs
    return e

def REF(table, w=1):
    return {"type": "minecraft:loot_table", "value": "nahas:" + table, "weight": w}

def table(kind, pools):
    return {"type": kind, "pools": pools}

# item loot tables
for k in ITEMS:
    LT["items/" + k] = table("minecraft:generic", [pool([item_entry(k)])])
for i, (dim, x, y, z, nm) in enumerate(ASTRO_TARGETS):
    e = item_entry("astrolabe" if False else "lantern")  # placeholder replaced below
    comps = {"minecraft:item_model": "nahas:astrolabe",
             "minecraft:custom_name": {"text": "الإسطرلاب", "color": "aqua", "italic": False},
             "minecraft:lore": lore(["يشير إلى وجهتك التالية:", nm, "اكتب /trigger nh_map set 1 لتحديثه"]),
             "minecraft:custom_data": {"nh": "astrolabe"},
             "minecraft:enchantment_glint_override": True,
             "minecraft:lodestone_tracker": {"target": {"pos": [x, y, z], "dimension": dim}, "tracked": False}}
    LT["items/astrolabe_%d" % i] = table("minecraft:generic", [pool([{
        "type": "minecraft:item", "name": "minecraft:compass",
        "functions": [{"function": "minecraft:set_components", "components": comps}]}])])
LT["trial/page"] = table("minecraft:generic", [pool([{
    "type": "minecraft:item", "name": "minecraft:paper", "functions": [{"function": "minecraft:set_components", "components": {
        "minecraft:item_model": "nahas:page",
        "minecraft:custom_name": {"text": "صفحة مفقودة", "color": "yellow", "italic": False},
        "minecraft:lore": lore(["صفحة من كتب المكتبة الغارقة"]),
        "minecraft:custom_data": {"nh": "page"}, "minecraft:enchantment_glint_override": True}}]}])])

def potion(name, pot, cnt=1):
    return {"type": "minecraft:item", "name": "minecraft:potion", "functions": [
        {"function": "minecraft:set_count", "count": cnt},
        {"function": "minecraft:set_components", "components": {
            "minecraft:potion_contents": {"potion": pot},
            "minecraft:custom_name": {"text": name, "color": "aqua", "italic": False}}}]}

# chest tables
LT["chests/common"] = table("minecraft:chest", [
    pool([E("bread", 10, (2, 5)), E("cooked_mutton", 8, (1, 4)), E("torch", 8, (4, 12)), E("arrow", 8, (4, 12)),
          E("gold_nugget", 10, (3, 9)), E("stick", 6, (2, 6)), E("string", 5, (1, 4)), E("bone", 5, (1, 3)),
          E("coal", 5, (2, 6)), E("leather", 4, (1, 3)), REF("items/dagger", 1)], rolls={"type": "minecraft:uniform", "min": 3, "max": 5})])
LT["chests/rare"] = table("minecraft:chest", [
    pool([E("gold_ingot", 10, (2, 5)), E("iron_ingot", 8, (2, 6)), E("emerald", 6, (1, 3)), E("arrow", 6, (8, 16)),
          E("experience_bottle", 6, (2, 5)), potion("جرعة شفاء", "minecraft:healing", 1) | {"weight": 4},
          REF("items/dagger", 2), REF("items/bow", 2), REF("items/bottle", 1), E("golden_apple", 2, 1)],
         rolls={"type": "minecraft:uniform", "min": 3, "max": 5})])
LT["chests/epic"] = table("minecraft:chest", [
    pool([E("diamond", 8, (1, 3)), E("emerald", 8, (2, 5)), E("gold_ingot", 10, (4, 9)), E("golden_apple", 5, (1, 2)),
          E("experience_bottle", 6, (4, 9)), REF("items/amulet", 3), REF("items/bow", 3), REF("items/bottle", 3),
          REF("items/scimitar", 1), REF("items/carpet", 1), E("netherite_scrap", 1, 1)],
         rolls={"type": "minecraft:uniform", "min": 4, "max": 6})])
LT["chests/ruins"] = table("minecraft:chest", [
    pool([E("gold_nugget", 10, (4, 12)), E("brick", 6, (2, 6)), E("clay_ball", 5, (2, 6)), E("bone", 6, (2, 5)),
          E("rotten_flesh", 4, (1, 4)), E("gold_ingot", 4, (1, 3)), E("emerald", 3, (1, 2)),
          E("amethyst_shard", 4, (1, 4)), E("torch", 6, (3, 8)), REF("items/dagger", 2), REF("items/bow", 1)],
         rolls={"type": "minecraft:uniform", "min": 3, "max": 5})])
LT["chests/library"] = table("minecraft:chest", [
    pool([E("book", 10, (1, 3)), E("paper", 10, (3, 8)), E("ink_sac", 6, (1, 3)), E("feather", 5, (1, 3)),
          E("lapis_lazuli", 6, (2, 7)), E("glow_ink_sac", 3, (1, 2)),
          E("book", 6, 1, [{"function": "minecraft:enchant_with_levels", "levels": {"type": "minecraft:uniform", "min": 8, "max": 20}}]),
          REF("items/bottle", 2), E("experience_bottle", 4, (2, 6))], rolls={"type": "minecraft:uniform", "min": 3, "max": 5})])
LT["chests/oasis"] = table("minecraft:chest", [
    pool([E("melon_slice", 8, (3, 8)), E("sweet_berries", 8, (3, 8)), E("apple", 8, (1, 4)), E("bread", 8, (2, 5)),
          E("cooked_cod", 6, (1, 4)), E("cooked_salmon", 6, (1, 4)), E("honey_bottle", 5, (1, 2)),
          E("dried_kelp", 6, (3, 8)), E("gold_nugget", 5, (2, 6)), E("golden_carrot", 3, (1, 3))],
         rolls={"type": "minecraft:uniform", "min": 3, "max": 5})])
LT["chests/camp"] = table("minecraft:chest", [
    pool([E("cooked_beef", 8, (1, 4)), E("leather", 6, (1, 4)), E("rotten_flesh", 5, (1, 4)), E("torch", 8, (3, 9)),
          E("arrow", 8, (4, 12)), E("iron_nugget", 6, (3, 8)), E("bone", 4, (1, 3)), E("string", 5, (1, 4)),
          E("bread", 8, (2, 5)), REF("items/dagger", 1)], rolls={"type": "minecraft:uniform", "min": 3, "max": 4})])
LT["chests/tomb"] = table("minecraft:chest", [
    pool([E("bone", 8, (2, 6)), E("gold_ingot", 8, (2, 5)), E("gold_nugget", 8, (4, 10)), E("emerald", 5, (1, 3)),
          E("rotten_flesh", 4, (1, 4)), E("golden_sword", 2, 1), E("golden_helmet", 2, 1), E("diamond", 2, 1),
          REF("items/amulet", 2), REF("items/dagger", 2), REF("items/bottle", 1)],
         rolls={"type": "minecraft:uniform", "min": 3, "max": 5})])
LT["chests/city"] = table("minecraft:chest", [
    pool([E("gold_block", 3, (1, 2)), E("copper_ingot", 10, (4, 10)), E("raw_copper", 6, (3, 8)),
          E("diamond", 5, (1, 3)), E("emerald", 6, (2, 5)), E("golden_apple", 4, (1, 2)), E("copper_block", 3, (1, 3)),
          REF("items/scimitar", 1), REF("items/carpet", 1), REF("items/bottle", 2), REF("items/amulet", 2)],
         rolls={"type": "minecraft:uniform", "min": 4, "max": 6})])
LT["chests/boss"] = table("minecraft:chest", [
    pool([E("gold_ingot", 1, (6, 12))]), pool([E("diamond", 1, (2, 4))]), pool([E("emerald", 1, (4, 8))]),
    pool([E("golden_apple", 1, 2)]), pool([E("experience_bottle", 1, (8, 16))]),
    pool([REF("items/scimitar", 2), REF("items/bow", 3), REF("items/amulet", 3), REF("items/bottle", 3),
          REF("items/dagger", 3)])])
LT["gift/traveler"] = table("minecraft:gift", [
    pool([E("bread", 1, (3, 5)), E("cooked_mutton", 1, (2, 4))], rolls=1),
    pool([E("gold_nugget", 1, (5, 12))]), pool([E("torch", 1, (6, 12))])])
LT["gift/seal_reward"] = table("minecraft:gift", [
    pool([E("gold_ingot", 1, (3, 6))]), pool([E("emerald", 1, (2, 4))]), pool([E("experience_bottle", 1, (8, 14))]),
    pool([E("golden_apple", 1, 1)]), pool([E("cooked_beef", 1, (8, 12))])])
LT["gift/final_reward"] = table("minecraft:gift", [
    pool([E("netherite_ingot", 1, 1)]), pool([E("totem_of_undying", 1, 1)]), pool([E("enchanted_golden_apple", 1, 2)]),
    pool([E("gold_block", 1, (3, 5))]), pool([E("diamond", 1, (5, 8))]), pool([REF("items/amulet", 1)])])
LT["kit/start"] = table("minecraft:gift", [
    pool([REF("items/lantern")]), pool([REF("items/astrolabe_0")]), pool([E("bread", 1, 8)]),
    pool([E("cooked_mutton", 1, 6)]), pool([E("stone_sword", 1, 1)]), pool([E("torch", 1, 8)]),
    pool([potion("قربة ماء", "minecraft:water", 2)])])
SHOP = {  # id: (name, price, table entries)
    1: ("خبز وتمر", 10, [E("bread", 1, 8), E("cooked_mutton", 1, 4)]),
    2: ("سهام ×٣٢", 15, [E("arrow", 1, 32)]),
    3: ("جرعة شفاء", 25, [potion("جرعة شفاء", "minecraft:healing", 1)]),
    4: ("مشاعل ×١٦", 20, [E("torch", 1, 16)]),
    5: ("خنجر الظل", 60, [REF("items/dagger")]),
    6: ("قوس الصحراء", 90, [REF("items/bow")]),
    7: ("تميمة الحماية", 120, [REF("items/amulet")]),
    8: ("قارورة الجني", 80, [REF("items/bottle")]),
    9: ("بساط الريح", 300, [REF("items/carpet")]),
    10: ("سيف الجن", 200, [REF("items/scimitar")]),
    11: ("فانوس جديد", 5, [REF("items/lantern")]),
    12: ("إسطرلاب جديد", 15, [REF("items/astrolabe_0")]),
}
SHOPKEY = {1: "food", 2: "arrows", 3: "heal", 4: "torches", 5: "dagger", 6: "bow", 7: "amulet", 8: "bottle",
           9: "carpet", 10: "scimitar", 11: "lantern", 12: "astrolabe"}
for i, (nm, pr, ents) in SHOP.items():
    LT["shop/" + SHOPKEY[i]] = table("minecraft:generic", [pool([e for e in ents]) if len(ents) == 1 else
                                                          {"rolls": 1, "entries": [{"type": "minecraft:group", "children": ents}]}])

# ---------------------------------------------------------------- advancements
ADVS = [  # id, parent, icon, title, desc, frame
    ("root", None, "copper_ingot", "مدينة النحاس", "بدأت رحلتك في الصحراء الغامضة", "task"),
    ("lantern", "root", "lantern", "فانوس الجني", "احصل على فانوسك المسحور", "task"),
    ("role", "lantern", "iron_sword", "اختر دورك", "اختر دورك في القافلة", "task"),
    ("disc_hub", "role", "campfire", "واحة الدلال", "اكتشف الواحة والسوق", "task"),
    ("disc_t1", "disc_hub", "sandstone", "معبد الواحة", "وصلت إلى المعبد الأول", "task"),
    ("disc_t2", "disc_hub", "red_sand", "وادي العقارب", "وصلت إلى الوادي الأحمر", "task"),
    ("disc_t3", "disc_hub", "bookshelf", "المكتبة الغارقة", "وصلت إلى المكتبة وسط البحيرة", "task"),
    ("disc_t4", "disc_hub", "blackstone", "قلعة الريح", "صعدت إلى قلعة الريح", "task"),
    ("disc_star", "disc_hub", "end_rod", "بوابة النجوم", "وجدت بوابة بحر النجوم", "task"),
    ("disc_ember", "disc_hub", "magma_block", "بوابة الجمر", "وجدت بوابة أرض الجمر", "task"),
    ("disc_city", "disc_hub", "gold_block", "أمام المدينة", "رأيت أسوار مدينة النحاس", "goal"),
    ("portal", "disc_star", "ender_pearl", "عبور البوابة", "اعبر بوابة إلى عالم آخر", "task"),
    ("star_sea", "portal", "amethyst_shard", "بحر النجوم", "وصلت إلى جزر النجوم العائمة", "task"),
    ("ember_realm", "portal", "blaze_powder", "أرض الجمر", "وصلت إلى أرض الجمر", "task"),
    ("seal_1", "disc_t1", "copper_ingot", "الختم الأول", "اهزم حراس المعبد", "goal"),
    ("seal_2", "disc_t2", "copper_ingot", "الختم الثاني", "اهزم ملكة العقارب", "goal"),
    ("seal_3", "disc_t3", "copper_ingot", "الختم الثالث", "أعد صفحات المكتبة الغارقة", "goal"),
    ("seal_4", "disc_t4", "copper_ingot", "الختم الرابع", "اهزم قائد الرياح", "goal"),
    ("seal_5", "star_sea", "copper_ingot", "الختم الخامس", "اهزم ملكة النجوم", "goal"),
    ("seal_6", "ember_realm", "copper_ingot", "الختم السادس", "اهزم عملاق الجمر", "goal"),
    ("seals_3", "root", "gold_ingot", "ثلاثة أختام", "اجمع ثلاثة أختام", "goal"),
    ("city_open", "disc_city", "tripwire_hook", "انفتحت البوابة", "ستة أختام تفتح بوابة المدينة", "goal"),
    ("seal_7", "city_open", "copper_block", "الختم السابع", "الختم الأخير للنحاس", "challenge"),
    ("final", "seal_7", "nether_star", "حارس المدينة", "هزمتم الحارس النحاسي وأيقظتم المدينة", "challenge"),
    ("shop", "disc_hub", "emerald", "أول صفقة", "اشترِ شيئاً من السوق", "task"),
    ("quest", "disc_hub", "writable_book", "باحث عن المهام", "أكمل مهمة جانبية", "task"),
    ("rich", "shop", "gold_block", "تاجر القافلة", "اجمع خمسمائة قطعة ذهب", "goal"),
    ("carpet", "shop", "elytra", "بساط الريح", "احصل على بساط الريح", "goal"),
    ("kids", "root", "cake", "رحلة عائلية", "فعّل وضع الأطفال ليكون اللعب أسهل", "task"),
]
for aid, parent, icon, ti, de, frame in ADVS:
    d = {"display": {"icon": {"id": "minecraft:" + icon}, "title": T(ti, "gold"), "description": T(de, "gray"),
                     "frame": frame, "show_toast": True, "announce_to_chat": True, "hidden": False},
         "criteria": {"done": {"trigger": "minecraft:impossible"}}}
    if parent:
        d["parent"] = "nahas:" + parent
    else:
        d["display"]["background"] = "minecraft:textures/gui/advancements/backgrounds/adventure.png"
        d["display"]["announce_to_chat"] = False
    ADV[aid] = d

def grant(sel, a):
    return "advancement grant %s only nahas:%s" % (sel, a)

# ---------------------------------------------------------------- core: load
OBJ = [("nh_g", "الحالة"), ("nh_gold", "الذهب"), ("nh_prole", None), ("nh_cd", None), ("nh_cd2", None),
       ("nh_gocd", None), ("nh_pcd", None), ("nh_tmp", None), ("nh_lastk", None), ("nh_lastseal", None),
       ("nh_askf", None), ("nh_disc", None)]
TRIG = ["nh_role", "nh_go", "nh_shop", "nh_quest", "nh_power", "nh_map", "nh_help", "nh_ask", "nh_start"]
load = []
for o, dn in OBJ:
    load.append("scoreboard objectives add %s dummy%s" % (o, (" " + J(T(dn))) if dn else ""))
load.append("scoreboard objectives add nh_kills totalKillCount")
load.append("scoreboard objectives add nh_dead deathCount")
for t in TRIG:
    load.append("scoreboard objectives add %s trigger" % t)
load += ["scoreboard objectives setdisplay list nh_gold",
         "scoreboard players set #2 nh_g 2", "scoreboard players set #10 nh_g 10",
         "scoreboard players set #100 nh_g 100",
         "function nahas:core/gamerules",
         "execute unless score #init nh_g matches 1 run function nahas:core/first_load",
         "scoreboard players set #loaded nh_g 1"]
fn("core/load", load)
fl = ["scoreboard players set #init nh_g 1"]
for k in ["seals", "kids", "trial", "phase", "boss", "city", "gate", "started", "next", "sn", "ok"]:
    fl.append("scoreboard players set #%s nh_g 0" % k)
for i in range(1, 8):
    fl.append("scoreboard players set #t%d nh_g 0" % i)
    fl.append("scoreboard players set #s%d nh_g 0" % i)
for b in range(1, 6):
    fl += ["scoreboard players set #b%d_ph nh_g 0" % b, "scoreboard players set #b%d_t nh_g 0" % b,
           "scoreboard players set #b%d_miss nh_g 0" % b, "scoreboard players set #bmax%d nh_g 100" % b,
           "bossbar add nahas:boss%d %s" % (b, J(T("زعيم")))]
fl += ["difficulty normal", "setworldspawn 300 71 2050"]
fn("core/first_load", fl)

# gamerules: one command per tiny macro function (old camelCase + new snake_case)
GR = [("mobGriefing", "mob_griefing", "false"), ("keepInventory", "keep_inventory", "true"),
      ("doInsomnia", "spawn_phantoms", "false"), ("doPatrolSpawning", "spawn_patrols", "false"),
      ("doTraderSpawning", "spawn_wandering_traders", "false"), ("doWardenSpawning", "spawn_wardens", "false"),
      ("playersSleepingPercentage", "players_sleeping_percentage", "1")]
g = []
for old, new, v in GR:
    n = old.lower()
    fn("core/gr/%s_old" % n, "$gamerule %s $(v)" % old)
    fn("core/gr/%s_new" % n, "$gamerule %s $(v)" % new)
    g += ["function nahas:core/gr/%s_old {v:\"%s\"}" % (n, v), "function nahas:core/gr/%s_new {v:\"%s\"}" % (n, v)]
fn("core/gamerules", g)

# ---------------------------------------------------------------- core: tick / second
fn("core/tick",
   "function nahas:core/triggers",
   "function nahas:portal/tick",
   "function nahas:items/tick",
   "scoreboard players add #tk nh_g 1",
   "execute if score #tk nh_g matches 20.. run function nahas:core/second",
   "function nahas:hook/tick")
trg = []
for t in TRIG:
    if t == "nh_role":
        trg.append("execute as @a[scores={nh_role=1..}] unless score @s nh_role = @s nh_prole at @s run function nahas:role/trigger")
        trg.append("execute as @a[scores={nh_role=0}] if score @s nh_prole matches 1.. run scoreboard players operation @s nh_role = @s nh_prole")
        trg.append("execute as @a[scores={nh_role=..-1}] run function nahas:role/menu")
        continue
    trg.append("execute as @a[scores={%s=1..}] at @s run function nahas:%s" % (t, {
        "nh_go": "portal/go", "nh_shop": "shop/trigger", "nh_quest": "quest/trigger", "nh_power": "role/power",
        "nh_map": "items/map", "nh_help": "core/help", "nh_ask": "core/ask", "nh_start": "core/start"}[t]))
    trg.append("scoreboard players set @a[scores={%s=..-1}] %s 0" % (t, t))
fn("core/triggers", trg)

sec = ["scoreboard players set #tk nh_g 0"]
for t in TRIG:
    sec.append("scoreboard players enable @a %s" % t)
for o in ["nh_gold", "nh_cd", "nh_cd2", "nh_gocd", "nh_pcd", "nh_prole", "nh_kills", "nh_lastk", "nh_disc", "nh_dead", "nh_askf"]:
    sec.append("scoreboard players add @a %s 0" % o)
sec += ["execute as @a[tag=!nh_seen] at @s run function nahas:core/first_join",
        "execute as @a at @s run function nahas:core/player_second",
        "execute as @a[scores={nh_dead=1..}] at @s run function nahas:core/died",
        "function nahas:core/world_second",
        "function nahas:trial/second",
        "function nahas:boss/second",
        "function nahas:ambient/second",
        "function nahas:npc/second"]
fn("core/second", sec)

ps = [
    # gold from kills
    "scoreboard players operation @s nh_tmp = @s nh_kills",
    "scoreboard players operation @s nh_tmp -= @s nh_lastk",
    "scoreboard players operation @s nh_lastk = @s nh_kills",
    "execute if score @s nh_tmp matches 1.. run function nahas:core/gold_kills",
    "execute if score @s nh_cd matches 1.. run scoreboard players remove @s nh_cd 1",
    "execute if score @s nh_cd2 matches 1.. run scoreboard players remove @s nh_cd2 1",
    "execute if score @s nh_gocd matches 1.. run scoreboard players remove @s nh_gocd 1",
    "execute if score @s nh_pcd matches 1.. run scoreboard players remove @s nh_pcd 1",
    "function nahas:core/seal_sync",
    "function nahas:role/second",
    "function nahas:items/second",
    "execute if score #kids nh_g matches 1 run effect give @s minecraft:resistance 3 0 true",
    "execute if score @s nh_gold matches 500.. run " + grant("@s", "rich"),
]
fn("core/player_second", ps)
fn("core/gold_kills",
   "scoreboard players operation @s nh_tmp *= #2 nh_g",
   "scoreboard players operation @s nh_gold += @s nh_tmp",
   bar("@s", T("+", "gold"), SC("@s", "nh_tmp", "gold"), T(" ذهب", "gold")))
fn("core/died",
   "scoreboard players set @s nh_dead 0",
   say("@s", "لا تخف، الجني يعيدك إلى الحياة. حاول مرة أخرى!", "yellow"),
   "function nahas:hook/player_death")

# first join / start
fn("core/first_join",
   "tag @s add nh_seen",
   "scoreboard players set @s nh_gold 20",
   "scoreboard players set @s nh_prole 0",
   "scoreboard players set @s nh_lastk 0",
   "loot give @s loot nahas:kit/start",
   grant("@s", "root"), grant("@s", "lantern"),
   "spawnpoint @s 300 71 2050",
   "scoreboard players set #started nh_g 1",
   title("@s", "مدينة النحاس", "ليلة الفانوس"),
   say("@s", "أهلاً بك أيها المسافر! معك فانوس الجني. اكتب /trigger nh_help set 1 لتعرف الأوامر.", "yellow"),
   "function nahas:role/menu",
   "function nahas:hook/first_join")
fn("core/start",
   "scoreboard players set @s nh_start 0",
   "execute unless entity @s[tag=nh_seen] run function nahas:core/first_join",
   "execute if entity @s[tag=nh_seen] run function nahas:hook/first_join")

# ask
fn("core/ask",
   "scoreboard players operation @s nh_askf = @s nh_ask",
   "tag @s add nh_asking",
   "scoreboard players set @s nh_ask 0",
   say("@s", "وصل سؤالك إلى الجني... انتظر الجواب.", "aqua"))

# help / kids
hm = [tw("@s", T("=== المساعدة ===", "gold")),
      tw("@s", CK("[١] القائمة", "/trigger nh_help set 1"), " ", CK("[٢] وضع الأطفال: تشغيل", "/trigger nh_help set 2", "green"),
         " ", CK("[٣] إيقاف", "/trigger nh_help set 3", "red")),
      tw("@s", CK("[٤] شرح الأوامر", "/trigger nh_help set 4"), " ", CK("[٥] هدفي الآن", "/trigger nh_help set 5"),
         " ", CK("[٦] فانوس وإسطرلاب جديدان", "/trigger nh_help set 6")),
      tw("@s", CK("[٧] إنقاذ: عد إلى الواحة", "/trigger nh_help set 7", "yellow"))]
fn("core/help_menu", hm)
fn("core/help",
   "scoreboard players operation @s nh_tmp = @s nh_help",
   "scoreboard players set @s nh_help 0",
   "execute if score @s nh_tmp matches 2 run function nahas:core/kids_on",
   "execute if score @s nh_tmp matches 3 run function nahas:core/kids_off",
   "execute if score @s nh_tmp matches 4 run function nahas:core/help_cmds",
   "execute if score @s nh_tmp matches 5 run function nahas:quest/main",
   "execute if score @s nh_tmp matches 6 run function nahas:core/help_kit",
   "execute if score @s nh_tmp matches 7 run function nahas:core/help_unstuck",
   "execute if score @s nh_tmp matches 8 if entity @s[tag=nh_admin] run function nahas:selftest",
   "execute unless score @s nh_tmp matches 2..8 run function nahas:core/help_menu")
fn("core/kids_on",
   "scoreboard players set #kids nh_g 1", "difficulty easy",
   tw("@a", T("وضع الأطفال مفعّل: الزعماء أضعف واللعب أسهل.", "green")), grant("@s", "kids"))
fn("core/kids_off",
   "scoreboard players set #kids nh_g 0", "difficulty normal",
   tw("@a", T("وضع الأطفال متوقف.", "yellow")))
fn("core/help_cmds",
   say("@s", "/trigger nh_role  : اختيار الدور", "aqua"), say("@s", "/trigger nh_power : قوة الدور (١) ووميض الفانوس (٢)", "aqua"),
   say("@s", "/trigger nh_go    : السفر إلى الأماكن المكتشفة", "aqua"), say("@s", "/trigger nh_shop  : السوق", "aqua"),
   say("@s", "/trigger nh_quest : المهام", "aqua"), say("@s", "/trigger nh_map   : الإسطرلاب والخريطة", "aqua"),
   say("@s", "/trigger nh_ask   : اسأل الجني للمساعدة", "aqua"), say("@s", "/trigger nh_start : إعادة القصة", "aqua"))
fn("core/help_kit",
   "execute unless items entity @s hotbar.* minecraft:lantern[minecraft:custom_data={nh:\"lantern\"}] unless items entity @s inventory.* minecraft:lantern[minecraft:custom_data={nh:\"lantern\"}] run loot give @s loot nahas:items/lantern",
   "function nahas:items/astro_update")
fn("core/help_unstuck",
   "execute in minecraft:overworld run tp @s 600 71 1650",
   say("@s", "عدت إلى واحة الدلال.", "yellow"))

# discovery
disc = []
for pid, (dim, x, y, z, nm, r) in POI.items():
    disc.append("execute in %s positioned %d %d %d as @a[distance=..%d,tag=!nh_d_%s] at @s run function nahas:core/found_%s" % (dim, x, y, z, r, pid, pid))
    body = ["tag @s add nh_d_%s" % pid, "scoreboard players add @s nh_disc 1", "scoreboard players add @s nh_gold 15",
            title("@s", nm, "اكتشفت مكاناً جديداً", "yellow", "gray", "10 50 20"),
            "playsound minecraft:entity.experience_orb.pickup master @s ~ ~ ~ 1 1"]
    if pid in DISC_ADV:
        body.append(grant("@s", DISC_ADV[pid]))
    fn("core/found_" + pid, body)
fn("core/discover", disc)

fn("core/world_second",
   "function nahas:core/discover",
   "execute if score #city nh_g matches 1 unless score #gate nh_g matches 1 in minecraft:overworld positioned 1200 70 1350 if entity @a[distance=..80] run function nahas:core/gate_open",
   "execute in nahas:ember positioned 500 64 500 run effect give @a[distance=..3000] minecraft:fire_resistance 15 0 true",
   "execute in nahas:ember as @a at @s if block ~ ~ ~ minecraft:lava run function nahas:portal/rescue_ember",
   "execute in nahas:star_sea as @a[y=-200,dy=220] run function nahas:portal/rescue_star")

# seals
sy = []
for n in range(1, 8):
    sy.append("execute if score #s%d nh_g matches 1 unless entity @s[tag=nh_got%d] run function nahas:core/give_seal_%d" % (n, n, n))
    gs = ["tag @s add nh_got%d" % n, "scoreboard players set @s nh_lastseal %d" % n,
          "loot give @s loot nahas:items/seal_%d" % n]
    if n < 7:
        gs.append("loot give @s loot nahas:gift/seal_reward")
    gs += [grant("@s", "seal_%d" % n),
           title("@s", "ختم النحاس %s" % SEALN[n - 1], "%d من ٧" % n),
           "playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1",
           "particle minecraft:happy_villager ~ ~1 ~ 1 1 1 0 30",
           "function nahas:hook/seal_gained"]
    fn("core/give_seal_%d" % n, gs)
fn("core/seal_sync", sy)
rc = ["scoreboard players set #seals nh_g 0"]
for n in range(1, 8):
    rc.append("execute if score #s%d nh_g matches 1 run scoreboard players add #seals nh_g 1" % n)
rc += ["execute if score #seals nh_g matches 3.. run " + grant("@a", "seals_3"),
       "execute if score #seals nh_g matches 6.. unless score #city nh_g matches 1 run function nahas:core/city_open"]
fn("core/seal_recount", rc)
fn("core/city_open",
   "scoreboard players set #city nh_g 1",
   title("@a", "انفتحت بوابة المدينة!", "اذهبوا إلى البوابة الجنوبية", "gold", "yellow", "10 80 30"),
   tw("@a", T("ستة أختام اجتمعت! بوابة مدينة النحاس الجنوبية انفتحت. اذهبوا إلى القصر وواجهوا الحارس.", "gold")),
   "execute as @a run loot give @s loot nahas:items/key",
   grant("@a", "city_open"),
   "forceload add 1200 1350",
   "schedule function nahas:core/gate_force 60t",
   "execute as @a at @s run function nahas:hook/city_open")
fn("core/gate_force",
   "execute in minecraft:overworld store success score #gate nh_g run fill 1188 71 1346 1212 90 1354 minecraft:air replace minecraft:barrier",
   "forceload remove 1200 1350")
fn("core/gate_open",
   "execute store success score #gate nh_g run fill 1188 71 1346 1212 90 1354 minecraft:air replace minecraft:barrier",
   "playsound minecraft:block.iron_door.open master @a[distance=..80] ~ ~ ~ 2 0.5")

# next target for astrolabe (as player)
nx = ["scoreboard players set #next nh_g 7"]
for i in (6, 5, 4, 3, 2, 1):
    nx.append("execute unless score #t%d nh_g matches 9 run scoreboard players set #next nh_g %d" % (i, i))
nx.append("execute unless entity @s[tag=nh_d_hub] run scoreboard players set #next nh_g 0")
fn("core/next", nx)

# ---------------------------------------------------------------- roles
ROLES = {1: ("المستكشف", "green"), 2: ("الفارس", "red"), 3: ("الحكيم", "aqua"), 4: ("الظل", "dark_purple")}
fn("role/menu",
   tw("@s", T("=== اختر دورك ===", "gold")),
   tw("@s", CK("[١] المستكشف", "/trigger nh_role set 1", "green", "سريع. قوته: نداء يكشف الوحوش"),
      T(" سريع، ونداؤه يكشف الوحوش", "gray")),
   tw("@s", CK("[٢] الفارس", "/trigger nh_role set 2", "red", "قوي ومتين. قوته: صرخة القوة"),
      T(" متين، وصرخته تقوّي الفريق", "gray")),
   tw("@s", CK("[٣] الحكيم", "/trigger nh_role set 3", "aqua", "يشفي الجميع"),
      T(" حظه جيد، وبركته تشفي الفريق", "gray")),
   tw("@s", CK("[٤] الظل", "/trigger nh_role set 4", "dark_purple", "يختفي وينتقل"),
      T(" يرى في الظلام، ويختفي وينتقل", "gray")),
   "execute if score @s nh_prole matches 1.. run scoreboard players operation @s nh_role = @s nh_prole",
   "execute unless score @s nh_prole matches 1.. run scoreboard players set @s nh_role 0")
fn("role/trigger",
   "execute if score @s nh_role matches 1..4 run function nahas:role/set",
   "execute unless score @s nh_role matches 1..4 run function nahas:role/menu")
rs = ["tag @s remove role_1", "tag @s remove role_2", "tag @s remove role_3", "tag @s remove role_4",
      "scoreboard players operation @s nh_prole = @s nh_role"]
for n, (nm, c) in ROLES.items():
    rs.append("execute if score @s nh_role matches %d run tag @s add role_%d" % (n, n))
    rs.append("execute if score @s nh_role matches %d run %s" % (n, tw("@s", T("دورك الآن: ", "yellow"), T(nm, c, bold=True),
                                                                    T("  (اكتب /trigger nh_power set 1 لاستخدام قوتك)", "gray"))))
rs += [grant("@s", "role"), "playsound minecraft:block.enchantment_table.use master @s ~ ~ ~ 1 1.2",
       "particle minecraft:enchant ~ ~1 ~ 0.5 0.8 0.5 0.3 40"]
fn("role/set", rs)
fn("role/second",
   "execute if entity @s[tag=role_1] run effect give @s minecraft:speed 3 0 true",
   "execute if entity @s[tag=role_2] run effect give @s minecraft:resistance 3 0 true",
   "execute if entity @s[tag=role_3] run effect give @s minecraft:luck 3 1 true",
   "execute if entity @s[tag=role_3] run effect give @s minecraft:saturation 1 0 true",
   "execute if entity @s[tag=role_4] run effect give @s minecraft:night_vision 15 0 true")
fn("role/power",
   "scoreboard players operation @s nh_tmp = @s nh_power",
   "scoreboard players set @s nh_power 0",
   "execute if score @s nh_tmp matches 2 run function nahas:role/flare",
   "execute unless score @s nh_tmp matches 2 run function nahas:role/active")
fn("role/active",
   "execute unless score @s nh_prole matches 1..4 run " + say("@s", "اختر دورك أولاً: /trigger nh_role set 1", "red"),
   "execute if score @s nh_prole matches 1..4 if score @s nh_cd matches 1.. run " +
   tw("@s", T("قوتك تحتاج إلى راحة: ", "red"), SC("@s", "nh_cd", "yellow"), T(" ثانية", "red")),
   "execute if score @s nh_prole matches 1..4 if score @s nh_cd matches ..0 run function nahas:role/fire")
fn("role/fire",
   "execute if score @s nh_prole matches 1 run function nahas:role/p1",
   "execute if score @s nh_prole matches 2 run function nahas:role/p2",
   "execute if score @s nh_prole matches 3 run function nahas:role/p3",
   "execute if score @s nh_prole matches 4 run function nahas:role/p4",
   "execute if score @s nh_prole matches 1 run scoreboard players set @s nh_cd 30",
   "execute if score @s nh_prole matches 2 run scoreboard players set @s nh_cd 45",
   "execute if score @s nh_prole matches 3 run scoreboard players set @s nh_cd 40",
   "execute if score @s nh_prole matches 4 run scoreboard players set @s nh_cd 30",
   "execute if score #kids nh_g matches 1 run scoreboard players operation @s nh_cd /= #2 nh_g")
fn("role/p1",
   say("@s", "نداء الاستكشاف! الوحوش القريبة تتوهج الآن.", "green"),
   "effect give @e[distance=..60,type=!minecraft:player] minecraft:glowing 15 0 true",
   "effect give @s minecraft:speed 10 2 true", "effect give @s minecraft:jump_boost 10 1 true",
   "particle minecraft:happy_villager ~ ~1 ~ 1 1 1 0 40",
   "playsound minecraft:entity.evoker.prepare_summon master @a[distance=..20] ~ ~ ~ 1 1.3",
   "function nahas:items/astro_update")
fn("role/p2",
   say("@s", "صرخة الفارس! أنت وأصدقاؤك أقوى الآن.", "red"),
   "effect give @a[distance=..14] minecraft:strength 15 1 true", "effect give @a[distance=..14] minecraft:resistance 15 1 true",
   "particle minecraft:angry_villager ~ ~1.5 ~ 1 0.5 1 0 25",
   "playsound minecraft:entity.ravager.roar master @a[distance=..30] ~ ~ ~ 1 1.2")
fn("role/p3",
   say("@s", "بركة الحكيم! الشفاء للجميع.", "aqua"),
   "effect give @a[distance=..14] minecraft:instant_health 1 1 true", "effect give @a[distance=..14] minecraft:regeneration 8 1 true",
   "effect clear @a[distance=..14] minecraft:poison", "effect clear @a[distance=..14] minecraft:weakness",
   "effect clear @a[distance=..14] minecraft:slowness", "effect clear @a[distance=..14] minecraft:blindness",
   "effect clear @a[distance=..14] minecraft:nausea", "effect clear @a[distance=..14] minecraft:wither",
   "particle minecraft:heart ~ ~1.5 ~ 2 0.5 2 0 25",
   "playsound minecraft:block.beacon.power_select master @a[distance=..20] ~ ~ ~ 1 1.5")
fn("role/p4",
   say("@s", "خطوة الظل! اختفيت وانتقلت.", "dark_purple"),
   "effect give @s minecraft:invisibility 8 0 true", "effect give @s minecraft:speed 8 2 true",
   "particle minecraft:large_smoke ~ ~1 ~ 0.4 0.6 0.4 0.02 30",
   "execute positioned ^ ^ ^8 if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run tp @s ~ ~ ~",
   "particle minecraft:large_smoke ~ ~1 ~ 0.4 0.6 0.4 0.02 30",
   "playsound minecraft:entity.enderman.teleport master @a[distance=..20] ~ ~ ~ 1 1")
fn("role/flare",
   "execute unless items entity @s hotbar.* minecraft:lantern[minecraft:custom_data={nh:\"lantern\"}] unless items entity @s weapon.offhand minecraft:lantern[minecraft:custom_data={nh:\"lantern\"}] run " +
   say("@s", "تحتاج إلى فانوس الجني في شريط الأدوات.", "red"),
   "execute if score @s nh_cd2 matches 1.. run " + tw("@s", T("الفانوس يحتاج إلى راحة: ", "red"), SC("@s", "nh_cd2", "yellow"), T(" ثانية", "red")),
   "execute if score @s nh_cd2 matches ..0 if items entity @s hotbar.* minecraft:lantern[minecraft:custom_data={nh:\"lantern\"}] run function nahas:role/flare_do",
   "execute if score @s nh_cd2 matches ..0 unless items entity @s hotbar.* minecraft:lantern[minecraft:custom_data={nh:\"lantern\"}] if items entity @s weapon.offhand minecraft:lantern[minecraft:custom_data={nh:\"lantern\"}] run function nahas:role/flare_do")
fn("role/flare_do",
   "scoreboard players set @s nh_cd2 60",
   say("@s", "وميض الفانوس! الأشباح تضعف.", "gold"),
   "effect give @e[distance=..15,type=#minecraft:undead] minecraft:weakness 10 1 true",
   "effect give @e[distance=..15,type=#minecraft:undead] minecraft:glowing 10 0 true",
   "effect give @a[distance=..12] minecraft:regeneration 5 0 true",
   "particle minecraft:flash ~ ~1 ~ 0 0 0 0 1", "particle minecraft:end_rod ~ ~1 ~ 3 1 3 0.05 60",
   "playsound minecraft:block.beacon.activate master @a[distance=..20] ~ ~ ~ 1 1.5")

# ---------------------------------------------------------------- items
cnbt = lambda k: "minecraft:custom_data={nh:\"%s\"}" % k
fn("items/second",
   "execute if items entity @s weapon.* minecraft:lantern[%s] run function nahas:items/lantern_aura" % cnbt("lantern"),
   "execute if items entity @s weapon.* minecraft:netherite_sword[%s] run effect give @s minecraft:speed 3 0 true" % cnbt("scimitar"),
   "execute if items entity @s weapon.mainhand minecraft:golden_sword[%s] run effect give @s minecraft:haste 3 0 true" % cnbt("dagger"),
   "execute if items entity @s hotbar.* minecraft:totem_of_undying[%s] run effect give @s minecraft:luck 3 0 true" % cnbt("amulet"))
fn("items/lantern_aura",
   "effect give @s minecraft:night_vision 15 0 true",
   "effect give @e[distance=..12,type=#minecraft:undead] minecraft:glowing 3 0 true",
   "particle minecraft:small_flame ~ ~1.2 ~ 0.4 0.4 0.4 0.01 4",
   bar("@s", T("الذهب: ", "gold"), SC("@s", "nh_gold", "yellow"), T("   الأختام: ", "gold"), SC("#seals", "nh_g", "yellow"), T(" / ٧", "gold")))
fn("items/tick",
   "execute as @a[nbt={FallFlying:1b}] at @s if items entity @s armor.chest minecraft:elytra[%s] run function nahas:items/carpet_glide" % cnbt("carpet"))
fn("items/carpet_glide",
   "execute if entity @s[x_rotation=-25..90] run tp @s ^ ^ ^0.4",
   "effect give @s minecraft:slow_falling 2 0 true",
   "particle minecraft:cloud ~ ~ ~ 0.2 0.1 0.2 0.01 2")
fn("items/astro_update",
   "function nahas:core/next",
   "clear @s minecraft:compass[%s]" % cnbt("astrolabe"),
   *["execute if score #next nh_g matches %d run loot give @s loot nahas:items/astrolabe_%d" % (i, i) for i in range(8)])
nm_lines = []
for i, (dim, x, y, z, nm) in enumerate(ASTRO_TARGETS):
    nm_lines.append("execute if score #next nh_g matches %d run %s" % (i, tw("@s", T("وجهتك التالية: ", "yellow"), T(nm, "gold", bold=True),
                                                                          T("  (س=%d ، ع=%d ، ص=%d)" % (x, y, z), "gray"))))
fn("items/map",
   "scoreboard players operation @s nh_tmp = @s nh_map",
   "scoreboard players set @s nh_map 0",
   "execute if score @s nh_tmp matches 2 run function nahas:items/coords",
   "execute if score @s nh_tmp matches 3 run function nahas:items/list_places",
   "execute unless score @s nh_tmp matches 2..3 run function nahas:items/map_next")
fn("items/map_next", "function nahas:items/astro_update", nm_lines,
   "playsound minecraft:item.lodestone_compass.lock master @s ~ ~ ~ 1 1")
fn("items/coords",
   tw("@s", T("مكانك: س=", "yellow"), {"nbt": "Pos[0]", "entity": "@s", "color": "gold"}, T(" ، ع=", "yellow"),
      {"nbt": "Pos[1]", "entity": "@s", "color": "gold"}, T(" ، ص=", "yellow"), {"nbt": "Pos[2]", "entity": "@s", "color": "gold"}))
ll = [tw("@s", T("الأماكن التي اكتشفتها:", "gold"))]
for pid, (dim, x, y, z, nm, r) in POI.items():
    ll.append("execute if entity @s[tag=nh_d_%s] run %s" % (pid, tw("@s", T("- " + nm, "aqua"), T("  (س=%d ، ص=%d)" % (x, z), "gray"))))
fn("items/list_places", ll)
for k in ITEMS:
    fn("items/give_" + k, "loot give @s loot nahas:items/" + k)
fn("items/give_all", *["loot give @s loot nahas:items/%s" % k for k in ITEMS], "loot give @s loot nahas:trial/page")

# ---------------------------------------------------------------- shop
fn("shop/menu", tw("@s", T("=== سوق الجني ===  ذهبك: ", "gold"), SC("@s", "nh_gold", "yellow")))
for i, (nm, pr, ents) in SHOP.items():
    F["shop/menu"].append(tw("@s", CK("[%d] %s" % (i + 1, nm), "/trigger nh_shop set %d" % (i + 1), "green", "اضغط للشراء"),
                            T("  السعر: %d ذهب" % pr, "yellow")))
F["shop/menu"].append(tw("@s", CK("[٢٠] بيع سبائك الذهب (١٠ ذهب لكل سبيكة)", "/trigger nh_shop set 20", "gold"),
                        " ", CK("[٢١] بيع قطع الذهب (١ لكل قطعة)", "/trigger nh_shop set 21", "gold")))
sh = ["scoreboard players operation @s nh_tmp = @s nh_shop", "scoreboard players set @s nh_shop 0"]
for i in SHOP:
    sh.append("execute if score @s nh_tmp matches %d run function nahas:shop/buy_%d" % (i + 1, i))
sh += ["execute if score @s nh_tmp matches 20 run function nahas:shop/sell_ingots",
       "execute if score @s nh_tmp matches 21 run function nahas:shop/sell_nuggets",
       "execute unless score @s nh_tmp matches 2..13 unless score @s nh_tmp matches 20..21 run function nahas:shop/menu"]
fn("shop/trigger", sh)
for i, (nm, pr, ents) in SHOP.items():
    fn("shop/buy_%d" % i,
       "scoreboard players set #ok nh_g 0",
       "execute if score @s nh_gold matches %d.. run scoreboard players set #ok nh_g 1" % pr,
       "execute if score #ok nh_g matches 1 run function nahas:shop/do_%d" % i,
       "execute if score #ok nh_g matches 0 run " + tw("@s", T("ذهبك لا يكفي لشراء ", "red"), T(nm, "gold")))
    body = ["scoreboard players remove @s nh_gold %d" % pr, "loot give @s loot nahas:shop/%s" % SHOPKEY[i],
            tw("@s", T("اشتريت: ", "green"), T(nm, "gold"), T("  باقي ذهبك: ", "green"), SC("@s", "nh_gold", "yellow")),
            "playsound minecraft:entity.villager.trade master @s ~ ~ ~ 1 1", grant("@s", "shop")]
    if i == 9:
        body.append(grant("@s", "carpet"))
    fn("shop/do_%d" % i, body)
fn("shop/sell_ingots",
   "execute store result score #n nh_g run clear @s minecraft:gold_ingot",
   "scoreboard players operation #n nh_g *= #10 nh_g",
   "scoreboard players operation @s nh_gold += #n nh_g",
   tw("@s", T("بعت سبائك الذهب. ذهبك الآن: ", "green"), SC("@s", "nh_gold", "yellow")))
fn("shop/sell_nuggets",
   "execute store result score #n nh_g run clear @s minecraft:gold_nugget",
   "scoreboard players operation @s nh_gold += #n nh_g",
   tw("@s", T("بعت قطع الذهب. ذهبك الآن: ", "green"), SC("@s", "nh_gold", "yellow")))

# ---------------------------------------------------------------- quests
fn("quest/menu", tw("@s", T("=== المهام ===", "gold")),
   tw("@s", CK("[١] هدفي الرئيسي", "/trigger nh_quest set 1", "aqua"), " ", CK("[٢] المهام الجانبية", "/trigger nh_quest set 2", "aqua")))
fn("quest/trigger",
   "scoreboard players operation @s nh_tmp = @s nh_quest",
   "scoreboard players set @s nh_quest 0",
   "execute if score @s nh_tmp matches 1 run function nahas:quest/main",
   "execute if score @s nh_tmp matches 2 run function nahas:quest/side",
   *["execute if score @s nh_tmp matches %d run function nahas:quest/claim_%d" % (10 + q, q) for q in range(1, 6)],
   "execute unless score @s nh_tmp matches 1..2 unless score @s nh_tmp matches 11..15 run function nahas:quest/menu")
TR_NAMES = {1: "معبد الواحة", 2: "وادي العقارب", 3: "المكتبة الغارقة", 4: "قلعة الريح", 5: "بحر النجوم (عبر بوابة النجوم)",
            6: "أرض الجمر (عبر بوابة الجمر)"}
qm = ["function nahas:core/next",
      "execute unless score @s nh_prole matches 1..4 run " + say("@s", "خطوتك الأولى: اختر دورك بـ /trigger nh_role set 1", "yellow"),
      tw("@s", T("الأختام: ", "gold"), SC("#seals", "nh_g", "yellow"), T(" من ٧", "gold"))]
for i, nm in TR_NAMES.items():
    qm.append("execute unless score #t%d nh_g matches 9 run %s" % (i, tw("@s", T("- ", "gray"), T(nm, "aqua"), T("  (لم يكتمل)", "gray"))))
qm += ["execute if score #seals nh_g matches 6.. unless score #s7 nh_g matches 1 run " + tw("@s", T("اذهبوا إلى مدينة النحاس وواجهوا الحارس النحاسي!", "gold")),
       "execute if score #s7 nh_g matches 1 run " + tw("@s", T("أنقذتم المدينة! أنتم أبطال القافلة.", "green")),
       "execute if score #next nh_g matches 0 run " + say("@s", "اذهب أولاً إلى واحة الدلال (س=600 ، ص=1650).", "yellow"),
       "function nahas:items/map_next"]
fn("quest/main", qm)
QUESTS = {1: ("صياد مبتدئ: اهزم ١٠ وحوش", "scores={nh_kills=10..}", 30, None),
          2: ("صياد ماهر: اهزم ٥٠ وحشاً", "scores={nh_kills=50..}", 100, "shop/heal"),
          3: ("جامع الثروة: املك ٢٠٠ ذهب", "scores={nh_gold=200..}", 60, "gift/traveler"),
          4: ("مستكشف: اكتشف ٥ أماكن", "scores={nh_disc=5..}", 80, None),
          5: ("حامل الأختام: اجمعوا ٣ أختام", None, 150, "items/amulet")}
sd = [tw("@s", T("=== المهام الجانبية ===", "gold"))]
for q, (nm, cond, gold, rew) in QUESTS.items():
    sd.append("execute if entity @s[tag=nh_q%d] run %s" % (q, tw("@s", T("- " + nm, "gray"), T("  (تم)", "green"))))
    sd.append("execute unless entity @s[tag=nh_q%d] run %s" % (q, tw("@s", CK("[%d] %s" % (q, nm), "/trigger nh_quest set %d" % (10 + q), "aqua", "اضغط لاستلام الجائزة"),
                                                                    T("  الجائزة: %d ذهب" % gold, "yellow"))))
    body = ["tag @s add nh_q%d" % q, "scoreboard players add @s nh_gold %d" % gold, grant("@s", "quest"),
            tw("@s", T("أنجزت المهمة! +%d ذهب" % gold, "green")),
            "playsound minecraft:entity.player.levelup master @s ~ ~ ~ 1 1"]
    if rew:
        body.append("loot give @s loot nahas:" + rew)
    chk = "execute if entity @s[tag=nh_q%d] run %s" % (q, say("@s", "استلمت هذه الجائزة من قبل.", "yellow"))
    if q == 5:
        cnd = "execute unless entity @s[tag=nh_q5] if score #seals nh_g matches 3.. run function nahas:quest/do_5"
        nc = "execute unless entity @s[tag=nh_q5] unless score #seals nh_g matches 3.. run " + say("@s", "لم تكتمل المهمة بعد.", "red")
    else:
        cnd = "execute unless entity @s[tag=nh_q%d,%s] if entity @s[%s,tag=!nh_q%d] run function nahas:quest/do_%d" % (q, "x=0", cond, q, q)
        cnd = "execute if entity @s[%s,tag=!nh_q%d] run function nahas:quest/do_%d" % (cond, q, q)
        nc = "execute unless entity @s[tag=nh_q%d] unless entity @s[%s] run %s" % (q, cond, say("@s", "لم تكتمل المهمة بعد.", "red"))
    fn("quest/do_%d" % q, body)
    fn("quest/claim_%d" % q, chk, cnd, nc)
fn("quest/side", sd)

# ---------------------------------------------------------------- portals
port = []
for pid, back, dimc in (("star", "starsea", DS), ("ember", "embersea", DE)):
    d, x, y, z, nm, r = POI[pid]
    d2, x2, y2, z2, nm2, r2 = POI[back]
    port.append("execute in %s positioned %d %d %d as @a[distance=..2.2,scores={nh_pcd=..0}] at @s run function nahas:portal/to_%s" % (d, x, y + 1, z, back))
    port.append("execute in %s positioned %d %d %d as @a[distance=..2.2,scores={nh_pcd=..0}] at @s run function nahas:portal/from_%s" % (d2, x2, y2 + 1, z2, back))
    ox, oy, oz = TP_OFF[back]
    fn("portal/to_" + back,
       "scoreboard players set @s nh_pcd 6",
       "particle minecraft:portal ~ ~1 ~ 0.5 1 0.5 0.5 60",
       "playsound minecraft:block.portal.travel master @s ~ ~ ~ 0.5 1.2",
       "execute in %s run tp @s %d %d %d" % (dimc, x2 + ox, y2 + oy, z2 + oz),
       "tag @s add nh_d_%s" % back,
       grant("@s", "portal"),
       say("@s", "عبرت البوابة إلى " + nm2 + "...", "light_purple"),
       "particle minecraft:portal ~ ~1 ~ 0.5 1 0.5 0.5 60")
    fn("portal/from_" + back,
       "scoreboard players set @s nh_pcd 6",
       "particle minecraft:portal ~ ~1 ~ 0.5 1 0.5 0.5 60",
       "playsound minecraft:block.portal.travel master @s ~ ~ ~ 0.5 1.2",
       "execute in minecraft:overworld run tp @s %d %d %d" % (x, y + 1, z + 6),
       say("@s", "عدت إلى عالمك الأول.", "light_purple"),
       "particle minecraft:portal ~ ~1 ~ 0.5 1 0.5 0.5 60")
fn("portal/tick", port)
fn("portal/rescue_star",
   "tp @s 600 101 605", "effect give @s minecraft:slow_falling 5 0 true",
   say("@s", "أنقذك ضوء النجوم وأعادك إلى الجزيرة.", "aqua"),
   "particle minecraft:end_rod ~ ~1 ~ 0.5 1 0.5 0.1 30")
fn("portal/rescue_ember",
   "tp @s 500 65 505", say("@s", "أنقذتك شعلة الجمر وأعادتك إلى المنصة.", "gold"),
   "particle minecraft:flame ~ ~1 ~ 0.5 1 0.5 0.1 30")
# go menu
gm = [tw("@s", T("=== السفر السريع (للأماكن التي اكتشفتها) ===", "gold"))]
for v, pid in GO:
    nm = POI[pid][4]
    if pid in ("spawn", "hub"):
        gm.append(tw("@s", CK("[%d] %s" % (v + 1, nm), "/trigger nh_go set %d" % (v + 1), "aqua")))
    else:
        gm.append("execute if entity @s[tag=nh_d_%s] run %s" % (pid, tw("@s", CK("[%d] %s" % (v + 1, nm), "/trigger nh_go set %d" % (v + 1), "aqua"))))
        gm.append("execute unless entity @s[tag=nh_d_%s] run %s" % (pid, tw("@s", T("[%d] ؟؟؟ (لم تُكتشف)" % (v + 1), "dark_gray"))))
gm.append(tw("@s", CK("[13] الانتقال إلى صديق", "/trigger nh_go set 13", "green")))
fn("portal/go_menu", gm)
go = ["scoreboard players operation @s nh_tmp = @s nh_go", "scoreboard players set @s nh_go 0",
      "execute unless score @s nh_tmp matches 2..13 run function nahas:portal/go_menu",
      "execute if score @s nh_tmp matches 2..13 if score @s nh_gocd matches 1.. run " +
      tw("@s", T("انتظر ", "red"), SC("@s", "nh_gocd", "yellow"), T(" ثانية قبل السفر مرة أخرى.", "red"))]
for v, pid in GO:
    go.append("execute if score @s nh_tmp matches %d if score @s nh_gocd matches ..0 run function nahas:portal/go_%d" % (v + 1, v))
go.append("execute if score @s nh_tmp matches 13 if score @s nh_gocd matches ..0 run function nahas:portal/go_12")
fn("portal/go", go)
for v, pid in GO:
    dim, x, y, z, nm, r = POI[pid]
    ox, oy, oz = TP_OFF.get(pid, (0, 1, 0))
    body = []
    if pid not in ("spawn", "hub"):
        body.append("execute unless entity @s[tag=nh_d_%s] run %s" % (pid, say("@s", "لم تكتشف هذا المكان بعد.", "red")))
    tp = ["scoreboard players set @s nh_gocd 45", "particle minecraft:cloud ~ ~1 ~ 0.3 0.6 0.3 0.05 30",
          "execute in %s run tp @s %d.5 %d %d.5" % (dim, x + ox, y + oy, z + oz),
          "playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 1 1",
          say("@s", "وصلت إلى " + nm, "aqua"), "particle minecraft:cloud ~ ~1 ~ 0.3 0.6 0.3 0.05 30"]
    if pid == "city":
        body.append("execute unless score #city nh_g matches 1 run " + say("@s", "بوابة المدينة مغلقة حتى تجمعوا ستة أختام.", "red"))
        tp = ["execute if score #city nh_g matches 1 run " + t for t in tp]
    elif pid not in ("spawn", "hub"):
        tp = ["execute if entity @s[tag=nh_d_%s] run %s" % (pid, t) for t in tp]
    fn("portal/go_%d" % v, body, tp)
fn("portal/go_12",
   "tag @s add nh_self",
   "execute if entity @a[tag=!nh_self] run scoreboard players set @s nh_gocd 30",
   "execute if entity @a[tag=!nh_self] run tp @s @r[tag=!nh_self]",
   "execute unless entity @a[tag=!nh_self] run " + say("@s", "لا يوجد أصدقاء آخرون الآن.", "yellow"),
   "tag @s remove nh_self")

# ---------------------------------------------------------------- trials
TRIAL = {1: ("t1", "معبد الواحة", "اهزم موجات حراس المعبد!"), 2: ("t2", "وادي العقارب", "ملكة العقارب تنتظرك في الساحة!"),
         3: ("t3", "المكتبة الغارقة", "اجمع ثلاث صفحات مفقودة من حراس الأعماق!"), 4: ("t4", "قلعة الريح", "اصعد إلى ساحة القلعة وواجه قائد الرياح!"),
         5: ("starsea", "بحر النجوم", "قاوموا أرواح النجوم ثم واجهوا ملكة النجوم!"),
         6: ("embersea", "أرض الجمر", "اهزموا حراس الجمر ثم عملاق الجمر!"), 7: ("city", "قصر النحاس", "واجهوا الحارس النحاسي!")}
ts = []
for i, (pid, nm, dsc) in TRIAL.items():
    dim, x, y, z, _, r = POI[pid]
    rr = {1: 70, 2: 70, 3: 70, 4: 70, 5: 700, 6: 400, 7: 60}[i]
    ts.append("execute in %s positioned %d %d %d if entity @a[distance=..%d] run function nahas:trial/t%d/near" % (dim, x, y, z, rr, i))
    fn("trial/t%d/announce" % i,
       "scoreboard players set #trial nh_g %d" % i,
       title("@a[distance=..%d]" % rr, nm, dsc, "gold", "yellow", "10 90 20"),
       "playsound minecraft:block.bell.use master @a[distance=..%d] ~ ~ ~ 1 0.6" % rr,
       "execute as @a[distance=..%d] at @s run function nahas:hook/trial_start" % rr)
    # complete
    comp_lines = ["scoreboard players set #t%d nh_g 9" % i, "scoreboard players set #trial nh_g %d" % i,
                  "scoreboard players set #s%d nh_g 1" % i, "function nahas:core/seal_recount",
                  "execute as @a at @s run function nahas:core/seal_sync"]
    if i < 7:
        comp_lines.append("execute as @a at @s run function nahas:hook/trial_done")
    fn("trial/complete_%d" % i, comp_lines)
fn("trial/second", ts)

def waves(i, tag, plan):
    """plan: {wave: [(ent, dx,dz, kidsonly?)]}"""
    for w, ml in plan.items():
        L = []
        for ent, dx, dz, extra, opt in ml:
            l = mob(ent, dx, 1, dz, [tag, "nh_trial"], extra)
            L.append(("execute unless score #kids nh_g matches 1 run " + l) if opt else l)
        L.append("particle minecraft:poof ~ ~2 ~ 8 1 8 0.05 40")
        L.append("playsound minecraft:entity.evoker.prepare_summon master @a[distance=..100] ~ ~ ~ 1 0.8")
        fn("trial/t%d/w%d" % (i, w), L)

# T1 waves of guardians
waves(1, "nh_t1", {1: [("minecraft:husk", 12, 0, "", 0), ("minecraft:husk", -12, 0, "", 0), ("minecraft:husk", 0, 12, "", 1)],
                   2: [("minecraft:husk", 12, 6, "", 0), ("minecraft:pillager", -12, 6, "", 0), ("minecraft:husk", 6, -12, "", 0), ("minecraft:pillager", -6, -12, "", 1)],
                   3: [("minecraft:vindicator", 12, 0, "", 0), ("minecraft:husk", -12, 0, "", 0), ("minecraft:pillager", 0, 12, "", 0), ("minecraft:husk", 0, -12, "", 1), ("minecraft:husk", 9, 9, "", 1)]})
fn("trial/t1/near",
   "execute if score #t1 nh_g matches 0 run function nahas:trial/t1/begin",
   "execute if score #t1 nh_g matches 1..3 unless entity @e[tag=nh_t1,distance=..100] run function nahas:trial/t1/next")
fn("trial/t1/begin", "scoreboard players set #t1 nh_g 1", "function nahas:trial/t1/announce", "function nahas:trial/t1/w1")
fn("trial/t1/next", "scoreboard players add #t1 nh_g 1",
   "execute if score #t1 nh_g matches 2..3 run " + tw("@a[distance=..100]", T("موجة جديدة من الحراس!", "red")),
   "execute if score #t1 nh_g matches 2 run function nahas:trial/t1/w2",
   "execute if score #t1 nh_g matches 3 run function nahas:trial/t1/w3",
   "execute if score #t1 nh_g matches 4 run function nahas:trial/complete_1")

# T2 / T4 boss trials
for i, boss, arena in ((2, 1, 28), (4, 2, 35)):
    fn("trial/t%d/near" % i,
       "execute if score #t%d nh_g matches 0 run function nahas:trial/t%d/announce" % (i, i),
       "execute if score #t%d nh_g matches 0 run scoreboard players set #t%d nh_g 1" % (i, i),
       "execute if score #t%d nh_g matches 1 if entity @a[distance=..%d] run function nahas:boss/b%d/spawn" % (i, arena, boss))

# T3 pages
waves(3, "nh_t3", {1: [("minecraft:drowned", 10, 0, ',DeathLootTable:"nahas:trial/page"', 0), ("minecraft:drowned", -10, 0, ',DeathLootTable:"nahas:trial/page"', 0),
                       ("minecraft:drowned", 0, 10, ',DeathLootTable:"nahas:trial/page"', 0), ("minecraft:drowned", 0, -10, ',DeathLootTable:"nahas:trial/page"', 1)]})
fn("trial/t3/near",
   "execute if score #t3 nh_g matches 0 run function nahas:trial/t3/begin",
   "execute if score #t3 nh_g matches 1 store result score #pg nh_g run clear @a[distance=..100] minecraft:paper[minecraft:custom_data={nh:\"page\"}] 0",
   "execute if score #t3 nh_g matches 1 if score #pg nh_g matches 3.. run function nahas:trial/t3/finish",
   "execute if score #t3 nh_g matches 1 if score #pg nh_g matches ..2 unless entity @e[tag=nh_t3,distance=..100] run function nahas:trial/t3/w1")
fn("trial/t3/begin", "scoreboard players set #t3 nh_g 1", "function nahas:trial/t3/announce", "function nahas:trial/t3/w1")
fn("trial/t3/finish", "clear @a minecraft:paper[minecraft:custom_data={nh:\"page\"}]", "kill @e[tag=nh_t3,distance=..120]",
   tw("@a[distance=..100]", T("الصفحات الثلاث اكتملت! الكتب تعود إلى مكانها.", "green")), "function nahas:trial/complete_3")

# T5 star sea: two vex waves then boss
waves(5, "nh_t5", {1: [("minecraft:vex", 6, 3, "", 0), ("minecraft:vex", -6, 3, "", 0), ("minecraft:vex", 0, -8, "", 1)],
                   2: [("minecraft:vex", 8, 3, "", 0), ("minecraft:vex", -8, 3, "", 0), ("minecraft:vex", 0, 10, "", 0), ("minecraft:vex", 0, -10, "", 1)]})
fn("trial/t5/near",
   "execute if score #t5 nh_g matches 0 run function nahas:trial/t5/begin",
   "execute if score #t5 nh_g matches 1..2 unless entity @e[tag=nh_t5,distance=..800] run function nahas:trial/t5/next",
   "execute if score #t5 nh_g matches 3 run function nahas:boss/b3/spawn")
fn("trial/t5/begin", "scoreboard players set #t5 nh_g 1", "function nahas:trial/t5/announce", "function nahas:trial/t5/w1")
fn("trial/t5/next", "scoreboard players add #t5 nh_g 1", "execute if score #t5 nh_g matches 2 run function nahas:trial/t5/w2",
   "execute if score #t5 nh_g matches 2 run " + tw("@a[distance=..800]", T("موجة أرواح جديدة!", "light_purple")),
   "execute if score #t5 nh_g matches 3 run " + tw("@a[distance=..800]", T("ملكة النجوم تستيقظ...", "light_purple")))
# T6 ember: blaze wave then boss
waves(6, "nh_t6", {1: [("minecraft:blaze", 8, 2, "", 0), ("minecraft:blaze", -8, 2, "", 0), ("minecraft:blaze", 0, -9, "", 1)]})
fn("trial/t6/near",
   "execute if score #t6 nh_g matches 0 run function nahas:trial/t6/begin",
   "execute if score #t6 nh_g matches 1 unless entity @e[tag=nh_t6,distance=..500] run function nahas:trial/t6/next",
   "execute if score #t6 nh_g matches 2 run function nahas:boss/b4/spawn")
fn("trial/t6/begin", "scoreboard players set #t6 nh_g 1", "function nahas:trial/t6/announce", "function nahas:trial/t6/w1")
fn("trial/t6/next", "scoreboard players set #t6 nh_g 2", tw("@a[distance=..500]", T("عملاق الجمر يخرج من الحمم!", "red")))
# T7 city
fn("trial/t7/near",
   "execute if score #t7 nh_g matches 0 if score #city nh_g matches 1 run function nahas:trial/t7/announce",
   "execute if score #t7 nh_g matches 0 if score #city nh_g matches 1 run scoreboard players set #t7 nh_g 1",
   "execute if score #t7 nh_g matches 1 if entity @a[distance=..30] run function nahas:boss/b5/spawn")

# ---------------------------------------------------------------- bosses
BOSS = {
    1: dict(name="ملكة العقارب", color="yellow", dim=DO, pos=(1800, 71, 1850), ent="minecraft:spider", scale=3.0, hp=400, hpk=200, dmg=6, dmgk=3,
            trial=2, watch=70,
            p_msg=["ملكة العقارب تستيقظ! حاذر لدغتها.", "ملكة العقارب تغضب وتسرع!", "الملكة في أشد غضبها!"],
            acts=[[mob("minecraft:cave_spider", 3, 0, 3, ["nh_bm"]), "effect give @a[distance=..5] minecraft:poison 3 0 true",
                   "particle minecraft:sneeze ~ ~1 ~ 2 0.5 2 0 15"],
                  [mob("minecraft:cave_spider", 3, 0, -3, ["nh_bm"]), mob("minecraft:cave_spider", -3, 0, 3, ["nh_bm"]),
                   "particle minecraft:cloud ~ ~ ~ 4 0.2 4 0.1 40"] + dmg("@a[distance=..6]", 3),
                  [mob("minecraft:cave_spider", 4, 0, 0, ["nh_bm"]), mob("minecraft:cave_spider", -4, 0, 0, ["nh_bm"]),
                   "effect give @a[distance=..8] minecraft:slowness 3 0 true", "particle minecraft:smoke ~ ~1 ~ 3 0.5 3 0.05 40"] + dmg("@a[distance=..7]", 4)],
            enters=[["playsound minecraft:entity.spider.ambient master @a[distance=..60] ~ ~ ~ 2 0.5"],
                    ["effect give @s minecraft:speed 30 1 true"], ["effect give @s minecraft:strength 30 0 true"]]),
    2: dict(name="قائد الرياح", color="white", dim=DO, pos=(1700, 121, 450), ent="minecraft:breeze", scale=2.0, hp=300, hpk=150, dmg=5, dmgk=3,
            trial=4, watch=70,
            p_msg=["قائد الرياح يهب بعاصفة!", "الرياح تشتد!", "العاصفة الأخيرة!"],
            acts=[["effect give @a[distance=..12] minecraft:levitation 1 0 true", "effect give @a[distance=..12] minecraft:slow_falling 6 0 true",
                   "particle minecraft:cloud ~ ~1 ~ 3 1 3 0.1 40"],
                  [mob("minecraft:vex", 2, 1, 2, ["nh_bm"]), "effect give @a[distance=..14] minecraft:levitation 1 0 true",
                   "effect give @a[distance=..14] minecraft:slow_falling 6 0 true"],
                  [mob("minecraft:vex", 2, 1, 2, ["nh_bm"]), mob("minecraft:vex", -2, 1, -2, ["nh_bm"]),
                   "effect give @a[distance=..16] minecraft:levitation 2 0 true", "effect give @a[distance=..16] minecraft:slow_falling 8 0 true"] + dmg("@a[distance=..8]", 3)],
            enters=[["playsound minecraft:entity.breeze.idle_ground master @a[distance=..60] ~ ~ ~ 2 0.6"],
                    ["effect give @s minecraft:speed 30 1 true"], ["effect give @s minecraft:resistance 30 1 true"]]),
    3: dict(name="ملكة النجوم", color="light_purple", dim=DS, pos=(600, 101, 600), ent="minecraft:evoker", scale=1.5, hp=350, hpk=175, dmg=6, dmgk=3,
            trial=5, watch=200,
            p_msg=["ملكة النجوم تنزل من السماء!", "النجوم تتساقط!", "ملكة النجوم تجمع كل ضيائها!"],
            acts=[["particle minecraft:end_rod ~ ~2 ~ 4 1 4 0.05 50"],
                  [mob("minecraft:vex", 3, 1, 0, ["nh_bm"]), "particle minecraft:end_rod ~ ~2 ~ 5 1 5 0.05 60"] + dmg("@a[distance=..6]", 2),
                  [mob("minecraft:vex", 3, 1, 0, ["nh_bm"]), mob("minecraft:vex", -3, 1, 0, ["nh_bm"]),
                   "particle minecraft:end_rod ~ ~2 ~ 6 1 6 0.05 80", "effect give @a[distance=..10] minecraft:slowness 2 0 true"] + dmg("@a[distance=..8]", 3)],
            enters=[["playsound minecraft:block.beacon.activate master @a[distance=..100] ~ ~ ~ 2 0.5"],
                    ["effect give @s minecraft:speed 30 0 true"], ["effect give @s minecraft:resistance 30 1 true"]]),
    4: dict(name="عملاق الجمر", color="red", dim=DE, pos=(500, 65, 496), ent="minecraft:wither_skeleton", scale=3.0, hp=450, hpk=225, dmg=8, dmgk=4,
            trial=6, watch=200,
            p_msg=["عملاق الجمر يخرج من الحمم!", "الجمر يشتعل أكثر!", "عملاق الجمر في ذروة غضبه!"],
            acts=[["particle minecraft:flame ~ ~1 ~ 3 1 3 0.05 60"],
                  [mob("minecraft:blaze", 4, 1, 0, ["nh_bm"]), "particle minecraft:lava ~ ~1 ~ 4 1 4 0 30"] + dmg("@a[distance=..6]", 3),
                  [mob("minecraft:blaze", 4, 1, 0, ["nh_bm"]), mob("minecraft:blaze", -4, 1, 0, ["nh_bm"]),
                   "particle minecraft:lava ~ ~1 ~ 5 1 5 0 50"] + dmg("@a[distance=..8]", 4)],
            enters=[["playsound minecraft:entity.wither.spawn master @a[distance=..100] ~ ~ ~ 1 0.6"],
                    ["effect give @s minecraft:speed 30 0 true"], ["effect give @s minecraft:strength 30 0 true"]]),
    5: dict(name="الحارس النحاسي", color="gold", dim=DO, pos=(1200, 71, 1200), ent="minecraft:iron_golem", scale=3.0, hp=800, hpk=400, dmg=12, dmgk=5,
            trial=7, watch=70,
            p_msg=["الحارس النحاسي يستيقظ! أنتم لا تعرفون ما ينتظركم.", "الحارس ينادي جنوده النحاسيين!", "الحارس في الغضب الأخير! اضربوا معاً!"],
            acts=[["particle minecraft:crit ~ ~1 ~ 4 0.5 4 0.2 60"] + dmg("@a[distance=..6]", 4),
                  [mob("minecraft:vindicator", 6, 0, 0, ["nh_bm"], ""), "execute unless score #kids nh_g matches 1 run " + mob("minecraft:vindicator", -6, 0, 0, ["nh_bm"]),
                   "particle minecraft:crit ~ ~1 ~ 5 0.5 5 0.2 80"] + dmg("@a[distance=..7]", 5),
                  [mob("minecraft:husk", 6, 0, 0, ["nh_bm"]), mob("minecraft:husk", -6, 0, 0, ["nh_bm"]),
                   "execute unless score #kids nh_g matches 1 run " + mob("minecraft:pillager", 0, 0, 6, ["nh_bm"]),
                   "effect give @a[distance=..9] minecraft:slowness 2 0 true", "particle minecraft:explosion ~ ~1 ~ 4 0.5 4 0 5"] + dmg("@a[distance=..8]", 6)],
            enters=[["playsound minecraft:block.anvil.land master @a[distance=..100] ~ ~ ~ 2 0.5"],
                    ["effect give @s minecraft:speed 30 0 true", "effect give @s minecraft:resistance 30 1 true"],
                    ["effect give @s minecraft:strength 30 1 true", "effect give @s minecraft:speed 30 1 true"]]),
}
bsec = []
for b, d in BOSS.items():
    dim = d["dim"]; x, y, z = d["pos"]; tn = d["trial"]
    bsec.append("execute if score #t%d nh_g matches 50 in %s positioned %d %d %d if entity @a[distance=..%d] run function nahas:boss/b%d/watch" % (tn, dim, x, y, z, d["watch"], b))
    nmj = J(T(d["name"], d["color"]))
    fn("boss/b%d/spawn" % b,
       "scoreboard players set #t%d nh_g 50" % tn,
       "scoreboard players set #boss nh_g %d" % b,
       "scoreboard players set #b%d_ph nh_g 0" % b, "scoreboard players set #b%d_t nh_g 0" % b, "scoreboard players set #b%d_miss nh_g 0" % b,
       "scoreboard players set #bmax%d nh_g %d" % (b, d["hp"]),
       "execute if score #kids nh_g matches 1 run scoreboard players set #bmax%d nh_g %d" % (b, d["hpk"]),
       "execute in %s run summon %s %d %d %d {Tags:[\"nh_boss\",\"nh_b%d\"],PersistenceRequired:1b}" % (dim, d["ent"], x, y, z, b),
       "execute in %s positioned %d %d %d as @e[tag=nh_b%d,distance=..6,limit=1] run function nahas:boss/b%d/init" % (dim, x, y, z, b, b),
       "bossbar set nahas:boss%d name %s" % (b, nmj), "bossbar set nahas:boss%d color %s" % (b, "red" if d["color"] in ("red", "gold", "yellow") else "purple"),
       "bossbar set nahas:boss%d style notched_10" % b,
       "execute store result bossbar nahas:boss%d max run scoreboard players get #bmax%d nh_g" % (b, b),
       "execute store result bossbar nahas:boss%d value run scoreboard players get #bmax%d nh_g" % (b, b),
       "bossbar set nahas:boss%d visible true" % b,
       title("@a[distance=..100]", d["name"], "المعركة بدأت!", d["color"], "yellow", "10 60 20"),
       "execute as @a[distance=..100] at @s run function nahas:hook/boss_start")
    fn("boss/b%d/init" % b,
       "attribute @s minecraft:max_health base set %d" % d["hp"], "attribute @s minecraft:scale base set %s" % d["scale"],
       "attribute @s minecraft:attack_damage base set %d" % d["dmg"], "attribute @s minecraft:knockback_resistance base set 0.7",
       "attribute @s minecraft:follow_range base set 64",
       "data modify entity @s Health set value %d.0f" % d["hp"],
       "execute if score #kids nh_g matches 1 run function nahas:boss/b%d/init_kids" % b)
    fn("boss/b%d/init_kids" % b,
       "attribute @s minecraft:max_health base set %d" % d["hpk"], "attribute @s minecraft:attack_damage base set %d" % d["dmgk"],
       "data modify entity @s Health set value %d.0f" % d["hpk"])
    fn("boss/b%d/watch" % b,
       "execute if entity @e[tag=nh_b%d,distance=..120] run function nahas:boss/b%d/alive" % (b, b),
       "execute unless entity @e[tag=nh_b%d,distance=..120] run function nahas:boss/b%d/miss" % (b, b))
    fn("boss/b%d/alive" % b, "scoreboard players set #b%d_miss nh_g 0" % b,
       "execute as @e[tag=nh_b%d,distance=..120,limit=1] at @s run function nahas:boss/b%d/tick" % (b, b))
    fn("boss/b%d/tick" % b,
       "bossbar set nahas:boss%d players @a[distance=..100]" % b,
       "execute store result score #hp nh_g run data get entity @s Health",
       "execute store result bossbar nahas:boss%d value run data get entity @s Health" % b,
       "scoreboard players operation #pct nh_g = #hp nh_g", "scoreboard players operation #pct nh_g *= #100 nh_g",
       "scoreboard players operation #pct nh_g /= #bmax%d nh_g" % b,
       "scoreboard players set #np nh_g 1",
       "execute if score #pct nh_g matches ..66 run scoreboard players set #np nh_g 2",
       "execute if score #pct nh_g matches ..33 run scoreboard players set #np nh_g 3",
       "execute unless score #np nh_g = #b%d_ph nh_g run function nahas:boss/b%d/phase" % (b, b),
       "scoreboard players add #b%d_t nh_g 1" % b,
       "execute if score #b%d_t nh_g matches 5.. run function nahas:boss/b%d/act" % (b, b))
    ph = ["scoreboard players operation #b%d_ph nh_g = #np nh_g" % b, "scoreboard players operation #phase nh_g = #np nh_g",
          "scoreboard players set #boss nh_g %d" % b]
    for p in (1, 2, 3):
        ph.append("execute if score #np nh_g matches %d run function nahas:boss/b%d/p%d" % (p, b, p))
        fn("boss/b%d/p%d" % (b, p), tw("@a[distance=..100]", T(d["p_msg"][p - 1], d["color"], bold=True)), d["enters"][p - 1],
           "playsound minecraft:entity.ender_dragon.growl master @a[distance=..60] ~ ~ ~ 1 1.2")
    ph.append("execute as @a[distance=..100] at @s run function nahas:hook/boss_phase")
    fn("boss/b%d/phase" % b, ph)
    ac = ["scoreboard players set #b%d_t nh_g 0" % b]
    for p in (1, 2, 3):
        ac.append("execute if score #b%d_ph nh_g matches %d run function nahas:boss/b%d/a%d" % (b, p, b, p))
        fn("boss/b%d/a%d" % (b, p), d["acts"][p - 1])
    fn("boss/b%d/act" % b, ac)
    fn("boss/b%d/miss" % b, "scoreboard players add #b%d_miss nh_g 1" % b,
       "execute if score #b%d_miss nh_g matches 3.. run function nahas:boss/b%d/defeated" % (b, b))
    df = ["bossbar set nahas:boss%d visible false" % b, "bossbar set nahas:boss%d players" % b,
          "scoreboard players set #b%d_ph nh_g 0" % b, "kill @e[tag=nh_bm,distance=..150]",
          "loot spawn ~ ~1 ~ loot nahas:chests/boss",
          "execute as @a[distance=..100] run scoreboard players add @s nh_gold 100",
          title("@a[distance=..100]", "انتصرتم!", d["name"] + " هُزم", "green", "yellow", "10 70 20"),
          "playsound minecraft:ui.toast.challenge_complete master @a[distance=..100] ~ ~ ~ 1 1",
          "particle minecraft:totem_of_undying ~ ~2 ~ 3 2 3 0.3 100",
          "function nahas:trial/complete_%d" % tn]
    if b == 5:
        df += ["execute as @a at @s run function nahas:hook/boss_defeated", grant("@a", "final"),
               "execute as @a run loot give @s loot nahas:gift/final_reward",
               tw("@a", T("هُزم الحارس النحاسي! استيقظت المدينة وتحرر أهلها. شكراً لكم أيها الأبطال!", "gold", bold=True))]
    fn("boss/b%d/defeated" % b, df)
fn("boss/second", bsec)
fn("boss/reset_all", *["scoreboard players set #t%d nh_g 0" % i for i in range(1, 8)], "kill @e[tag=nh_boss]", "kill @e[tag=nh_bm]",
   "kill @e[tag=nh_trial]")

# ---------------------------------------------------------------- admin
for n in range(1, 8):
    fn("core/admin/seal_%d" % n, "function nahas:trial/complete_%d" % n)
fn("core/admin/reset", "function nahas:boss/reset_all",
   *["scoreboard players set #s%d nh_g 0" % i for i in range(1, 8)],
   "scoreboard players set #seals nh_g 0", "scoreboard players set #city nh_g 0", "scoreboard players set #gate nh_g 0",
   "tag @a remove nh_got1", "tag @a remove nh_got2", "tag @a remove nh_got3", "tag @a remove nh_got4", "tag @a remove nh_got5",
   "tag @a remove nh_got6", "tag @a remove nh_got7")

# ---------------------------------------------------------------- selftest
def ok(sel, msg):
    return tw(sel, T("[نجح] ", "green", bold=True), T(msg, "white"))
def bad(sel, msg):
    return tw(sel, T("[فشل] ", "red", bold=True), T(msg, "white"))
def check(cond, msg, sel="@a[tag=nh_tester]"):
    return ["execute %s run %s" % (cond, ok(sel, msg)), "execute unless %s run %s" % (cond.replace("if ", "", 1) if cond.startswith("if ") else cond, bad(sel, msg))]

st = ["tag @s add nh_tester", say("@s", "=== اختبار مدينة النحاس ===", "gold"),
      "execute if score #loaded nh_g matches 1 run " + ok("@s", "الحزمة محمّلة (nahas:core/load)"),
      "execute unless score #loaded nh_g matches 1 run " + bad("@s", "الحزمة غير محمّلة، جرّب /reload"),
      "execute store result score #n nh_g run scoreboard objectives list",
      "execute if score #n nh_g matches 10.. run " + ok("@s", "لوحات النقاط موجودة"),
      "execute unless score #n nh_g matches 10.. run " + bad("@s", "لوحات النقاط ناقصة"),
      "execute store result score #n nh_g run loot spawn ~ ~ ~ loot nahas:items/seal_1",
      "execute if score #n nh_g matches 1.. run " + ok("@s", "جداول الغنائم تعمل (ختم النحاس)"),
      "execute unless score #n nh_g matches 1.. run " + bad("@s", "جدول الغنائم لا يعمل"),
      "kill @e[type=minecraft:item,distance=..3,nbt={Item:{id:\"minecraft:copper_ingot\"}}]",
      "execute store result score #n nh_g run loot spawn ~ ~ ~ loot nahas:kit/start",
      "execute if score #n nh_g matches 1.. run " + ok("@s", "حقيبة البداية تعمل"),
      "execute unless score #n nh_g matches 1.. run " + bad("@s", "حقيبة البداية لا تعمل"),
      "kill @e[type=minecraft:item,distance=..3]",
      "execute store success score #d1 nh_g in nahas:star_sea run forceload add 600 600",
      "execute store success score #d2 nh_g in nahas:ember run forceload add 500 500",
      "execute if score #d1 nh_g matches 1 run " + ok("@s", "البُعد nahas:star_sea موجود"),
      "execute unless score #d1 nh_g matches 1 run " + bad("@s", "البُعد nahas:star_sea غير موجود"),
      "execute if score #d2 nh_g matches 1 run " + ok("@s", "البُعد nahas:ember موجود"),
      "execute unless score #d2 nh_g matches 1 run " + bad("@s", "البُعد nahas:ember غير موجود"),
      "execute store success score #h1 nh_g run function nahas:hook/tick",
      "execute store success score #h2 nh_g run function nahas:ambient/second",
      "execute store success score #h3 nh_g run function nahas:npc/second",
      "execute unless score #h1 nh_g matches 0 unless score #h2 nh_g matches 0 unless score #h3 nh_g matches 0 run " + ok("@s", "دوال القصة (hook/ambient/npc) موجودة"),
      "execute if score #h1 nh_g matches 0 run " + bad("@s", "hook/tick غير موجودة"),
      "execute if score #h2 nh_g matches 0 run " + bad("@s", "ambient/second غير موجودة"),
      "execute if score #h3 nh_g matches 0 run " + bad("@s", "npc/second غير موجودة"),
      say("@s", "جارٍ فحص عالم الخريطة (٣ ثوانٍ)...", "gray")]
for pid in ("spawn", "hub", "t1", "t2", "t3", "t4", "star", "ember", "city"):
    dim, x, y, z, nm, r = POI[pid]
    st.append("execute in minecraft:overworld run forceload add %d %d" % (x, z))
st.append("schedule function nahas:selftest2 60t")
fn("selftest", st)
s2 = []
for pid in ("spawn", "hub", "t1", "t2", "t3", "t4", "star", "ember", "city"):
    dim, x, y, z, nm, r = POI[pid]
    s2.append("execute in minecraft:overworld if block %d %d %d minecraft:air run %s" % (x, y, z, bad("@a[tag=nh_tester]", "لا أرض عند " + nm)))
    s2.append("execute in minecraft:overworld unless block %d %d %d minecraft:air run %s" % (x, y, z, ok("@a[tag=nh_tester]", "أرض موجودة عند " + nm)))
    s2.append("execute in minecraft:overworld run forceload remove %d %d" % (x, z))
s2 += ["execute in nahas:star_sea unless block 600 100 600 minecraft:air run " + ok("@a[tag=nh_tester]", "جزيرة الوصول في بحر النجوم موجودة"),
       "execute in nahas:star_sea if block 600 100 600 minecraft:air run " + bad("@a[tag=nh_tester]", "لا جزيرة عند (600،100،600) في بحر النجوم"),
       "execute in nahas:ember unless block 500 64 500 minecraft:air run " + ok("@a[tag=nh_tester]", "منصة الوصول في أرض الجمر موجودة"),
       "execute in nahas:ember if block 500 64 500 minecraft:air run " + bad("@a[tag=nh_tester]", "لا منصة عند (500،64،500) في أرض الجمر"),
       "execute in nahas:star_sea run forceload remove 600 600", "execute in nahas:ember run forceload remove 500 500",
       say("@a[tag=nh_tester]", "=== انتهى الاختبار ===", "gold"), "tag @a remove nh_tester"]
fn("selftest2", s2)

# ---------------------------------------------------------------- write
def w(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

for d in ("core", "trial", "items", "shop", "portal", "boss", "role", "quest"):
    shutil.rmtree(os.path.join(FN, d), ignore_errors=True)
for d in ("loot_table", "advancement", "dimension"):
    shutil.rmtree(os.path.join(NS, d), ignore_errors=True)
for k, lines in F.items():
    w(os.path.join(FN, k + ".mcfunction"), "\n".join(flat(lines)) + "\n")
for k, v in LT.items():
    w(os.path.join(NS, "loot_table", k + ".json"), json.dumps(v, ensure_ascii=False, indent=1))
for k, v in ADV.items():
    w(os.path.join(NS, "advancement", k + ".json"), json.dumps(v, ensure_ascii=False, indent=1))
w(os.path.join(NS, "dimension", "star_sea.json"), json.dumps({
    "type": "minecraft:the_end",
    "generator": {"type": "minecraft:flat", "settings": {"biome": "minecraft:the_end", "features": False, "lakes": False,
                                                          "layers": [], "structure_overrides": []}}}, indent=1))
w(os.path.join(NS, "dimension", "ember.json"), json.dumps({
    "type": "minecraft:the_nether",
    "generator": {"type": "minecraft:flat", "settings": {"biome": "minecraft:nether_wastes", "features": False, "lakes": False,
                                                          "layers": [], "structure_overrides": []}}}, indent=1))
w(os.path.join(DP, "data", "minecraft", "tags", "function", "load.json"),
  json.dumps({"values": ["nahas:core/load", {"id": "nahas:story/load", "required": False}]}, indent=1))
w(os.path.join(DP, "data", "minecraft", "tags", "function", "tick.json"), json.dumps({"values": ["nahas:core/tick"]}, indent=1))
w(os.path.join(DP, "pack.mcmeta"), json.dumps({"pack": {
    "pack_format": 61, "supported_formats": {"min_inclusive": 61, "max_inclusive": 121},
    "min_format": 61, "max_format": 121,
    "description": "مدينة النحاس: ليلة الفانوس"}}, ensure_ascii=False, indent=1))
print("functions:", len(F), "loot tables:", len(LT), "advancements:", len(ADV))
