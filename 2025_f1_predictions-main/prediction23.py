import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set a professional style for the plots
plt.style.use('ggplot')

print("=" * 70)
print("🎰 2025 LAS VEGAS GP RACE PREDICTION - NEON NIGHTS EDITION 🎰")
print("=" * 70)
print("☀️  SCENARIO: DRY & COLD (0% Rain, 14°C Air Temp)")
print("📉  TRACK: Low Grip, High Top Speed, Heavy Braking")
print("=" * 70)

# --- 2025 Qualifying Data (Las Vegas GP) ---
qualifying_vegas = pd.DataFrame({
    "Driver": ["NOR", "VER", "SAI", "LEC", "PIA", "ANT", "RUS", "HAM", "HAD"],
    "QualifyingPosition": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "QualifyingTime (s)": [
        92.411, 92.495, 92.601, 92.650, 92.810, 
        92.900, 93.100, 93.150, 93.400
    ]
})

# ===============================================
# SCENARIO A: DRY & COLD RACE ❄️
# ===============================================

# Race Pace (Lower is faster)
race_pace_vegas = {
    "VER": 96.2, "NOR": 96.4, "LEC": 96.3, "SAI": 96.5,
    "PIA": 96.6, "HAM": 96.8, "RUS": 96.9, "ANT": 97.2, "HAD": 97.5
}

# Overtaking Factor (Higher is better)
overtaking_vegas = {
    "VER": 0.5, "NOR": 0.1, "LEC": 0.4, "SAI": 0.2,
    "HAM": 0.3, "PIA": 0.1, "RUS": 0.0, "ANT": -0.2, "HAD": -0.3
}

# Current Form
form_vegas = {
    "NOR": 0.96, "VER": 0.95, "SAI": 0.98, "LEC": 0.97,
    "ANT": 1.01, "PIA": 1.00, "HAM": 1.00, "RUS": 1.00, "HAD": 1.02
}

reliability_vegas = {
    "NOR": 1.00, "VER": 1.00, "SAI": 1.00, "LEC": 1.00, 
    "PIA": 1.00, "ANT": 1.02, "RUS": 1.00, "HAM": 1.00, "HAD": 1.05
}

# Calculate Results
vegas_results = qualifying_vegas.copy()
vegas_results["RacePace"] = vegas_results["Driver"].map(race_pace_vegas)
vegas_results["OvertakingFactor"] = vegas_results["Driver"].map(overtaking_vegas)
vegas_results["FormMultiplier"] = vegas_results["Driver"].map(form_vegas)
vegas_results["ReliabilityFactor"] = vegas_results["Driver"].map(reliability_vegas)

# Prediction Formula
vegas_results["RaceScore"] = (
    vegas_results["RacePace"] * vegas_results["FormMultiplier"] * vegas_results["ReliabilityFactor"] - 
    (vegas_results["OvertakingFactor"] * 0.4)
)

vegas_results = vegas_results.sort_values("RaceScore").reset_index(drop=True)
vegas_results["PredictedPosition"] = range(1, len(vegas_results) + 1)
vegas_results["PositionChange"] = vegas_results["QualifyingPosition"] - vegas_results["PredictedPosition"]

# Output Text
print("\n🏁 PREDICTED RESULTS (LAS VEGAS GP):\n")
print(vegas_results[[
    "PredictedPosition", "Driver", "QualifyingPosition", "RaceScore"
]].to_string(index=False))

print("\n" + "=" * 70)
print("🏆 LAS VEGAS GP PODIUM PREDICTION")
print("=" * 70)
print(f"🥇 P1: {vegas_results.iloc[0]['Driver']} (Change: {vegas_results.iloc[0]['PositionChange']:+d})")
print(f"🥈 P2: {vegas_results.iloc[1]['Driver']} (Change: {vegas_results.iloc[1]['PositionChange']:+d})")
print(f"🥉 P3: {vegas_results.iloc[2]['Driver']} (Change: {vegas_results.iloc[2]['PositionChange']:+d})")

# ===============================================
# 📊 VISUALIZATION SECTION
# ===============================================
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("2025 LAS VEGAS GP - PREDICTION ANALYSIS", fontsize=18, fontweight='bold', color='darkblue')

# --- Chart 1: The Podium Battle (Quali vs Race) ---
ax1 = axes[0, 0]
top_3_drivers = vegas_results.head(3)["Driver"].tolist()
# Filter data for just the top 3 predicted finishers
top_3_data = vegas_results[vegas_results["Driver"].isin(top_3_drivers)].sort_values("PredictedPosition")

x = np.arange(len(top_3_drivers))
width = 0.35

# Bar for Qualifying
ax1.bar(x - width/2, top_3_data["QualifyingPosition"], width, label='Start Pos (Quali)', color='gray', alpha=0.6)
# Bar for Race
ax1.bar(x + width/2, top_3_data["PredictedPosition"], width, label='Finish Pos (Pred)', color='gold')

ax1.set_ylabel('Position (Lower is Better)', fontsize=11)
ax1.set_title('Podium Fight: Where They Started vs. Finished', fontsize=12, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(top_3_data["Driver"])
ax1.legend()
ax1.invert_yaxis() # P1 at top

# --- Chart 2: Full Grid Evolution (Line Plot) ---
ax2 = axes[0, 1]
# We need the data sorted by original grid order to make the chart readable
grid_sorted = vegas_results.sort_values("QualifyingPosition")
drivers = grid_sorted["Driver"]
quali_pos = grid_sorted["QualifyingPosition"]
race_pos = grid_sorted["PredictedPosition"]

ax2.plot(drivers, quali_pos, 'o--', label='Qualifying', color='gray', linewidth=1.5, alpha=0.7)
ax2.plot(drivers, race_pos, 's-', label='Race Prediction', color='darkblue', linewidth=2.5)

# Add arrows for big movers
for i, txt in enumerate(drivers):
    change = grid_sorted.iloc[i]["PositionChange"]
    if abs(change) >= 1:
        color = 'green' if change > 0 else 'red'
        ax2.annotate(f"{change:+d}", 
                     (txt, race_pos.iloc[i]), 
                     xytext=(0, 10), textcoords='offset points', 
                     ha='center', color=color, fontweight='bold')

ax2.set_title('Grid Evolution: Qualifying ➔ Race Result', fontsize=12, fontweight='bold')
ax2.set_ylabel('Position')
ax2.legend()
ax2.invert_yaxis()
ax2.grid(True, linestyle='--', alpha=0.3)

# --- Chart 3: Position Gainers & Losers (Horizontal Bar) ---
ax3 = axes[1, 0]
# Sort by magnitude of change
changes = vegas_results.sort_values("PositionChange", ascending=True)
colors = ['red' if x < 0 else 'green' if x > 0 else 'gray' for x in changes["PositionChange"]]

ax3.barh(changes["Driver"], changes["PositionChange"], color=colors)
ax3.set_xlabel('Positions Gained (+) / Lost (-)', fontsize=11)
ax3.set_title('Biggest Movers: The "Strip" Effect', fontsize=12, fontweight='bold')
ax3.axvline(0, color='black', linewidth=0.8)

# --- Chart 4: Why They Won? (Race Score Analysis) ---
ax4 = axes[1, 1]
# Compare Race Pace (Physics) vs Overtaking Factor (Skill/Top Speed)
# We normalize them slightly for visual comparison
top_5 = vegas_results.head(5)
x_metrics = np.arange(len(top_5))

# We want to show Overtaking Factor because that's why Max wins
# Scale overtaking factor for visibility
overtaking_visual = top_5["OvertakingFactor"] * 10 

ax4.bar(x_metrics, top_5["RaceScore"], color='navy', alpha=0.3, label='Total Race Score (Lower=Better)')
ax4_twin = ax4.twinx()
ax4_twin.plot(x_metrics, overtaking_visual, color='orange', marker='o', linewidth=2, label='Overtaking/Top Speed Metric')

ax4.set_xticks(x_metrics)
ax4.set_xticklabels(top_5["Driver"])
ax4.set_ylim(90, 100) # Zoom in on the score scores
ax4.set_ylabel('Race Score')
ax4_twin.set_ylabel('Overtaking Capability (Higher=Better)')
ax4.set_title('Top 5 Analysis: Pace vs. Overtaking Power', fontsize=12, fontweight='bold')

# Combine legends
lines, labels = ax4.get_legend_handles_labels()
lines2, labels2 = ax4_twin.get_legend_handles_labels()
ax4_twin.legend(lines + lines2, labels + labels2, loc='upper left')

plt.tight_layout(rect=[0, 0.03, 1, 0.96])
plt.savefig("las_vegas_2025_prediction.png", dpi=300, bbox_inches='tight')
print("\n📈 Visualization saved as 'las_vegas_2025_prediction.png'")
print("=" * 70)
plt.show()