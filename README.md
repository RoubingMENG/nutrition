# Nutrition Tracker

A simple, private daily nutrition tracker that runs in your browser. It is a single `index.html` file with no accounts, no server and no build step. It works well on an iPhone and can be added to the home screen like an app.

**Live site:** `https://roubingmeng.github.io/nutrition/`

## Features

- **Foods database:** save foods with calories, fat, protein and carbs per 100 g.
- **kJ or kcal:** enter energy in kJ (the default) or kcal. Everything is calculated in kcal.
- **Serving sizes:** set a serving (for example, 1 biscuit = 5 g) and log by servings instead of weighing.
- **Meals of the day:** log to Breakfast, Lunch, Dinner or Snack, with per-meal calories, fat, protein and carbs.
- **Daily goals:** set a calorie goal (and optional fat, protein and carb goals) and see progress such as `500 / 2000 kcal`.
- **Any date:** log, browse and edit entries for past or future days.
- **Edit entries:** change the amount, unit, meal or date of anything you logged.
- **Search:** find foods by name or barcode, with recently used foods shown first.
- **Saved meals:** save combinations such as "egg and milk" and log them in one tap. You can also save a logged meal from the Today tab.
- **Barcode scanning:** save a barcode with a food, then scan it later to pick the food instantly.
- **Backup and restore:** export all data to a file or text, and import it later (merge or replace).
- **Storage cleanup:** delete logged entries from before today to free up space.

## Using it

1. **Foods tab:** add your foods with values per 100 g. Optionally add a serving size and a barcode.
2. **Log food tab:** search or scan a food, choose the meal and date, enter the amount and tap *Add to day*.
3. **Today tab:** see your totals, goal progress and each meal. Edit or delete entries here.
4. **Meals tab:** build or save meals you eat often, then log them in one tap.
5. **Settings tab:** set goals, export or import data, and free up storage.

## Deploy with GitHub Pages

1. Create a **public** repository.
2. Upload `index.html` (this file must have exactly that name).
3. Go to **Settings → Pages**, set the source to **Deploy from a branch**, choose `main` and `/ (root)`, and save.
4. After a minute or two your site is available at `https://YOUR-USERNAME.github.io/YOUR-REPO/`.
5. On iPhone, open the link in Safari, tap **Share → Add to Home Screen**.

## Your data and privacy

- All data is stored in your browser's local storage on your own device. Nothing is sent to a server.
- Data is **per browser and per web address**. It does not sync between devices, and a different address (for example, a new repository name) starts empty.
- Clearing Safari's website data erases it. **Export a backup regularly** from *Settings → Export data*.
- To move data between devices, versions or addresses, export from the old one and import into the new one. *Merge* adds to your existing data; *Replace all* overwrites it.
- Updating `index.html` on the same address keeps your data.

## Barcode scanning notes

- Live scanning needs camera permission, a secure (HTTPS) address and an internet connection to load the scanner library ([html5-qrcode](https://github.com/mebjas/html5-qrcode), loaded from jsDelivr).
- If the live camera is unavailable, use **Take a photo of the barcode**, or type the number.
- Barcodes only match foods you have saved. This app does not look up products online.

## Limitations

- Nutrition values are whatever you enter, so check them against the package.
- There is no cloud sync or multi-user support.
- Data lives in browser storage, which has a size limit and can be cleared by the browser.

## Tech

Plain HTML, CSS and JavaScript in one file. The only external dependency is the barcode scanner library mentioned above.
