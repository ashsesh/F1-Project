import pandas as pd
import matplotlib.pyplot as plt

# Set style
plt.style.use('ggplot')

# ===============================================
# HEADER AND SCENARIO
# ===============================================
print("=" * 70)
print("2025 ABU DHABI GP PREDICTION - CHAMPIONSHIP FINALE")
print("=" * 70)
print("SCENARIO: TWILIGHT RACE (28-30°C) - Stable & Dry")
print("REGULATION: Title Decider - Norris vs Verstappen vs Piastri")
print("STRATEGY: One-Stop (Soft/Medium -> Hard) - Track Evolution Critical")
print("USER OVERRIDE: Traffic/Dirty Air Penalties MINIMIZED (Expect the Unexpected)")
print("=" * 70)

# ===============================================
# 1. DATA INPUT (Abu Dhabi Qualifying Results)
# ===============================================
qualifying_abudhabi = pd.DataFrame({
    "Driver": ["VER", "NOR", "PIA", "RUS", "LEC", "ALO", "BOR", "OCO", "HAD", "TSU"],
    "Team": ["Red Bull", "McLaren", "McLaren", "Mercedes", "Ferrari",
             "Aston Martin", "Sauber", "Haas", "RB", "Red Bull"],
    "QualifyingPosition": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "QualifyingTime": [82.207, 82.408, 82.437, 82.645, 82.730,
                       82.902, 82.904, 82.913, 83.072, 83.083]
})

qualifying_abudhabi["QualifyingGap"] = qualifying_abudhabi["QualifyingTime"] - qualifying_abudhabi["QualifyingTime"].min()

# ===============================================
# 2. MODEL PARAMETERS
# ===============================================
points_current = {"NOR": 408, "VER": 396, "PIA": 392}

race_pace_abudhabi = {
    "VER": 95.00, "NOR": 95.05, "PIA": 95.05, "RUS": 95.30, "LEC": 95.20,
    "ALO": 95.80, "BOR": 96.00, "OCO": 96.00, "HAD": 96.20, "TSU": 96.20
}

traffic_penalty_abudhabi = {
    "VER": 0.00, "NOR": 0.02, "PIA": 0.04, "RUS": 0.05, "LEC": 0.05,
    "ALO": 0.08, "BOR": 0.10, "OCO": 0.10, "HAD": 0.12, "TSU": 0.12
}

form_abudhabi = {
    "VER": 0.990, "NOR": 1.000, "PIA": 0.995, "RUS": 1.000, "LEC": 0.995,
    "ALO": 1.000, "BOR": 1.010, "OCO": 1.000, "HAD": 1.010, "TSU": 1.000
}

# ===============================================
# 3. CALCULATION
# ===============================================
results = qualifying_abudhabi.copy()
results["RacePace"] = results["Driver"].map(race_pace_abudhabi)
results["TrafficPenalty"] = results["Driver"].map(traffic_penalty_abudhabi)
results["Form"] = results["Driver"].map(form_abudhabi)

results["RaceScore"] = (results["RacePace"] * results["Form"] + results["TrafficPenalty"])
results = results.sort_values("RaceScore").reset_index(drop=True)
results["PredictedPosition"] = range(1, len(results) + 1)
results["PositionChange"] = results["QualifyingPosition"] - results["PredictedPosition"]

# ===============================================
# 4. CHAMPIONSHIP CALCULATION
# ===============================================
points_map = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

def calculate_championship(prediction_df, current_points):
    final_standings = current_points.copy()
    for _, row in prediction_df.iterrows():
        driver = row['Driver']
        pos = row['PredictedPosition']
        if driver in final_standings:
            final_standings[driver] += points_map.get(pos, 0)
    winner = max(final_standings, key=final_standings.get)
    return final_standings, winner

final_points, champion = calculate_championship(results, points_current)

# ===============================================
# 5. FINAL PREDICTION SUMMARY (BEAUTIFUL OUTPUT)
# ===============================================
print("\n" + "=" * 70)
print("FINAL PREDICTION - 2025 ABU DHABI GRAND PRIX")
print("=" * 70)
print("P1: VER (Max Verstappen)     - Starts P1  | Red Bull")
print("P2: PIA (Oscar Piastri)       - Starts P3  | McLaren")
print("P3: LEC (Charles Leclerc)     - Starts P5  | Ferrari")
print("-" * 70)
print("Full Top 10 Predicted Finishing Order:")
for i, row in results.head(10).iterrows():
    change = row["PositionChange"]
    if change > 0:
        arrow = f"Up {change}"
    elif change < 0:
        arrow = f"Down {-change}"
    else:
        arrow = "No Change"
    print(f"{row['PredictedPosition']:2d}. {row['Driver']:3s} ({row['Team']:12s}) | Start P{row['QualifyingPosition']:2d} → {arrow}")
print("-" * 70)
print(f"2025 WORLD DRIVERS' CHAMPION: {champion} with {final_points[champion]} points")

if champion == "NOR":
    print("   LANDO NORRIS WINS HIS FIRST WORLD CHAMPIONSHIP!")
elif champion == "VER":
    print("   MAX VERSTAPPEN SECURES HIS 5TH TITLE!")
else:
    print("   OSCAR PIASTRI BECOMES THE YOUNGEST CHAMPION EVER!")
print("=" * 70)

# ===============================================
# 6. VISUALIZATION DASHBOARD (NOW 100% ERROR-FREE)
# ===============================================
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("2025 ABU DHABI GP - FINAL PREDICTION & TITLE DECIDER", fontsize=20, fontweight='bold', color='darkblue')

# Chart 1: Podium
ax1 = axes[0, 0]
top3 = results.head(3)
colors = ['gold', 'silver', '#CD7F32']
bars = ax1.bar(top3["Driver"], [3, 2, 1], color=colors, edgecolor='black', linewidth=1.5)
ax1.set_ylim(0, 4)
ax1.set_yticks([])
ax1.set_title('Predicted Podium', fontsize=14, fontweight='bold')
for i, (rect, driver) in enumerate(zip(bars, top3["Driver"])):
    ax1.text(rect.get_x() + rect.get_width()/2., 3.3 - i,
             f"P{i+1} {driver}", ha='center', va='bottom', fontsize=16, fontweight='bold')

# Chart 2: Championship Standings
ax2 = axes[0, 1]
contenders = ["NOR", "VER", "PIA"]
final_scores = [final_points[d] for d in contenders]
bars2 = ax2.bar(contenders, final_scores, color=['orange', 'navy', 'papayawhip'], edgecolor='black', linewidth=1.5)
ax2.set_title("Final 2025 Championship Points", fontsize=14, fontweight='bold')
ax2.set_ylim(0, max(final_scores) + 30)

for i, score in enumerate(final_scores):
    ax2.text(i, score + 5, str(score), ha='center', fontweight='bold', fontsize=14)

# Highlight champion with gold border
champ_idx = contenders.index(champion)
bars2[champ_idx].set_edgecolor('gold')
bars2[champ_idx].set_linewidth(6)

# Chart 3: Grid Evolution
ax3 = axes[1, 0]
grid_order = results.sort_values("QualifyingPosition")
ax3.plot(grid_order["Driver"], grid_order["QualifyingPosition"], 'o--', color='gray', label='Qualifying', markersize=10)
ax3.plot(grid_order["Driver"], grid_order["PredictedPosition"], 's-', color='purple', linewidth=3, label='Predicted Finish', markersize=10)
ax3.invert_yaxis()
ax3.set_title('Start → Finish Evolution', fontsize=14, fontweight='bold')
ax3.legend(fontsize=12)
ax3.grid(True, alpha=0.3)

# Chart 4: Performance Breakdown
ax4 = axes[1, 1]
base = results["RacePace"] * results["Form"]
ax4.bar(results["Driver"], base - 94, label='Adjusted Race Pace', color='#1E90FF', alpha=0.8)
ax4.bar(results["Driver"], results["TrafficPenalty"], bottom=base-94, label='Traffic Penalty', color='red', alpha=0.7)
ax4.set_title('Why They Finish Where They Do\n(Lower = Faster)', fontsize=14, fontweight='bold')
ax4.legend()
ax4.set_ylim(0.5, 3.5)

plt.tight_layout(rect=[0, 0.03, 1, 0.96])
plt.savefig("AbuDhabi_2025_Prediction_FINAL.png", dpi=300, bbox_inches='tight')
plt.show()