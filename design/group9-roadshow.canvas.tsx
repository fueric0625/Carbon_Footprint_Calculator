import {
  BarChart,
  Callout,
  Divider,
  Grid,
  H1,
  H2,
  H3,
  Pill,
  Row,
  Stack,
  Stat,
  Table,
  Text,
  UsageBar,
} from "cursor/canvas";

export default function Group9Roadshow() {
  return (
    <Stack gap={24}>
      <Stack gap={6}>
        <H1>Group 9 roadshow</H1>
        <Text tone="secondary">
          Final calculator, Li Ming, one teaching semester. Default result
          checked in the browser on 9 Nov 2026. The demo is scored on whether
          the audience can see a client need, a product response, and one
          reviewed revision.
        </Text>
      </Stack>

      <Grid columns={4} gap={12}>
        <Stat value="8 min" label="Hard cap, aim for 7:30" />
        <Stat value="783.7 kg" label="Reported total at 18 weeks" />
        <Stat value="96.1 kg" label="Sourced CO2: electricity + rail" tone="info" />
        <Stat value="687.6 kg" label="Unverified CO2e, mostly food" tone="warning" />
      </Grid>

      <Callout tone="warning" title="Say this before anyone asks">
        Food, metro, and ride-hailing factors are still marked “not yet
        verified.” Beef or lamb is 324 kg only because the factor is 6 kg per
        meal and the profile gives no meal weight. The comparison is
        illustrative. Do not present it as a verified ranking.
      </Callout>

      <H2>Seven and a half minutes</H2>
      <Text tone="secondary">
        Three speakers. The calculator page carries the middle five minutes.
        Slides only frame the opening and the one revision.
      </Text>
      <Table
        headers={["Time", "Beat", "What the audience should hear", "Score it serves"]}
        columnAlign={["left", "left", "left", "left"]}
        rows={[
          [
            "0:00–1:00",
            "Introduction",
            "Li Ming needs a semester result that shows what is counted, what is left out, and which number he can change. The calculator keeps his shared facts and labels the 18-week assumption and the mixed units.",
            "Client needs, 20",
          ],
          [
            "1:00–2:00",
            "Open on defaults",
            "Do not retype the profile. Point at the banner, then Transport: metro is trips times kilometres, ride-hailing is monthly and traveled alone, high-speed rail is already per semester.",
            "Demo, 30",
          ],
          [
            "2:00–3:30",
            "One live change",
            "Energy. Weeks is an assumption, default 18. Room electricity is 120 kWh for four people. Showers are recorded and excluded. Change 18 to 16: metro falls, rail stays 880 km. Reset back to 18.",
            "Demo and functionality",
          ],
          [
            "3:30–5:30",
            "Read the result",
            "783.7 kg reported, not a complete CO2e total. Sourced 96.1 kg CO2 against unverified 687.6 kg CO2e. Food is 648 kg. Read the beef suggestion through the word “illustrative,” then the electricity suggestion in kg CO2.",
            "Results, 20; credibility, 20",
          ],
          [
            "5:30–6:00",
            "What is left out",
            "One sentence on showers, parcels, clothing, and waste: counted on the page, absent from the total, because the profile has no energy, mass, or material.",
            "Transparency, 20",
          ],
          [
            "6:00–7:30",
            "One revision",
            "Prototype 1 called the headline kg CO2e. Electricity and rail are sourced CO2; the food factors are unverified per meal. The final page splits the units and marks those suggestions illustrative. Remaining limit: three factors still have no source.",
            "Reflection, 20",
          ],
        ]}
        rowTone={["info", "neutral", "success", "warning", "neutral", "info"]}
      />

      <H2>Default result to memorize</H2>
      <Grid columns={2} gap={20}>
        <Stack gap={8}>
          <H3>Reported kilograms at 18 weeks</H3>
          <BarChart
            categories={["Food", "Electricity", "Metro", "Ride-hailing", "High-speed rail", "Walking"]}
            series={[{ name: "kg reported per teaching semester", data: [648, 72.3, 21.6, 18, 23.8, 0] }]}
            height={220}
            valueSuffix=" kg"
            showValues
          />
          <Text tone="tertiary" size="small">
            Source: Group9_Final_Calculator.html with Li Ming’s defaults and 18 weeks. Walking is 360 km and 0 kg. Rounded to 0.1 kg.
          </Text>
        </Stack>
        <Stack gap={12}>
          <H3>Two units inside the 783.7 kg</H3>
          <UsageBar
            total={783.7}
            segments={[
              { id: "sourced", value: 96.1 },
              { id: "unverified", value: 687.6 },
            ]}
            topLeftLabel="Sourced CO2, 96.1 kg"
            topRightLabel="Unverified CO2e, 687.6 kg"
          />
          <Text>
            Electricity 72.3 kg uses 0.5737 kg CO2/kWh, Shanghai 2023, Announcement 2025 No. 47. High-speed rail 23.8 kg uses 0.02709 kg CO2 per passenger-kilometre, China 2019 operation phase.
          </Text>
          <Text tone="secondary">
            At 16 weeks the total falls to 699.3 kg, metro to 480 km, beef meals from 54 to 48. Rail stays 880 km. Reset returns 18 weeks and 783.7 kg.
          </Text>
        </Stack>
      </Grid>

      <Divider />

      <H2>Answers worth rehearsing</H2>
      <Table
        headers={["If asked", "Answer in one breath"]}
        rows={[
          [
            "Why 0.5737, not the class example 0.4701?",
            "The in-class sheet uses the Shanghai 2024 grid factor, 0.4701 kg CO2e/kWh. This file uses the 2023 Shanghai provincial factor, 0.5737 kg CO2/kWh, from the 2025 No. 47 announcement. The source says CO2, so the page does not relabel it CO2e.",
          ],
          [
            "Why not multiply by 52?",
            "The profile mixes weeks, months, 30 days, and a teaching semester. The result is one semester. Eighteen weeks is an assumption. One month is counted as four weeks. Rail and clothing are already per semester, so they are not scaled.",
          ],
          [
            "Why is food most of the total?",
            "The per-meal factors are unverified and have no meal weight. Three beef or lamb meals a week become 54 meals and 324 kg. That ranking is illustrative.",
          ],
          [
            "Why leave out showers and waste?",
            "The profile gives counts, not energy, mass, or treatment. Those rows stay visible and stay out of the total.",
          ],
          [
            "Is 120 kWh Li Ming’s own use?",
            "No. It is the whole room over 30 days. His share is one quarter, scaled to the semester length.",
          ],
          [
            "Is a battery car always lower-carbon?",
            "Only if asked. In the BMW sheets, iX5 production is 18.1 t CO2e against 11.7 t for the diesel X5. Over 200,000 km on the European mix, iX5 is 31.1 t and X5 is 58.3 t. Renewable charging drops iX5 use from 12.1 t to 0.8 t. That case is not an input to this calculator.",
          ],
        ]}
        rowTone={["warning", "info", "warning", "neutral", "neutral", "neutral"]}
      />

      <Row gap={8} align="center">
        <Pill tone="warning" active>Credibility risk</Pill>
        <Text tone="secondary">
          The Revisit 1 sheet says every factor should have a source before the final calculator. Three still do not. Disclosure is the current defense.
        </Text>
      </Row>
    </Stack>
  );
}
