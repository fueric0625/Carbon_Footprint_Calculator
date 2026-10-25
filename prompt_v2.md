# Prompt V2

Group: 9
Members: Fu Diyan
Date: 2026.10.12
AI tool: Cursor (Grok)


## C — Context

I am an undergraduate completing a carbon-accounting course project. Build a personal carbon footprint calculator for a fictional Shanghai Jiao Tong University student named Li Ming. He is a shared course case for the whole class, not a statistical description of all SJTU students.

This is an exploratory prototype for the course. Activity data in the shared profile are the default facts. Emission factors are placeholder values for the prototype. The page must label them as placeholders. Do not present them as verified official factors.

## O — Objective

Build an interactive web calculator that opens directly in a browser. It needs to:

- Accept activity data, with Li Ming’s shared facts filled in by default
- Estimate emissions in CO₂e
- Show the result and briefly explain what the number means, what it includes, and what it excludes
- Give reduction suggestions related to the current result

Method: first convert activity amounts to the same reporting period, then calculate activity data × emission factor, then add the quantified categories. The user can change the inputs to compare different activity levels. Reset returns to Li Ming’s defaults.

## S — Style

Use a step-by-step wizard. Do not put every question on one screen. Use five steps, in this order:

1. Transport: walking or cycling on campus, metro, ride-hailing, high-speed rail home
2. Energy: dorm electricity, hot showers
3. Food
4. Shopping: online parcels, clothing
5. Waste

Each step shows only that category’s inputs. The user can go back and edit an earlier step.

Keep the interface simple, with a dark theme, clear contrast between text and background, labeled inputs, and keyboard access. Give each category an icon.

While the form is being filled in, keep a sticky preview bar at the top or bottom. It always shows the current estimated total and updates as soon as an input changes.

After the last step is confirmed, open a results dashboard. The dashboard includes the total, a category comparison chart, a short explanation, and reduction suggestions. When the user goes back from the dashboard to edit inputs, the preview bar, chart, and suggestions update together.

## T — Tone

Concise and rational. Use short sentences for the questions. Lead with the number, then explain why. Reduction suggestions address only activities in the current estimate. Do not lecture, and do not use exaggerated encouragement.

## A — Audience

Both the user of the calculator and the person being accounted for are Li Ming. Use the shared facts below as the default inputs. Do not change these numbers. Do not write anything the profile does not give as a fact. On the page, label the assumptions below as “assumption” or “placeholder.”

### Shared facts

Identity: Li Ming, age 20, a second-year engineering student at Shanghai Jiao Tong University. He lives in a four-person dorm, spends most days on campus, and occasionally leaves campus or goes home to visit family.

Travel:

- Walking or cycling on campus: about 20 km/week
- Metro: 2 one-way trips per week, 15 km each
- Ride-hailing: 2 one-way trips per month, 10 km each, usually alone

Food:

- 21 main meals per week: 3 beef or lamb, 8 other meat, 5 fish, eggs, dairy, or soy, and 5 mostly plant-based
- Most meals are eaten in the campus canteen
- About 2 takeaway meals per week are already included in these 21 meals

Dorm and energy:

- Four people share one room
- Room electricity: 120 kWh over the last 30 days, for the whole room
- Hot showers: 6 per week, about 8 minutes each

Goods and parcels:

- Online shopping: 3 parcels/month
- Clothing: 2 items per teaching semester

Intercity travel:

- 2 round trips home by high-speed rail per teaching semester
- About 220 km one way

Waste:

- General waste: about 3 small bags/week
- Recyclable bottles or cans: about 3 per week

### Assumptions

Assumption 1: Results are reported per teaching semester. One semester is 18 weeks. Activities given per month are converted with 1 month = 4 weeks, so one semester is 4.5 months. Electricity for the last 30 days is not treated as one calendar month. One semester is 18 × 7 = 126 days.

This assumption is needed because the profile mixes weeks, months, 30-day windows, and teaching semesters. Those amounts cannot be added until they share one period. Neither 18 weeks nor “1 month = 4 weeks” is a fact from the profile.

Assumption 2: Dorm electricity is split equally among 4 people. Li Ming is assigned one quarter of the room’s electricity.

This assumption is needed because 120 kWh is the whole room, and the profile does not give his personal use.

### Record only, do not add to the total

The activities below appear in the inputs and in the results notes, but they are not multiplied by an emission factor and are not added to the total:

- Hot showers: only a count and a duration, with no energy type or amount
- Online parcels and clothing: only counts, with no material, price, packaging weight, or product lifetime
- General waste and recyclable bottles or cans: only bag and item counts, with no mass and no treatment pathway. The profile does not say whether the 3 small bags are personal or for the whole room. Do not divide by 4
- Takeaway packaging and delivery: the food itself is already in the 21 main meals. The profile gives no packaging weight or delivery distance

State on the page why each item is excluded.

## Accounting rules

Keep each input in the profile’s original time unit. Do not ask the user to convert. The program converts to per teaching semester using Assumption 1, then calculates.

Quantified activities use the placeholder factors below. The page must list each factor and its unit, and label them “placeholder factors, not facts from the shared profile”:

| Activity | Placeholder factor |
| --- | --- |
| Walking or cycling | 0 kg CO₂e/km |
| Metro | 0.04 kg CO₂e/passenger·km |
| Ride-hailing | 0.20 kg CO₂e/km |
| High-speed rail | 0.03 kg CO₂e/passenger·km |
| Beef or lamb | 6 kg CO₂e/meal |
| Other meat | 1.5 kg CO₂e/meal |
| Fish, eggs, dairy, or soy | 0.8 kg CO₂e/meal |
| Mostly plant-based | 0.4 kg CO₂e/meal |
| Electricity | 0.57 kg CO₂e/kWh |

Walking and cycling stay in the transport step. Their use-phase emissions are counted as 0, and the notes say so.

Ride-hailing defaults to traveling alone and is not divided by the number of passengers.

Food has only four meal-count inputs, defaulting to 3, 8, 5, and 5. Do not add a separate takeaway-meal input. Note beside them that about 2 takeaway meals per week are already included in these main meals.

The electricity input defaults to the room total, 120 kWh / 30 days. The results show both the room total and Li Ming’s share under Assumption 2. Only his share is added to the total.

The total is the sum of the quantified categories, in kg CO₂e per teaching semester. Transport, energy, and food each have a subtotal. Unquantified activities are listed separately, below the total.

Each activity is counted only once.

## R — Response

Return only one complete HTML file containing the HTML, CSS, and JavaScript. After it is saved, it must open directly in a browser. Do not split it into multiple files, do not reference external images, fonts, or libraries, and do not return only an implementation note.

The page includes:

- Five steps of activity inputs. Each input states its time unit
- A sticky preview bar showing the current total
- A calculate button and a reset button. Reset restores all of Li Ming’s defaults
- A results dashboard: the total, a category comparison chart with icons, and category subtotals
- A short explanation: the reporting period, the conversion assumptions, the electricity split, the placeholder factors, which categories are in the total, which activities are excluded, and that takeaway is already included in the 21 meals
- At most three reduction suggestions. Each one points to a quantified activity that is currently high, and states how the estimate would change if that activity were reduced or replaced

Use English for all interface text.
