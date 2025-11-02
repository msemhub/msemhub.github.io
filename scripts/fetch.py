import requests, json, os

all_sets_text = requests.get("https://raw.githubusercontent.com/cajunwritescode/MSEM/refs/heads/main/AllSets.json").text

all_sets_json = json.loads(all_sets_text)

def print_set_json(msem_json): 
    in_dfc = False

    set_json = {}
    card = {}
    set_json["name"] = msem_json["name"]
    set_json["formats"] = ""
    set_json["trimmed"] = "y"
    set_json["image_type"] = "jpg"
    set_json["draft_structure"] = "play booster"
    set_json["image_name"] = "position"
    set_json["cards"] = []

    for msem_card in msem_json["cards"]:
        if not in_dfc: card = {}

        card["card_name" + ("2" if in_dfc else "")] = msem_card["name"]
        card["color" + ("2" if in_dfc else "")] = liststr(msem_card["colors"])
        card["type" + ("2" if in_dfc else "")] = msem_card["type"]
        card["cost" + ("2" if in_dfc else "")] = msem_card["manaCost"]
        card["rules_text" + ("2" if in_dfc else "")] = msem_card["text"]
        card["flavor_text" + ("2" if in_dfc else "")] = "[i]" + msem_card["flavor"] + "[/i]"
        card["pt" + ("2" if in_dfc else "")] = "" if not msem_card.get("power") else str(msem_card["power"]) + "/" + str(msem_card["toughness"])
        card["special_text" + ("2" if in_dfc else "")] = ""
        card["loyalty" + ("2" if in_dfc else "")] = "" if not msem_card.get("loyalty") else msem_card["loyalty"]
        card["artist" + ("2" if in_dfc else "")] = msem_card["artist"]
        card["alias" + ("2" if in_dfc else "")] = ""

        if card_layout(msem_card) == "adventure":
            adventure = msem_card["pageData"]
            card["card_name2"] = adventure["name"]
            card["cost2"] = adventure["manaCost"]
            card["rules_text2"] = adventure["text"]
            card["color2"] = getColors(adventure["manaCost"])
            card["flavor_text2"] = "[i][/i]"
            card["pt2"] = ""
            card["special_text2"] = ""
            card["artist2"] = card["artist"]
            card["alias2"] = ""
            card["loyalty2"] = ""
            card["rules_text"] = msem_card["text"].split("-----\n")[0]

        if not in_dfc:
            card["shape"] = card_layout(msem_card)
            card["set"] = msem_json["code"]
            card["position"] = msem_card["number"]
            card["notes"] = ""
            card["color_identity"] = liststr(msem_card["colorIdentity"])
            card["rarity"] = msem_card["rarity"]
            card["number"] = int(msem_card["number"].replace("a", "").replace("b", ""))

        if in_dfc: in_dfc = False
        if "a" in msem_card["number"]: in_dfc = True

        set_json["cards"].append(card)

    set_path = os.path.join("sets", msem_json["code"] + "-files")
    set_json_path = os.path.join(set_path, msem_json["code"] + ".json")

    if not os.path.exists(set_path):
        os.mkdir(set_path)

    if os.path.exists(set_json_path):
        os.remove(set_json_path)

    with open(set_json_path, "w", encoding = "utf-8-sig") as f:
        json.dump(set_json, f)

def card_layout(msem_card):
    if msem_card["layout"] == "modal_dfc":
        return "modal double faced"
    if msem_card["layout"] == "transform":
        return "transforming double faced"
    if msem_card.get("frameType") == "adventure":
        return "adventure"
    
    return "normal"

def getColors(c):
    colors = "WUBRG"
    res = ""

    for color in colors:
        if color in c:
            res += color

    return res

def liststr(l):
    s = ""
    for i in l:
        s += i

    return s

for code, msem_json in all_sets_json["data"].items():
    print("Writing " + code + "...")
    print_set_json(msem_json)