# Prompt V1

Group: 9
Members: Fu Diyan
Date: 2026.10.12

---

## C — Context

I am an undergraduate completing a carbon-accounting course project. Build a personal carbon footprint calculator for a fictional Shanghai Jiao Tong University student. This student is a shared course case for the whole class, not a statistical description of all SJTU students.

## O — Objective

Build an interactive calculator that runs in a browser. It needs to:

- Accept activity data
- Estimate emissions in CO₂e
- Show the result and briefly explain what it means
- Give reduction suggestions tied to the activities entered

Activity data × emission factor gives each category’s emissions, which are then summed into a total. Numbers in the shared profile are the defaults. The user can change the inputs to compare different activity levels. Reset returns to Li Ming’s defaults.

## S — Style

Wizard: Use a step-by-step guide that splits the questions into sections such as transport, energy, food, and shopping, so the user is not faced with too many questions at once.

Dashboard: After the calculation, present the results on a dashboard or results page. Use several icons, and update the results as the inputs change.

Look and interaction: Keep the interface simple, with a dark theme, to reduce visual noise and meet accessibility expectations. Add a sticky live preview bar so the running total stays visible while the user fills in the options.

## T — Tone

Clear and concise. Analyze the result rationally and offer reduction suggestions.

## A — Audience

Both the user of the calculator and the person being accounted for are Li Ming. Use the shared facts below as the default inputs. Do not change these numbers. Do not write anything the profile does not give as a fact. If you add something, label it as an assumption.

### Shared facts

Identity: Li Ming, age 20, a second-year engineering student at Shanghai Jiao Tong University. He lives in a four-person dorm, spends most days on campus, and occasionally leaves campus or goes home to visit family. Time units differ across activities.

Travel:

- Walking or cycling on campus: about 20 km/week
- Metro: 2 one-way trips per week, 15 km each
- Ride-hailing: 2 one-way trips per month, 10 km each, usually alone

Food:

- 21 main meals per week: 3 beef or lamb, 8 other meat, 5 fish, eggs, dairy, or soy, and 5 mostly plant-based
- Most meals are eaten in the campus canteen
- About 2 takeaway meals per week are already included in these 21 meals. Do not count takeaway as extra meals

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

## R — Response

Return only one complete HTML file containing the HTML, CSS, and JavaScript. After it is saved, it must open directly in a browser. Do not split it into multiple files, and do not return only an explanation.

The page must include:

- An activity input area. Next to each input, state the time unit, matching the shared facts: per week, per month, last 30 days, or per teaching semester
- A calculate button and a reset button. Reset restores Li Ming’s defaults
- The total emissions, with the reporting period stated
- Emissions broken down by activity category
- A short explanation of how the result was produced, what the boundary includes and excludes, which numbers are shared facts, and which are group assumptions
- Reduction suggestions related to the current inputs
