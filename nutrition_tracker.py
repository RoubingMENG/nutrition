"""Daily Nutrition Tracker - for Pythonista 3 on iPhone.

Foods are stored per 100 g (calories, fat, protein, carbs).
You log how many grams you ate; the app scales and sums the day.
Data is saved in nutrition_data.json next to this script.
"""
import json
import os
from datetime import date

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nutrition_data.json")
FIELDS = ["calories", "fat", "protein", "carbs"]
UNITS = {"calories": "kcal", "fat": "g", "protein": "g", "carbs": "g"}


# ---------------- Core logic (no UI) ----------------
def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"foods": {}, "log": []}


def save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_food(data, name, calories, fat, protein, carbs):
    """Nutrition values are per 100 g."""
    data["foods"][name] = {"calories": calories, "fat": fat,
                           "protein": protein, "carbs": carbs}


def log_food(data, name, grams, day=None):
    data["log"].append({"date": day or date.today().isoformat(),
                        "food": name, "grams": grams})


def entry_nutrition(data, entry):
    food = data["foods"][entry["food"]]
    factor = entry["grams"] / 100.0
    return {k: food[k] * factor for k in FIELDS}


def day_summary(data, day=None):
    day = day or date.today().isoformat()
    total = {k: 0.0 for k in FIELDS}
    lines = []
    for e in data["log"]:
        if e["date"] != day or e["food"] not in data["foods"]:
            continue
        n = entry_nutrition(data, e)
        for k in FIELDS:
            total[k] += n[k]
        lines.append("%s %gg: %.0f kcal" % (e["food"], e["grams"], n["calories"]))
    return lines, total


def format_summary(lines, total):
    body = "\n".join(lines) if lines else "Nothing logged yet."
    totals = ("\n\nTOTAL\nCalories: %.0f kcal\nFat: %.1f g\nProtein: %.1f g\nCarbs: %.1f g"
              % (total["calories"], total["fat"], total["protein"], total["carbs"]))
    return body + totals


def delete_last_today(data):
    today = date.today().isoformat()
    for i in range(len(data["log"]) - 1, -1, -1):
        if data["log"][i]["date"] == today:
            return data["log"].pop(i)
    return None


# ---------------- UI layer ----------------
try:
    import dialogs
    import console
    IN_PYTHONISTA = True
except ImportError:  # lets you test on a computer
    IN_PYTHONISTA = False


def ui_message(title, text):
    if IN_PYTHONISTA:
        console.alert(title, text, "OK", hide_cancel_button=True)
    else:
        print("\n== %s ==\n%s" % (title, text))


def ui_pick(title, items):
    if IN_PYTHONISTA:
        return dialogs.list_dialog(title, items)
    print("\n" + title)
    for i, it in enumerate(items, 1):
        print(" %d. %s" % (i, it))
    s = input("> ").strip()
    return items[int(s) - 1] if s.isdigit() and 1 <= int(s) <= len(items) else None


def ui_form(title, fields):
    """fields: list of (label, 'text'|'number'). Returns list of values or None."""
    if IN_PYTHONISTA:
        res = dialogs.form_dialog(title, [{"title": l, "type": t} for l, t in fields])
        if not res:
            return None
        return [res[l] for l, _ in fields]
    print("\n" + title)
    return [input(l + ": ") for l, _ in fields]


def to_num(s):
    try:
        return float(str(s).strip())
    except ValueError:
        return None


def screen_add_food(data):
    r = ui_form("New food (values per 100 g)",
                [("Name", "text"), ("Calories", "number"), ("Fat", "number"),
                 ("Protein", "number"), ("Carbs", "number")])
    if not r:
        return
    name = r[0].strip()
    nums = [to_num(x) for x in r[1:]]
    if not name or None in nums:
        ui_message("Error", "Enter a name and numbers for every field.")
        return
    add_food(data, name, *nums)
    save(data)
    ui_message("Saved", "%s added." % name)


def screen_log(data):
    if not data["foods"]:
        ui_message("No foods", "Add a food first.")
        return
    name = ui_pick("What did you eat?", sorted(data["foods"]))
    if not name:
        return
    r = ui_form("Weight of %s" % name, [("Grams", "number")])
    grams = to_num(r[0]) if r else None
    if grams is None or grams <= 0:
        return
    log_food(data, name, grams)
    save(data)
    n = entry_nutrition(data, data["log"][-1])
    ui_message("Logged", "%s %gg\n%.0f kcal | F %.1f | P %.1f | C %.1f"
               % (name, grams, n["calories"], n["fat"], n["protein"], n["carbs"]))


def screen_today(data):
    lines, total = day_summary(data)
    ui_message("Today (%s)" % date.today().isoformat(), format_summary(lines, total))


def screen_delete(data):
    e = delete_last_today(data)
    if e:
        save(data)
        ui_message("Deleted", "Removed %s %gg." % (e["food"], e["grams"]))
    else:
        ui_message("Nothing to delete", "No entries today.")


def main():
    data = load()
    menu = {"Log food I ate": screen_log, "Today's totals": screen_today,
            "Add new food": screen_add_food, "Undo last entry": screen_delete}
    while True:
        choice = ui_pick("Nutrition Tracker", list(menu))
        if not choice:
            break
        menu[choice](data)


if __name__ == "__main__":
    main()
