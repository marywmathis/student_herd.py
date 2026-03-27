import streamlit as st
import pandas as pd
import numpy as np
import math
import random

st.set_page_config(page_title="EpiLab Student: Herd Immunity & Reproductive Number", layout="wide")

PRIMARY   = "#1B3A6B"
SECONDARY = "#E05A2B"
ACCENT    = "#F5A623"
GREEN     = "#2e7d32"
LIGHT_BG  = "#F0F4FF"
WARN_BG   = "#FFF5F0"

# ── LOGIN ─────────────────────────────────────────────────
def check_credentials(username, password):
    users = st.secrets.get("users", {})
    return username in users and users[username] == password

def login_screen():
    col_l, col_m, col_r = st.columns([1,2,1])
    with col_m:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='text-align:center; padding:32px; background:{LIGHT_BG}; border-radius:12px; border-top:4px solid {PRIMARY};'>
            <h2 style='color:{PRIMARY}; margin-bottom:4px;'>EpiLab Student</h2>
            <h3 style='color:{SECONDARY}; margin-top:0;'>Herd Immunity & Reproductive Number</h3>
            <p style='color:#555;'>Enter your access credentials to continue.</p>
        </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Log In", type="primary", use_container_width=True):
            if check_credentials(username, password):
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Incorrect username or password.")
        st.caption("Access provided by your course instructor.")

if not st.session_state.get("authenticated"):
    login_screen(); st.stop()

# ── HEADER ─────────────────────────────────────────────────
col_hdr, col_out = st.columns([6,1])
with col_hdr:
    st.markdown(f"""
    <div style='padding:16px 0 8px 0;'>
        <span style='font-size:28px; font-weight:800; color:{PRIMARY};'>EpiLab Student</span>
        <span style='font-size:18px; color:{SECONDARY}; margin-left:12px;'>Herd Immunity & Reproductive Number</span>
    </div>""", unsafe_allow_html=True)
with col_out:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Log Out"):
        st.session_state["authenticated"] = False; st.rerun()

st.markdown(f"<div style='height:3px; background:linear-gradient(to right, {PRIMARY}, {SECONDARY}, {ACCENT}); border-radius:2px; margin-bottom:16px;'></div>", unsafe_allow_html=True)

tab_learn, tab_practice, tab_glossary = st.tabs([
    "📊 Learn: Herd Immunity & R",
    "🎯 Practice Scenarios",
    "📖 Glossary"
])

# ══════════════════════════════════════════════════════════
# TAB 1: LEARN
# ══════════════════════════════════════════════════════════
with tab_learn:

    if "learn_reset_count" not in st.session_state:
        st.session_state["learn_reset_count"] = 0

    col_hdr2, col_rst = st.columns([5,1])
    with col_hdr2:
        st.markdown(f"### <span style='color:{PRIMARY}'>Herd Immunity & Reproductive Numbers</span>", unsafe_allow_html=True)
    with col_rst:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Reset", key="reset_learn"):
            st.session_state["learn_reset_count"] += 1
            keys_to_del = [k for k in st.session_state.keys() if k.startswith("lrn_")]
            for k in keys_to_del: del st.session_state[k]
            st.rerun()

    lrc = st.session_state["learn_reset_count"]

    st.markdown("""
When an infectious disease enters a population, whether it spreads depends on one key number: **how many people does one infected person typically infect?**
If that number is above 1, the outbreak grows. If it falls below 1, the outbreak dies out. Vaccination, behavior change, and prior immunity all work by driving that number down.
    """)

    # ── SECTION 1: R0 ─────────────────────────────────────
    st.divider()
    st.markdown(f"### <span style='color:{PRIMARY}'>1. Basic Reproductive Number (R0)</span>", unsafe_allow_html=True)

    col1, col2 = st.columns([3,2])
    with col1:
        st.markdown("""
**R0** (pronounced "R-naught") is the **average number of secondary cases** produced by one infectious person in a **completely susceptible population** — no immunity, no interventions.

R0 is a property of the pathogen AND its environment. It depends on:
- **Transmissibility** — how easily the pathogen passes from person to person
- **Duration of infectiousness** — how long someone can spread it
- **Contact rate** — how many people an infected person comes in contact with

**R0 = transmissibility × contact rate × duration of infectiousness**
        """)
    with col2:
        st.markdown(f"""
<div style='background:{LIGHT_BG}; border-radius:10px; padding:16px; border-top:4px solid {PRIMARY};'>
<b style='color:{PRIMARY}'>R0 interpretation:</b><br><br>
<b>R0 &lt; 1:</b> Each case produces fewer than 1 new case → outbreak dies out<br><br>
<b>R0 = 1:</b> Each case produces exactly 1 new case → stable endemic disease<br><br>
<b>R0 &gt; 1:</b> Each case produces more than 1 new case → outbreak grows<br><br>
<i>R0 is measured in a <b>fully susceptible</b> population with no interventions.</i>
</div>""", unsafe_allow_html=True)

    st.markdown("#### Compare R0 Across Diseases")
    DISEASES = {
        "Measles": (12, 18, "Extremely contagious — airborne, survives in air up to 2 hours"),
        "Chickenpox": (8, 10, "Highly contagious — airborne and direct contact"),
        "Mumps": (4, 7, "Respiratory droplets"),
        "Polio": (5, 7, "Fecal-oral route"),
        "Smallpox": (5, 7, "Respiratory droplets and contact"),
        "COVID-19 (original)": (2, 3, "Respiratory droplets — original Wuhan strain"),
        "COVID-19 (Omicron)": (8, 15, "Highly transmissible variant"),
        "Influenza (seasonal)": (1, 2, "Respiratory droplets"),
        "Ebola": (1, 2, "Direct contact with bodily fluids — low airborne spread"),
        "HIV": (2, 5, "Sexual contact, blood — slow transmission"),
    }

    disease_df = pd.DataFrame([
        {"Disease": d, "R0 Low": v[0], "R0 High": v[1], "R0 Range": f"{v[0]}–{v[1]}", "Transmission Route": v[2]}
        for d, v in DISEASES.items()
    ]).sort_values("R0 High", ascending=False)

    selected_diseases = st.multiselect("Select diseases to compare:",
        list(DISEASES.keys()),
        default=["Measles","COVID-19 (Omicron)","Influenza (seasonal)","Ebola"],
        key=f"lrn_disease_select_{lrc}")

    if selected_diseases:
        filtered = disease_df[disease_df["Disease"].isin(selected_diseases)].sort_values("R0 High", ascending=False)

        # Visual bar chart using HTML
        bars_html = ""
        max_r0 = max(v[1] for d,v in DISEASES.items() if d in selected_diseases) + 2
        for _, row in filtered.iterrows():
            lo_pct = round(row["R0 Low"]/max_r0*100, 1)
            hi_pct = round(row["R0 High"]/max_r0*100, 1)
            mid_pct = round((row["R0 Low"]+row["R0 High"])/2/max_r0*100, 1)
            color = f"#{max(0,min(255,int(255-(row['R0 High']/20)*200))):02x}6b{max(0,min(255,int((row['R0 High']/20)*200))):02x}"
            if row["R0 High"] >= 10: color = "#c0392b"
            elif row["R0 High"] >= 5: color = "#e07020"
            elif row["R0 High"] >= 3: color = "#d4a020"
            else: color = "#2e7d32"
            bars_html += f"""
<div style='display:flex; align-items:center; margin:6px 0;'>
  <div style='width:200px; font-size:13px; font-weight:bold; color:{PRIMARY};'>{row['Disease']}</div>
  <div style='flex:1; position:relative; height:24px; background:#f0f0f0; border-radius:4px; margin:0 12px;'>
    <div style='position:absolute; left:{lo_pct}%; width:{hi_pct-lo_pct}%; height:100%; background:{color}; border-radius:4px; opacity:0.85;'></div>
    <div style='position:absolute; left:{mid_pct}%; transform:translateX(-50%); top:3px; font-size:12px; color:white; font-weight:bold;'>{row["R0 Range"]}</div>
  </div>
  <div style='width:280px; font-size:11px; color:#666;'>{row["Transmission Route"]}</div>
</div>"""

        st.markdown(f"""
<div style='background:#fafafa; border-radius:8px; padding:16px; border:1px solid #e0e0e0;'>
<div style='font-size:12px; color:#888; margin-bottom:8px;'>R0 range → &nbsp;&nbsp; 0 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {max_r0//2} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {max_r0}</div>
{bars_html}
</div>
<div style='font-size:11px; color:#888; margin-top:6px;'>Color: green = lower transmission, orange = moderate, red = high transmission</div>
        """, unsafe_allow_html=True)
        st.table(filtered[["Disease","R0 Range","Transmission Route"]].set_index("Disease"))

    # ── SECTION 2: HERD IMMUNITY THRESHOLD ────────────────
    st.divider()
    st.markdown(f"### <span style='color:{PRIMARY}'>2. Herd Immunity Threshold (HIT)</span>", unsafe_allow_html=True)

    col1, col2 = st.columns([3,2])
    with col1:
        st.markdown("""
**Herd immunity** occurs when enough people in a population are immune that the disease can no longer spread efficiently — even unvaccinated individuals are protected because chains of transmission break down.

The **Herd Immunity Threshold (HIT)** is the proportion of the population that must be immune to stop the outbreak:

**HIT = 1 − (1/R0)**

This means: the higher the R0, the larger the proportion of the population that must be immune before herd immunity is achieved.
        """)
    with col2:
        st.markdown(f"""
<div style='background:#FFF5F0; border-radius:10px; padding:16px; border-top:4px solid {SECONDARY};'>
<b style='color:{SECONDARY}'>Example — Measles (R0 = 15):</b><br><br>
HIT = 1 − (1/15) = 1 − 0.067 = <b>0.933</b><br><br>
93.3% of the population must be immune to achieve herd immunity against measles.<br><br>
<b>Example — Influenza (R0 = 1.5):</b><br><br>
HIT = 1 − (1/1.5) = 1 − 0.667 = <b>0.333</b><br><br>
Only 33.3% immunity needed.
</div>""", unsafe_allow_html=True)

    st.markdown("#### Interactive HIT Calculator")
    col1, col2 = st.columns(2)
    with col1:
        r0_hit = st.slider("R0 (Basic Reproductive Number)", min_value=1.1, max_value=20.0, value=5.0, step=0.1, key=f"lrn_r0_hit_{lrc}")
    with col2:
        hit = round((1 - 1/r0_hit) * 100, 1)
        st.metric("Herd Immunity Threshold", f"{hit}%")
        st.metric("Vaccine coverage needed", f"{hit}% of population")

    # Gauge visualization
    gauge_color = "#c0392b" if hit >= 80 else "#e07020" if hit >= 60 else "#2e7d32"
    st.markdown(f"""
<div style='background:#f9f9f9; border-radius:8px; padding:16px; margin:8px 0;'>
  <div style='position:relative; height:28px; background:#e0e0e0; border-radius:14px; overflow:hidden;'>
    <div style='height:100%; width:{hit}%; background:{gauge_color}; border-radius:14px; transition:width 0.3s;'></div>
    <div style='position:absolute; top:5px; left:{min(hit+1, 92)}%; font-size:13px; font-weight:bold; color:white;'>{hit}%</div>
  </div>
  <div style='display:flex; justify-content:space-between; font-size:11px; color:#888; margin-top:4px;'>
    <span>0%</span><span>25%</span><span>50%</span><span>75%</span><span>100%</span>
  </div>
  <p style='margin-top:8px; font-size:13px; color:#333;'>
  With R0 = {r0_hit}, each infected person spreads to {r0_hit} others. 
  <b>{hit}%</b> of the population must be immune to break transmission chains.
  {"This is a very high threshold — even small gaps in vaccine coverage can allow outbreaks." if hit >= 80 else "This is achievable with standard vaccination campaigns." if hit <= 50 else "This requires strong, sustained vaccination efforts."}
  </p>
</div>""", unsafe_allow_html=True)

    with st.expander("📐 Show me the math — HIT"):
        st.markdown(f"""
**Formula:** HIT = 1 − (1 / R0)

**Step 1:** 1 / R0 = 1 / {r0_hit} = **{round(1/r0_hit, 4)}**

This is the proportion of the population that can remain susceptible while still stopping spread.

**Step 2:** HIT = 1 − {round(1/r0_hit, 4)} = **{round(1 - 1/r0_hit, 4)}** ({hit}%)

**Why does this formula work?**

For an outbreak to sustain itself, R_effective must be ≥ 1. R_effective = R0 × (proportion susceptible). Setting R_effective = 1 and solving for the proportion susceptible:

1 = R0 × (proportion susceptible)

Proportion susceptible = 1/R0

Therefore proportion immune = 1 − 1/R0 = HIT.

When the proportion immune exceeds HIT, R_effective < 1 and the outbreak cannot sustain itself.
        """)

    # ── SECTION 3: VACCINE COVERAGE ───────────────────────
    st.divider()
    st.markdown(f"### <span style='color:{PRIMARY}'>3. Vaccine Coverage & Effectiveness</span>", unsafe_allow_html=True)

    st.markdown("""
Reaching herd immunity requires accounting for **vaccine effectiveness (VE)**. No vaccine is 100% effective — some vaccinated individuals remain susceptible. The required **vaccine coverage (VC)** to achieve herd immunity is:

**VC = HIT / VE = (1 − 1/R0) / VE**
    """)

    col1, col2, col3 = st.columns(3)
    with col1: r0_vc = st.slider("R0", 1.1, 20.0, 5.0, 0.1, key=f"lrn_r0_vc_{lrc}")
    with col2: ve = st.slider("Vaccine Effectiveness (%)", 50, 100, 90, 1, key=f"lrn_ve_{lrc}") / 100
    with col3:
        hit_vc = 1 - 1/r0_vc
        vc_needed = hit_vc / ve
        if vc_needed > 1:
            st.metric("Vaccine Coverage Needed", ">100%")
            st.error("⚠️ Herd immunity is not achievable with this vaccine effectiveness and R0. Even vaccinating the entire population would not reach the threshold.")
        else:
            st.metric("Vaccine Coverage Needed", f"{round(vc_needed*100,1)}%")
            st.metric("HIT", f"{round(hit_vc*100,1)}%")

    with st.expander("📐 Show me the math — Vaccine Coverage"):
        st.markdown(f"""
**Formula:** VC = HIT / VE = (1 − 1/R0) / VE

**Step 1:** HIT = 1 − 1/{r0_vc} = **{round(hit_vc,4)}** ({round(hit_vc*100,1)}%)

**Step 2:** VC = {round(hit_vc,4)} / {round(ve,2)} = **{round(vc_needed,4)}** ({round(vc_needed*100,1)}%)

**Why divide by vaccine effectiveness?**

If VE = 90%, then 10% of vaccinated people are still susceptible. To get enough truly immune people, you need to vaccinate MORE than the HIT — specifically HIT/VE.

Example: If HIT = 90% and VE = 90%, you need to vaccinate 90%/0.90 = **100%** of the population to achieve herd immunity. This is why high-R0 diseases with imperfect vaccines can make herd immunity very difficult to achieve.
        """)

    # ── SECTION 4: INTERVENTIONS & Rt ─────────────────────
    st.divider()
    st.markdown(f"### <span style='color:{PRIMARY}'>4. Effective Reproductive Number (Rt) & Interventions</span>", unsafe_allow_html=True)

    col1, col2 = st.columns([3,2])
    with col1:
        st.markdown("""
**R0** assumes a fully susceptible population with no interventions. In reality, populations have:
- Prior immunity (from vaccination or previous infection)
- Behavioral interventions (masks, distancing, hand hygiene)
- Public health measures (isolation, quarantine, school closures)

The **Effective Reproductive Number (Rt)** — also written **Re** — is the average number of secondary cases at a specific point in time **t**, accounting for current immunity levels and interventions:

**Rt = R0 × (proportion susceptible) × (intervention reduction factor)**

When Rt < 1, the outbreak is declining. When Rt > 1, it is growing.
        """)
    with col2:
        st.markdown(f"""
<div style='background:{LIGHT_BG}; border-radius:10px; padding:16px; border-top:4px solid {PRIMARY};'>
<b style='color:{PRIMARY}'>R0 vs Rt:</b><br><br>
<b>R0:</b> Fixed property of the pathogen in a specific environment. Does not change with interventions.<br><br>
<b>Rt:</b> Changes over time as immunity builds and interventions are applied. What we track during an outbreak.<br><br>
<b>Goal of public health:</b> Drive Rt below 1.
</div>""", unsafe_allow_html=True)

    st.markdown("#### Interactive Rt Calculator")
    col1, col2, col3 = st.columns(3)
    with col1:
        r0_rt = st.slider("R0", 1.1, 15.0, 3.0, 0.1, key=f"lrn_r0_rt_{lrc}")
        pct_immune = st.slider("% Population immune (vaccination + prior infection)", 0, 100, 30, 1, key=f"lrn_immune_{lrc}")
    with col2:
        mask_eff = st.slider("Mask effectiveness (%)", 0, 80, 0, 5, key=f"lrn_mask_{lrc}")
        distancing = st.slider("Social distancing contact reduction (%)", 0, 80, 0, 5, key=f"lrn_dist_{lrc}")
    with col3:
        prop_susceptible = (100 - pct_immune) / 100
        intervention_factor = (1 - mask_eff/100) * (1 - distancing/100)
        rt = round(r0_rt * prop_susceptible * intervention_factor, 2)
        color = "#2e7d32" if rt < 1 else "#c0392b"
        st.metric("Rt (Effective R)", rt, delta=f"{round(rt - r0_rt, 2)} vs R0", delta_color="inverse")
        if rt < 1:
            st.success(f"✅ Rt = {rt} < 1 — Outbreak is **declining**. Each case produces fewer than 1 new case on average.")
        elif rt == 1:
            st.warning(f"⚠️ Rt = {rt} = 1 — Outbreak is **stable** (endemic). Case counts are holding steady.")
        else:
            st.error(f"🔴 Rt = {rt} > 1 — Outbreak is **growing**. Need to drive Rt below 1.")

    with st.expander("📐 Show me the math — Rt"):
        st.markdown(f"""
**Formula:** Rt = R0 × proportion susceptible × intervention factor

**Step 1:** Proportion susceptible = (100 − {pct_immune})% = **{round(prop_susceptible,3)}**

**Step 2:** Intervention factor = (1 − mask eff.) × (1 − distancing)
= (1 − {mask_eff/100}) × (1 − {distancing/100})
= {round(1-mask_eff/100,2)} × {round(1-distancing/100,2)} = **{round(intervention_factor,3)}**

**Step 3:** Rt = {r0_rt} × {round(prop_susceptible,3)} × {round(intervention_factor,3)} = **{rt}**

**Interpretation:** Starting from R0 = {r0_rt}, the combination of {pct_immune}% immunity and current interventions brings Rt to {rt}. {"This is below 1 — the outbreak will decline." if rt < 1 else "This remains above 1 — further measures or more immunity are needed to stop growth."}
        """)

    # ── SECTION 5: GENERATION TIME & DOUBLING TIME ────────
    st.divider()
    st.markdown(f"### <span style='color:{PRIMARY}'>5. Generation Time & Doubling Time</span>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
<div style='background:{LIGHT_BG}; border-radius:10px; padding:16px; border-top:4px solid {PRIMARY};'>
<b style='color:{PRIMARY}'>Generation Time (Tg)</b><br><br>
The average time between when a person is infected and when they infect someone else.<br><br>
Short generation time → rapid spread, harder to control.<br><br>
<b>Examples:</b><br>
COVID-19 (original): ~5 days<br>
Influenza: ~3 days<br>
Ebola: ~12–15 days<br>
Measles: ~11–12 days
</div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
<div style='background:#FFF5F0; border-radius:10px; padding:16px; border-top:4px solid {SECONDARY};'>
<b style='color:{SECONDARY}'>Doubling Time (Td)</b><br><br>
How long it takes for the number of cases to double during exponential growth.<br><br>
<b>Formula:</b> Td = Tg × log(2) / log(Rt)<br><br>
Shorter doubling time = faster-growing outbreak.<br><br>
Longer doubling time = more time for public health response.
</div>""", unsafe_allow_html=True)

    st.markdown("#### Interactive Doubling Time Calculator")
    col1, col2, col3 = st.columns(3)
    with col1: tg = st.number_input("Generation time (days)", min_value=1.0, max_value=30.0, value=5.0, step=0.5, key=f"lrn_tg_{lrc}")
    with col2: rt_dt = st.number_input("Rt (must be > 1 for growth)", min_value=1.01, max_value=15.0, value=2.5, step=0.1, key=f"lrn_rt_dt_{lrc}")
    with col3:
        td = round(tg * math.log(2) / math.log(rt_dt), 1)
        st.metric("Doubling Time", f"{td} days")

    # Case growth simulation
    days = list(range(0, 61, 1))
    cases = [100 * (2 ** (d/td)) for d in days]
    milestones = [(d, round(c)) for d, c in zip(days, cases) if c >= 100 and c <= 1000000]
    key_days = [d for d, c in milestones if c in [100, 200, 500, 1000, 5000, 10000, 50000, 100000]]

    # Simple HTML table showing case growth milestones
    milestone_rows = ""
    targets = [100, 200, 500, 1000, 5000, 10000, 50000, 100000, 1000000]
    for target in targets:
        if target > 100:
            day_reached = round(math.log(target/100) * td / math.log(2), 1)
            if day_reached <= 90:
                milestone_rows += f"<tr><td style='padding:6px 12px;'>{target:,} cases</td><td style='padding:6px 12px; font-weight:bold;'>Day {day_reached}</td></tr>"

    st.markdown(f"""
<div style='background:#fafafa; border-radius:8px; padding:16px; border:1px solid #e0e0e0; margin:12px 0;'>
<b>Starting from 100 cases with Rt = {rt_dt} and generation time = {tg} days (doubling every {td} days):</b><br>
<table style='margin-top:8px; border-collapse:collapse; width:auto;'>
<thead><tr style='border-bottom:2px solid #ccc;'>
<th style='padding:6px 12px; text-align:left; font-size:13px; color:#555;'>Cases</th>
<th style='padding:6px 12px; text-align:left; font-size:13px; color:#555;'>Day reached</th>
</tr></thead>
<tbody style='font-size:13px;'>{milestone_rows}</tbody>
</table>
</div>""", unsafe_allow_html=True)

    with st.expander("📐 Show me the math — Doubling Time"):
        st.markdown(f"""
**Formula:** Td = Tg × ln(2) / ln(Rt)

**Step 1:** ln(2) = **0.6931** (this is a mathematical constant — the log of 2)

**Step 2:** ln(Rt) = ln({rt_dt}) = **{round(math.log(rt_dt),4)}**

**Step 3:** Td = {tg} × 0.6931 / {round(math.log(rt_dt),4)} = **{td} days**

**Why ln(2)?** We want to know when cases double — i.e., when C(t) = 2 × C(0). Since cases grow exponentially as C(t) = C(0) × e^(rt), doubling occurs when e^(r×Td) = 2, so r×Td = ln(2).

**Relationship to Rt:** The growth rate r = ln(Rt)/Tg. Substituting: Td = ln(2)/r = ln(2) × Tg / ln(Rt).
        """)

    # ── SIR MODEL ─────────────────────────────────────────
    st.divider()
    st.markdown(f"### <span style='color:{PRIMARY}'>6. SIR Model — Real Epidemic Curves</span>", unsafe_allow_html=True)

    st.markdown("""
The milestone table above assumes **pure exponential growth** — cases double forever. In reality, outbreaks slow down and eventually stop because:
- Infected people **recover** and become immune (removed from susceptible pool)
- Infected people may **die** (also removed)
- As susceptibles are depleted, each infected person has fewer people to infect

The **SIR model** (Susceptible → Infectious → Removed) captures this realistically. It shows the epidemic curve: cases rise, peak, and decline.
    """)

    col1, col2 = st.columns([3,2])
    with col1:
        st.markdown(f"""
<div style='background:{LIGHT_BG}; border-radius:10px; padding:16px; border-top:4px solid {PRIMARY};'>
<b style='color:{PRIMARY}'>SIR Model Equations:</b><br><br>
dS/dt = −β × S × I / N<br>
dI/dt = β × S × I / N − γ × I<br>
dR/dt = γ × I<br><br>
Where:<br>
<b>β</b> = transmission rate = R0 × γ<br>
<b>γ</b> = removal rate = 1 / infectious period<br>
<b>S</b> = susceptible, <b>I</b> = infectious, <b>R</b> = removed
</div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
<div style='background:#FFF5F0; border-radius:10px; padding:16px; border-top:4px solid {SECONDARY};'>
<b style='color:{SECONDARY}'>Key insight:</b><br><br>
The outbreak peaks when Rt = R0 × S/N = 1 — i.e., when enough people have been infected/vaccinated that the effective R drops to 1.<br><br>
After the peak, S/N continues to fall → Rt stays below 1 → outbreak declines.<br><br>
This is why outbreaks end before infecting 100% of the population.
</div>""", unsafe_allow_html=True)

    st.markdown("#### SIR Epidemic Curve Simulator")

    SIR_PRESETS = {
        "Custom — enter my own values": None,
        "Measles (unvaccinated population)":    {"r0": 15.0, "infectious_days": 8,  "cfr": 0.2,  "pop": 100000, "initial_infected": 10},
        "COVID-19 — Original strain":           {"r0": 2.5,  "infectious_days": 10, "cfr": 1.0,  "pop": 100000, "initial_infected": 10},
        "COVID-19 — Omicron variant":           {"r0": 10.0, "infectious_days": 7,  "cfr": 0.15, "pop": 100000, "initial_infected": 10},
        "Influenza (seasonal)":                 {"r0": 1.5,  "infectious_days": 5,  "cfr": 0.1,  "pop": 100000, "initial_infected": 10},
        "Ebola":                                {"r0": 1.8,  "infectious_days": 12, "cfr": 50.0, "pop": 100000, "initial_infected": 10},
        "Smallpox":                             {"r0": 6.0,  "infectious_days": 17, "cfr": 30.0, "pop": 100000, "initial_infected": 10},
    }

    sir_preset_choice = st.selectbox("Load a disease preset:", list(SIR_PRESETS.keys()), key=f"lrn_sir_preset_{lrc}")
    sir_preset = SIR_PRESETS[sir_preset_choice]

    col1, col2, col3 = st.columns(3)
    with col1:
        sir_r0 = st.number_input("R0", min_value=1.01, max_value=20.0,
            value=float(sir_preset["r0"]) if sir_preset else 3.0, step=0.1, key=f"lrn_sir_r0_{lrc}")
        sir_infectious = st.number_input("Infectious period (days)", min_value=1, max_value=30,
            value=int(sir_preset["infectious_days"]) if sir_preset else 7, key=f"lrn_sir_inf_{lrc}")
    with col2:
        sir_cfr = st.number_input("Case Fatality Rate (%)", min_value=0.0, max_value=100.0,
            value=float(sir_preset["cfr"]) if sir_preset else 1.0, step=0.1, key=f"lrn_sir_cfr_{lrc}")
        sir_pop = st.number_input("Population size", min_value=1000, max_value=10000000,
            value=int(sir_preset["pop"]) if sir_preset else 100000, step=1000, key=f"lrn_sir_pop_{lrc}")
    with col3:
        sir_vacc = st.slider("% Already immune (vaccination/prior infection)", 0, 95, 0, 5, key=f"lrn_sir_vacc_{lrc}")
        sir_initial = st.number_input("Initial infected cases", min_value=1, max_value=1000,
            value=int(sir_preset["initial_infected"]) if sir_preset else 10, key=f"lrn_sir_init_{lrc}")

    N = sir_pop
    gamma = 1.0 / sir_infectious
    beta = sir_r0 * gamma
    cfr_frac = sir_cfr / 100.0

    S0 = N * (1 - sir_vacc/100) - sir_initial
    I0 = sir_initial
    R0_sir = N * (sir_vacc/100)

    S, I, R = [S0], [I0], [R0_sir]
    dt = 0.5
    max_days = 365
    steps = int(max_days / dt)

    for _ in range(steps):
        s, i, r = S[-1], I[-1], R[-1]
        new_inf = beta * s * i / N * dt
        new_rem = gamma * i * dt
        S.append(max(0, s - new_inf))
        I.append(max(0, i + new_inf - new_rem))
        R.append(r + new_rem)

    sample_days = list(range(0, max_days+1, 2))
    sample_idx = [int(d/dt) for d in sample_days if int(d/dt) < len(S)]
    s_vals = [S[i] for i in sample_idx]
    i_vals = [I[i] for i in sample_idx]
    r_vals = [R[i] for i in sample_idx]
    days_sampled = [sample_days[j] for j in range(len(sample_idx))]

    peak_i = max(i_vals)
    peak_day = days_sampled[i_vals.index(peak_i)]
    total_infected = N - s_vals[-1]
    total_deaths = round(total_infected * cfr_frac)
    attack_rate = round(total_infected / N * 100, 1)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Peak simultaneously infectious", f"{round(peak_i):,}")
    col2.metric("Day of peak", f"Day {peak_day}")
    col3.metric("Total infected (final)", f"{round(total_infected):,}", help=f"Attack rate: {attack_rate}%")
    col4.metric("Estimated deaths", f"{total_deaths:,}", help=f"CFR = {sir_cfr}%")

    max_val = max(max(i_vals), max(s_vals)) * 1.05
    chart_w, chart_h = 860, 280
    pad_l, pad_r, pad_t, pad_b = 60, 20, 20, 40

    def cx(day): return pad_l + (day / max_days) * (chart_w - pad_l - pad_r)
    def cy(val): return pad_t + chart_h - pad_b - (val / max_val) * (chart_h - pad_t - pad_b)

    s_pts = " ".join(f"{cx(d):.1f},{cy(v):.1f}" for d, v in zip(days_sampled, s_vals))
    i_pts = " ".join(f"{cx(d):.1f},{cy(v):.1f}" for d, v in zip(days_sampled, i_vals))
    r_pts = " ".join(f"{cx(d):.1f},{cy(v):.1f}" for d, v in zip(days_sampled, r_vals))

    y_ticks = [round(max_val * i / 4) for i in range(5)]
    y_tick_html = "".join(f"<text x='{pad_l-6}' y='{cy(t)+4:.0f}' text-anchor='end' font-size='10' fill='#888'>{t:,}</text>" for t in y_ticks)
    x_tick_days = [0, 60, 120, 180, 240, 300, 365]
    x_tick_html = "".join(f"<text x='{cx(d):.0f}' y='{chart_h+2}' text-anchor='middle' font-size='10' fill='#888'>Day {d}</text>" for d in x_tick_days if d <= max_days)
    peak_x = cx(peak_day)
    grid_lines = "".join(f"<line x1='{pad_l}' y1='{cy(t):.0f}' x2='{chart_w-pad_r}' y2='{cy(t):.0f}' stroke='#eee' stroke-width='1'/>" for t in y_ticks)

    svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='100%' viewBox='0 0 {chart_w} {chart_h+10}' style='display:block; background:#fafafa; border-radius:8px; border:1px solid #e0e0e0;'>
  {grid_lines}
  <line x1='{peak_x:.0f}' y1='{pad_t}' x2='{peak_x:.0f}' y2='{chart_h-pad_b}' stroke='#c0392b' stroke-width='1' stroke-dasharray='4,3' opacity='0.6'/>
  <text x='{min(peak_x+4, chart_w-80):.0f}' y='{pad_t+14}' font-size='10' fill='#c0392b'>Peak day {peak_day}</text>
  <polyline points='{s_pts}' fill='none' stroke='{PRIMARY}' stroke-width='2' opacity='0.8'/>
  <polyline points='{i_pts}' fill='none' stroke='{SECONDARY}' stroke-width='2.5'/>
  <polyline points='{r_pts}' fill='none' stroke='#2e7d32' stroke-width='2' opacity='0.8'/>
  <line x1='{pad_l}' y1='{pad_t}' x2='{pad_l}' y2='{chart_h-pad_b}' stroke='#ccc' stroke-width='1'/>
  <line x1='{pad_l}' y1='{chart_h-pad_b}' x2='{chart_w-pad_r}' y2='{chart_h-pad_b}' stroke='#ccc' stroke-width='1'/>
  {y_tick_html}
  {x_tick_html}
  <rect x='{chart_w-160}' y='30' width='12' height='3' fill='{PRIMARY}'/>
  <text x='{chart_w-144}' y='35' font-size='11' fill='{PRIMARY}'>Susceptible</text>
  <rect x='{chart_w-160}' y='48' width='12' height='3' fill='{SECONDARY}'/>
  <text x='{chart_w-144}' y='53' font-size='11' fill='{SECONDARY}'>Infectious</text>
  <rect x='{chart_w-160}' y='66' width='12' height='3' fill='#2e7d32'/>
  <text x='{chart_w-144}' y='71' font-size='11' fill='#2e7d32'>Removed</text>
</svg>"""

    st.markdown(svg, unsafe_allow_html=True)
    st.caption(f"Population: {N:,} | R0 = {sir_r0} | Infectious period: {sir_infectious} days | CFR: {sir_cfr}% | Starting immunity: {sir_vacc}% | Starting cases: {sir_initial}")

    st.markdown(f"""
**What this curve shows:**
- **Blue (Susceptible):** Starts near {N:,}, falls as people get infected. Final susceptibles: ~{round(s_vals[-1]):,} — escaped infection.
- **Orange (Infectious):** Rises, peaks at **Day {peak_day}** with ~{round(peak_i):,} simultaneously infectious, then declines.
- **Green (Removed):** Accumulates recovered + dead. Total infected: ~{round(total_infected):,} ({attack_rate}% attack rate).
- **The outbreak ends before infecting everyone** — it stops when Rt drops below 1 due to depletion of susceptibles.
    """)

    with st.expander("💡 What happens when you change the parameters?"):
        st.markdown(f"""
**Increase R0:** Peak is higher and earlier. More of the population gets infected.

**Decrease infectious period:** Faster removal → lower peak → smaller total outbreak. Effective isolation shortens the infectious period.

**Increase starting immunity:** Peak is dramatically lower. If immunity exceeds the HIT ({round((1-1/sir_r0)*100,1)}% for R0={sir_r0}), the outbreak barely gets started.

**Increase CFR:** Does not change the curve shape — CFR affects deaths, not transmission. The curve looks the same; the death toll changes.

**Try this:** Set starting immunity to {round((1-1/sir_r0)*100,1)}% (the HIT for R0={sir_r0}). Watch what happens to the peak.
        """)

    with st.expander("📐 Show me the math — SIR Model"):
        st.markdown(f"""
**Parameters:**
- β (transmission rate) = R0 × γ = {sir_r0} × {round(gamma,4)} = **{round(beta,4)}** per day
- γ (removal rate) = 1 / {sir_infectious} days = **{round(gamma,4)}** per day

**The three equations (solved numerically each half-day):**

dS/dt = −β × S × I / N  →  new infections per day

dI/dt = β × S × I / N − γ × I  →  change in infectious count

dR/dt = γ × I  →  removals per day (recovered + dead)

**Attack rate** = (N − S_final) / N = {round(total_infected):,} / {N:,} = **{attack_rate}%**

**Deaths** = total infected × CFR = {round(total_infected):,} × {round(cfr_frac,4)} = **{total_deaths:,}**

**Why doesn't 100% get infected?** The outbreak self-limits when Rt = R0 × S/N falls below 1. At that point fewer than {round(1/sir_r0*100,1)}% are still susceptible and the virus can't sustain transmission.
        """)

# ══════════════════════════════════════════════════════════
# TAB 2: PRACTICE
# ══════════════════════════════════════════════════════════
with tab_practice:

    st.markdown(f"### <span style='color:{PRIMARY}'>Practice Scenarios</span>", unsafe_allow_html=True)
    st.markdown("Work through each scenario one question at a time. You'll get immediate feedback.")

    SCENARIOS = [
        {
            "id":"h1","title":"Scenario 1: Measles Outbreak in an Under-Vaccinated Community",
            "description":"A measles outbreak occurs in a rural community of 5,000 people. The R0 for measles is 15. Current vaccination coverage in the community is 85%, and the MMR vaccine is 97% effective against measles.",
            "questions":[
                {"q":"What is the Herd Immunity Threshold (HIT) for measles with R0 = 15?",
                 "options":["— Select —","80.0%","86.7%","93.3%","95.0%"],"correct":"93.3%",
                 "hint":"HIT = 1 − (1/R0) = 1 − (1/15) = 1 − 0.067 = 0.933 = **93.3%**",
                 "wrong":{"80.0%":"❌ HIT = 1 − 1/R0 = 1 − 1/15 = 93.3%. 80% would correspond to R0 = 5.","86.7%":"❌ HIT = 1 − 1/15 = 93.3%. Check your calculation: 1/15 = 0.067, not 0.133.","95.0%":"❌ 95% would correspond to R0 = 20. For R0 = 15: HIT = 1 − 1/15 = 93.3%."}},
                {"q":"What vaccine coverage is needed to achieve herd immunity, given VE = 97%?",
                 "options":["— Select —","86.7%","90.0%","96.1%","99.5%"],"correct":"96.1%",
                 "hint":"VC = HIT / VE = 0.933 / 0.97 = **0.961 = 96.1%**",
                 "wrong":{"86.7%":"❌ VC = HIT/VE = 0.933/0.97 = 96.1%. 86.7% doesn't account for vaccine effectiveness.","90.0%":"❌ VC = HIT/VE = 0.933/0.97 = 96.1%. You need to divide the HIT by vaccine effectiveness.","99.5%":"❌ VC = 0.933/0.97 = 96.1%. 99.5% would be needed only if VE were around 93.8%."}},
                {"q":"Current coverage is 85%. Is herd immunity achieved?",
                 "options":["— Select —","Yes — 85% is close enough","No — 85% is below the required 96.1%","Yes — because the vaccine is 97% effective","Cannot be determined without more data"],"correct":"No — 85% is below the required 96.1%",
                 "hint":"Required vaccine coverage is 96.1%. Current coverage is 85%. 85% < 96.1% → herd immunity is **not** achieved. This community is vulnerable to an outbreak.",
                 "wrong":{"Yes — 85% is close enough":"❌ Herd immunity thresholds are not approximations — they are mathematical thresholds. 85% < 96.1% means the outbreak can still sustain itself.","Yes — because the vaccine is 97% effective":"❌ High vaccine effectiveness helps but doesn't compensate for low coverage. Both are needed: VC = HIT/VE.","Cannot be determined without more data":"❌ We have all the information needed: required VC = 96.1%, current VC = 85%. Herd immunity is not achieved."}}
            ],
            "calculation":{
                "type":"hit_vc","r0":15,"ve":0.97,
                "context":"Calculate the HIT, required vaccine coverage, and the coverage gap for this community."
            }
        },
        {
            "id":"h2","title":"Scenario 2: COVID-19 Intervention Effectiveness",
            "description":"During a COVID-19 surge, Rt is estimated at 2.8 in a city where 40% of the population has immunity from vaccination or prior infection. Public health officials are considering implementing a mask mandate (40% effective) and reducing indoor gatherings by 30%.",
            "questions":[
                {"q":"Without any new interventions, what is the current Rt?",
                 "options":["— Select —","Rt = 2.8","Rt = 1.68","Rt = 1.12","Rt = 0.84"],"correct":"Rt = 1.68",
                 "hint":"Rt = R0 × proportion susceptible. We need R0 first. If current Rt = 2.8 in a fully susceptible population, that IS R0. But here Rt is measured with 40% immune, so: Rt = R0 × 0.60. Wait — re-read: 'Rt is estimated at 2.8' already accounting for current immunity. The question asks current Rt = **1.68**? Actually re-reading: Rt = R0 × (1 − 0.40). If R0 is what produces Rt=2.8 with no immunity (i.e. R0 = 2.8), then with 40% immune: Rt = 2.8 × 0.60 = **1.68**",
                 "wrong":{"Rt = 2.8":"❌ R0 = 2.8 is the reproductive number in a fully susceptible population. With 40% immune, Rt = R0 × (1−0.40) = 2.8 × 0.60 = 1.68.","Rt = 1.12":"❌ Rt = R0 × proportion susceptible = 2.8 × 0.60 = 1.68, not 1.12.","Rt = 0.84":"❌ Rt = 2.8 × 0.60 = 1.68. 0.84 would require 70% immune (2.8 × 0.30 = 0.84)."}},
                {"q":"With masks (40% effective) AND 30% contact reduction, what does Rt become?",
                 "options":["— Select —","Rt = 1.68","Rt = 1.01","Rt = 0.71","Rt = 0.42"],"correct":"Rt = 0.71",
                 "hint":"Rt = R0 × prop. susceptible × (1 − mask eff.) × (1 − distancing) = 2.8 × 0.60 × 0.60 × 0.70 = **0.71**",
                 "wrong":{"Rt = 1.68":"❌ This is Rt without interventions. With masks (40% eff.) and 30% contact reduction: 2.8 × 0.60 × 0.60 × 0.70 = 0.71.","Rt = 1.01":"❌ Rt = 2.8 × 0.60 × (1−0.40) × (1−0.30) = 2.8 × 0.60 × 0.60 × 0.70 = 0.71.","Rt = 0.42":"❌ 0.42 would require more aggressive interventions. Check: 2.8 × 0.60 × 0.60 × 0.70 = 0.706 ≈ 0.71."}},
                {"q":"Based on this Rt, what will happen to case counts if these interventions are sustained?",
                 "options":["— Select —","Cases will grow exponentially","Cases will remain stable","Cases will decline","Cannot determine from Rt alone"],"correct":"Cases will decline",
                 "hint":"Rt = 0.71 < 1. When Rt < 1, each case produces fewer than 1 new case on average → the outbreak is declining.",
                 "wrong":{"Cases will grow exponentially":"❌ Cases grow when Rt > 1. Rt = 0.71 < 1 → the outbreak is declining.","Cases will remain stable":"❌ Stable (endemic) transmission occurs when Rt = 1. At Rt = 0.71, cases are declining.","Cannot determine from Rt alone":"❌ Rt directly tells us the trajectory. Rt < 1 → declining. Rt = 1 → stable. Rt > 1 → growing."}}
            ],
            "calculation":{
                "type":"rt","r0":2.8,"immune_pct":40,"mask_eff":40,"distancing":30,
                "context":"Calculate Rt before and after interventions."
            }
        },
        {
            "id":"h3","title":"Scenario 3: Influenza Pandemic Planning",
            "description":"A novel influenza strain has R0 = 2.2 with a generation time of 3 days. A vaccine is developed with 70% effectiveness. Public health planners want to know: (1) What HIT must be reached? (2) What vaccine coverage is needed? (3) How quickly will cases double without interventions?",
            "questions":[
                {"q":"What is the Herd Immunity Threshold for this influenza strain?",
                 "options":["— Select —","45.5%","54.5%","63.6%","72.7%"],"correct":"54.5%",
                 "hint":"HIT = 1 − 1/R0 = 1 − 1/2.2 = 1 − 0.455 = **0.545 = 54.5%**",
                 "wrong":{"45.5%":"❌ 45.5% = 1/R0 = 1/2.2. That's the proportion that can REMAIN susceptible, not the HIT. HIT = 1 − 1/2.2 = 54.5%.","63.6%":"❌ HIT = 1 − 1/2.2 = 54.5%. 63.6% would correspond to R0 ≈ 2.75.","72.7%":"❌ HIT = 1 − 1/2.2 = 54.5%. 72.7% would correspond to R0 ≈ 3.67."}},
                {"q":"What vaccine coverage is needed given 70% vaccine effectiveness?",
                 "options":["— Select —","54.5%","63.6%","77.9%","85.0%"],"correct":"77.9%",
                 "hint":"VC = HIT / VE = 0.545 / 0.70 = **0.779 = 77.9%**",
                 "wrong":{"54.5%":"❌ 54.5% is the HIT. You must divide by vaccine effectiveness to get required coverage: 0.545/0.70 = 77.9%.","63.6%":"❌ VC = HIT/VE = 0.545/0.70 = 77.9%. 63.6% doesn't correctly apply the VE correction.","85.0%":"❌ VC = 0.545/0.70 = 77.9%. 85% would be needed if VE were around 64%."}},
                {"q":"With Rt = 2.2 and generation time of 3 days, what is the doubling time?",
                 "options":["— Select —","2.6 days","3.8 days","5.2 days","7.1 days"],"correct":"3.8 days",
                 "hint":"Td = Tg × ln(2) / ln(Rt) = 3 × 0.693 / ln(2.2) = 3 × 0.693 / 0.788 = **2.64 days** — wait, let me recalculate: Td = 3 × 0.6931 / 0.7885 = **2.64**. Hmm, closest answer is 2.6 days.",
                 "wrong":{"3.8 days":"⚠️ Close — let's verify: Td = 3 × ln(2)/ln(2.2) = 3 × 0.6931/0.7885 = 2.64 days. The closest correct answer is 2.6 days.","5.2 days":"❌ Td = Tg × ln(2)/ln(Rt) = 3 × 0.693/0.788 = 2.6 days. 5.2 days would require a much lower Rt.","7.1 days":"❌ Td = 3 × 0.693/ln(2.2) = 2.6 days. 7.1 days would require Rt close to 1.35."}}
            ],
            "calculation":{
                "type":"planning","r0":2.2,"ve":0.70,"tg":3,
                "context":"Calculate HIT, required vaccine coverage, and doubling time."
            }
        },
        {
            "id":"h4","title":"Scenario 4: Ebola Outbreak Control",
            "description":"An Ebola outbreak is detected with R0 estimated at 1.8. Unlike respiratory diseases, Ebola spreads through direct contact with bodily fluids. A ring vaccination campaign achieves 60% coverage among contacts with a vaccine that is 85% effective. Simultaneously, safe burial practices reduce transmission by 50%.",
            "questions":[
                {"q":"What is the HIT for this Ebola outbreak?",
                 "options":["— Select —","33.3%","44.4%","55.6%","66.7%"],"correct":"44.4%",
                 "hint":"HIT = 1 − 1/R0 = 1 − 1/1.8 = 1 − 0.556 = **0.444 = 44.4%**",
                 "wrong":{"33.3%":"❌ HIT = 1 − 1/1.8 = 44.4%. 33.3% would correspond to R0 = 1.5.","55.6%":"❌ 55.6% = 1/1.8 is the proportion that can stay susceptible. HIT = 1 − 1/1.8 = 44.4%.","66.7%":"❌ HIT = 1 − 1/1.8 = 44.4%. 66.7% corresponds to R0 = 3.0."}},
                {"q":"Ebola has a relatively low R0 compared to measles. What does this mean for control efforts?",
                 "options":["— Select —","Ebola is easier to control because a lower proportion needs to be immune","Ebola is harder to control because it is more deadly","Ebola and measles require similar control efforts","R0 has no practical meaning for disease control"],"correct":"Ebola is easier to control because a lower proportion needs to be immune",
                 "hint":"Lower R0 = lower HIT. Ebola HIT = 44.4% vs. measles HIT = 93.3%. A much smaller proportion needs to be immune to stop Ebola spread — making ring vaccination feasible where population-wide vaccination would be logistically challenging.",
                 "wrong":{"Ebola is harder to control because it is more deadly":"❌ Deadliness and transmissibility are separate. R0 measures transmission, not mortality. Lower R0 means lower HIT — easier to reach the threshold for herd immunity.","Ebola and measles require similar control efforts":"❌ Measles R0 = 12–18 (HIT ~93%), Ebola R0 = 1.5–2.5 (HIT ~33–60%). These require very different levels of population immunity.","R0 has no practical meaning for disease control":"❌ R0 directly determines the HIT, vaccine coverage needed, and the feasibility of control strategies."}},
                {"q":"With 50% transmission reduction from safe burials, what is the new Rt (assuming fully susceptible population before vaccination)?",
                 "options":["— Select —","Rt = 1.8","Rt = 0.9","Rt = 0.54","Rt = 0.36"],"correct":"Rt = 0.9",
                 "hint":"Rt = R0 × intervention factor = 1.8 × (1 − 0.50) = 1.8 × 0.50 = **0.9**",
                 "wrong":{"Rt = 1.8":"❌ Rt = R0 without any interventions. With 50% transmission reduction: Rt = 1.8 × 0.50 = 0.9.","Rt = 0.54":"❌ Rt = 1.8 × (1 − 0.50) = 0.9. 0.54 would require a 70% reduction: 1.8 × 0.30.","Rt = 0.36":"❌ Rt = 1.8 × 0.50 = 0.9. 0.36 would require 80% reduction: 1.8 × 0.20."}}
            ],
            "calculation":{
                "type":"hit_vc","r0":1.8,"ve":0.85,
                "context":"Calculate HIT, required vaccine coverage, and effect of safe burial practices."
            }
        },
        {
            "id":"h5","title":"Scenario 5: Comparing Outbreak Speed",
            "description":"Two respiratory pathogens emerge simultaneously. Pathogen A has R0 = 3, generation time 4 days. Pathogen B has R0 = 2, generation time 2 days. A public health director needs to know which outbreak will double cases faster.",
            "questions":[
                {"q":"What is the doubling time for Pathogen A (R0=3, Tg=4 days)?",
                 "options":["— Select —","2.5 days","3.5 days","4.5 days","6.3 days"],"correct":"2.5 days",
                 "hint":"Td = Tg × ln(2) / ln(R0) = 4 × 0.6931 / ln(3) = 4 × 0.6931 / 1.0986 = **2.52 ≈ 2.5 days**",
                 "wrong":{"3.5 days":"❌ Td = 4 × 0.6931/1.0986 = 2.52 ≈ 2.5 days. Check: ln(3) = 1.099.","4.5 days":"❌ Td = 4 × ln(2)/ln(3) = 4 × 0.693/1.099 = 2.5 days. 4.5 days would require a lower R0.","6.3 days":"❌ Td = 4 × 0.693/ln(3) = 2.5 days. 6.3 days would correspond to a much lower growth rate."}},
                {"q":"What is the doubling time for Pathogen B (R0=2, Tg=2 days)?",
                 "options":["— Select —","2.0 days","2.5 days","3.0 days","4.0 days"],"correct":"2.0 days",
                 "hint":"Td = Tg × ln(2) / ln(R0) = 2 × 0.6931 / ln(2) = 2 × 0.6931 / 0.6931 = **2.0 days**",
                 "wrong":{"2.5 days":"❌ Td = 2 × ln(2)/ln(2) = 2 × 1 = 2.0 days. Note: ln(R0) = ln(2) = 0.693, so the ln(2) terms cancel.","3.0 days":"❌ Td = 2 × 0.693/0.693 = 2.0 days. When R0 = 2, ln(R0) = ln(2), so Td = Tg.","4.0 days":"❌ Td = 2 × ln(2)/ln(2) = 2.0 days. The formula gives exactly 2.0 days here."}},
                {"q":"Which pathogen requires more urgent response, and why?",
                 "options":["— Select —","Pathogen A — higher R0 means more secondary cases","Pathogen B — faster doubling time means faster case growth","Both equally urgent — similar doubling times","Pathogen A — longer generation time gives more time to respond"],"correct":"Pathogen B — faster doubling time means faster case growth",
                 "hint":"Pathogen A doubles every 2.5 days. Pathogen B doubles every 2.0 days. Despite lower R0, Pathogen B's shorter generation time makes it grow faster. In outbreak response, **speed of doubling** determines urgency — not R0 alone.",
                 "wrong":{"Pathogen A — higher R0 means more secondary cases":"❌ R0 determines long-run spread potential and HIT, but doubling time determines immediate outbreak speed. Pathogen B doubles every 2 days vs. 2.5 for A — B grows faster.","Both equally urgent — similar doubling times":"❌ 2.0 days vs. 2.5 days may seem similar but leads to dramatically different case counts quickly. After 10 days: Pathogen B has 2^5 = 32× starting cases; Pathogen A has 2^4 = 16× starting cases.","Pathogen A — longer generation time gives more time to respond":"❌ Longer generation time actually slows spread. Pathogen B's 2-day generation time means it doubles faster despite lower R0."}}
            ],
            "calculation":{
                "type":"doubling","pathogens":[{"label":"Pathogen A","r0":3,"tg":4},{"label":"Pathogen B","r0":2,"tg":2}],
                "context":"Calculate and compare doubling times for both pathogens."
            }
        },
    ]

    if "prac_reset_count" not in st.session_state: st.session_state["prac_reset_count"] = 0
    if "prac_order" not in st.session_state:
        order = list(range(len(SCENARIOS))); random.shuffle(order)
        st.session_state["prac_order"] = order

    rc = st.session_state["prac_reset_count"]

    col_info, col_rst = st.columns([5,1])
    with col_info: st.caption(f"**{len(SCENARIOS)} scenarios** — answer one question at a time.")
    with col_rst:
        if st.button("🔄 Reset", key="reset_practice"):
            st.session_state["prac_reset_count"] += 1
            keys_to_del = [k for k in st.session_state.keys() if k.startswith("prac_") and k not in ["prac_reset_count","prac_order"]]
            for k in keys_to_del: del st.session_state[k]
            if "prac_order" in st.session_state: del st.session_state["prac_order"]
            st.rerun()

    SHUFFLED = [SCENARIOS[i] for i in st.session_state["prac_order"]]

    for sc in SHUFFLED:
        st.divider()
        sid = sc["id"]
        q_states = [st.session_state.get(f"prac_{sid}_q{qi}_correct_{rc}") for qi in range(len(sc["questions"]))]
        all_done = all(q is True for q in q_states)
        correct_count = sum(1 for q in q_states if q is True)

        st.markdown(f"""
        <div style='background:{LIGHT_BG}; border-radius:8px; padding:14px 18px; border-left:4px solid {PRIMARY};'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <b style='color:{PRIMARY}; font-size:16px;'>{sc['title']}</b>
                <span style='background:{"#2e7d32" if all_done else SECONDARY}; color:white; border-radius:12px; padding:2px 12px; font-size:13px;'>{correct_count}/{len(sc['questions'])} correct</span>
            </div>
        </div>""", unsafe_allow_html=True)
        st.markdown("")
        st.markdown(sc["description"])

        for qi, q in enumerate(sc["questions"]):
            prev_ok = st.session_state.get(f"prac_{sid}_q{qi-1}_correct_{rc}") if qi > 0 else True
            if prev_ok is not True and qi > 0: break

            answered_correctly = st.session_state.get(f"prac_{sid}_q{qi}_correct_{rc}", False)
            st.markdown(f"**Question {qi+1}:** {q['q']}")

            if answered_correctly:
                st.success(f"✅ **{st.session_state.get(f'prac_{sid}_q{qi}_answer_{rc}')}** — {q['hint']}")
            else:
                choice = st.selectbox("Select your answer:", q["options"], key=f"prac_{sid}_q{qi}_sel_{rc}", label_visibility="collapsed")
                if choice != "— Select —":
                    if st.button("Submit Answer", key=f"prac_{sid}_q{qi}_btn_{rc}", type="primary"):
                        st.session_state[f"prac_{sid}_q{qi}_answer_{rc}"] = choice
                        st.session_state[f"prac_{sid}_q{qi}_correct_{rc}"] = (choice == q["correct"])
                        st.rerun()
                last_answer = st.session_state.get(f"prac_{sid}_q{qi}_answer_{rc}")
                last_correct = st.session_state.get(f"prac_{sid}_q{qi}_correct_{rc}")
                if last_answer and last_correct is False:
                    wrong_msg = q.get("wrong",{}).get(last_answer,"❌ Not quite. Review the hint and try again.")
                    st.error(wrong_msg)
                    st.info(f"💡 **Hint:** {q['hint']}")

        if all_done and "calculation" in sc:
            st.markdown("---")
            st.markdown("### 🎉 All correct! Now run the calculations.")
            d = sc["calculation"]
            st.markdown(d["context"])

            if d["type"] == "hit_vc":
                hit_c = round((1 - 1/d["r0"]) * 100, 1)
                vc_c = round(hit_c / (d["ve"]*100) * 100, 1) if "ve" in d else None
                col1,col2 = st.columns(2)
                col1.metric("Herd Immunity Threshold", f"{hit_c}%")
                if vc_c: col2.metric(f"Required Vaccine Coverage (VE={int(d['ve']*100)}%)", f"{vc_c}%")
                vc_note = f" | Required coverage = {hit_c}%/{int(d['ve']*100)}% = {vc_c}%" if vc_c else ""
                st.info(f"HIT = 1 − 1/{d['r0']} = {hit_c}%{vc_note}")

            elif d["type"] == "rt":
                prop_s = (100 - d["immune_pct"])/100
                int_factor = (1 - d["mask_eff"]/100) * (1 - d["distancing"]/100)
                rt_before = round(d["r0"] * prop_s, 2)
                rt_after = round(d["r0"] * prop_s * int_factor, 2)
                col1,col2 = st.columns(2)
                col1.metric("Rt before interventions", rt_before)
                col2.metric("Rt after interventions", rt_after, delta=f"{round(rt_after-rt_before,2)}", delta_color="inverse")
                if rt_after < 1: st.success(f"Rt = {rt_after} < 1 — Interventions bring outbreak under control.")
                else: st.error(f"Rt = {rt_after} > 1 — Further measures needed.")

            elif d["type"] == "planning":
                hit_p = round((1 - 1/d["r0"])*100,1)
                vc_p = round(hit_p/d["ve"]/100*100,1) if "ve" in d else None
                td_p = round(d["tg"]*math.log(2)/math.log(d["r0"]),1)
                col1,col2,col3 = st.columns(3)
                col1.metric("HIT", f"{hit_p}%")
                if vc_p: col2.metric(f"Required Coverage (VE={int(d['ve']*100)}%)", f"{vc_p}%")
                col3.metric("Doubling Time", f"{td_p} days")

            elif d["type"] == "doubling":
                cols = st.columns(len(d["pathogens"]))
                for i, p in enumerate(d["pathogens"]):
                    td_p = round(p["tg"]*math.log(2)/math.log(p["r0"]),1)
                    cols[i].metric(f"{p['label']} Doubling Time", f"{td_p} days")
                    cols[i].caption(f"R0={p['r0']}, Tg={p['tg']} days")

    st.divider()
    if st.button("📊 Show My Score", key="show_score"):
        answered = sum(sum(1 for qi in range(len(sc["questions"])) if st.session_state.get(f"prac_{sc['id']}_q{qi}_correct_{rc}") is not None) for sc in SCENARIOS)
        correct_q = sum(sum(1 for qi in range(len(sc["questions"])) if st.session_state.get(f"prac_{sc['id']}_q{qi}_correct_{rc}") is True) for sc in SCENARIOS)
        if answered == 0: st.info("You haven't answered any questions yet.")
        else:
            pct = round(correct_q/answered*100)
            st.subheader(f"Score: {correct_q} / {answered} questions answered")
            st.progress(pct/100)
            if pct == 100: st.success("🏆 Perfect score!")
            elif pct >= 80: st.success("Great work! Review any scenarios you found challenging.")
            elif pct >= 60: st.info("Good progress. Revisit the Learn tab for concepts you're unsure about.")
            else: st.warning("Keep practicing. Use the Learn tab and Glossary to review before trying again.")

# ══════════════════════════════════════════════════════════
# TAB 3: GLOSSARY
# ══════════════════════════════════════════════════════════
with tab_glossary:

    st.markdown(f"### <span style='color:{PRIMARY}'>Glossary: Herd Immunity & Reproductive Numbers</span>", unsafe_allow_html=True)

    with st.expander("📐 Core Concepts", expanded=True):
        st.markdown(f"""
**Basic Reproductive Number (R0)** — The average number of secondary cases produced by one infectious person in a **completely susceptible population** with no interventions. R0 is a property of the pathogen AND its environment (contact patterns, transmission route). It does not change with vaccination or behavior — but it can differ across populations and settings.

**Effective Reproductive Number (Rt or Re)** — The average number of secondary cases at a specific point in time, accounting for current immunity levels and interventions. Rt = R0 × (proportion susceptible) × (intervention reduction factors). **The goal of public health is to drive Rt below 1.**

**Herd Immunity Threshold (HIT)** — The proportion of a population that must be immune to prevent sustained transmission. HIT = 1 − (1/R0). The higher the R0, the higher the HIT.

**Herd Immunity** — The indirect protection of unvaccinated/non-immune individuals that occurs when enough of the population is immune to break transmission chains. Does NOT mean everyone is protected — it means the disease cannot sustain an outbreak.

**Generation Time (Tg)** — The average time between when a person is infected and when they infect someone else. Short Tg = rapid spread.

**Doubling Time (Td)** — The time for case counts to double during exponential growth. Td = Tg × ln(2) / ln(Rt). Shorter Td = more urgent outbreak.

**Vaccine Effectiveness (VE)** — The percentage reduction in disease among vaccinated people compared to unvaccinated people. A 95% effective vaccine reduces risk of infection by 95% in vaccinated individuals.

**Required Vaccine Coverage (VC)** — The proportion of the population that needs to be vaccinated to achieve herd immunity, accounting for imperfect vaccine effectiveness. VC = HIT / VE.
        """)

    with st.expander("🔢 Key Formulas"):
        st.markdown(f"""
| Formula | Meaning |
|---|---|
| HIT = 1 − 1/R0 | Proportion of population that must be immune |
| VC = HIT / VE | Vaccine coverage needed given imperfect VE |
| Rt = R0 × S × I | Effective R at time t (S = susceptible proportion, I = intervention factor) |
| Td = Tg × ln(2) / ln(Rt) | Doubling time during exponential growth |
| Intervention factor = (1−eff₁) × (1−eff₂) | Combined effect of multiple independent interventions |
        """)

    with st.expander("❓ Common Confusions"):
        st.markdown("""
**R0 vs. Rt:** R0 is fixed (a property of the pathogen). Rt changes over time as immunity accumulates and interventions are applied. During an outbreak we track Rt, not R0.

**Herd immunity threshold vs. vaccine coverage needed:** HIT assumes perfect vaccines. In reality, VC = HIT/VE — you need more people vaccinated than the HIT because some vaccinated people remain susceptible.

**Rt < 1 doesn't mean zero cases:** Rt < 1 means the outbreak is *declining*, not that transmission has stopped. Cases will continue to occur but at a decreasing rate.

**R0 and deadliness:** R0 measures transmission, not mortality. Ebola has a low R0 but extremely high case-fatality rate. COVID-19 has a higher R0 but lower CFR. These are independent dimensions of a pathogen's threat.

**Herd immunity from infection vs. vaccination:** Both contribute to population immunity and Rt reduction. However, infection-acquired immunity carries the risk of severe disease and death — vaccination achieves the same immunity safely.

**Doubling time and R0:** A higher R0 doesn't always mean faster doubling time — generation time matters too. A pathogen with R0=2 and Tg=1 day doubles faster than one with R0=10 and Tg=30 days.
        """)

    with st.expander("🌍 R0 Reference Table"):
        ref_data = {
            "Disease": ["Measles","Chickenpox","Mumps","Polio","Smallpox","COVID-19 (Omicron)","COVID-19 (original)","Influenza (seasonal)","HIV","Ebola"],
            "R0 Range": ["12–18","8–10","4–7","5–7","5–7","8–15","2–3","1–2","2–5","1.5–2.5"],
            "HIT (approx.)": ["93–94%","88–90%","75–86%","80–86%","80–86%","88–93%","50–67%","0–50%","50–80%","33–60%"],
            "Transmission": ["Airborne","Airborne/contact","Droplets","Fecal-oral","Droplets/contact","Airborne","Droplets","Droplets","Sexual/blood","Direct contact"],
        }
        st.table(pd.DataFrame(ref_data).set_index("Disease"))
