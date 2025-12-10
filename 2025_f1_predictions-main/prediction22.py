import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=" * 70)
print("2025 BRAZIL GP RACE PREDICTION - DUAL SCENARIO ANALYSIS")
print("=" * 70)
print("☀️  SCENARIO A: DRY CONDITIONS")
print("🌧️  SCENARIO B: WET CONDITIONS (60-70% probability)")
print("=" * 70)

# --- 2025 Prediction Data (Brazil GP) ---
qualifying_2025 = pd.DataFrame({
    "Driver": ["NOR", "ANT", "LEC", "PIA", "HAD", "RUS", "HAM", "SAI", "VER"],
    "QualifyingPosition": [1, 2, 3, 4, 5, 6, 13, 15, 16],
    "QualifyingTime (s)": [  
        69.511,  69.685, 69.805, 69.886, 69.931,
        69.942, 70.100, 70.472, 70.403
    ]
})

# ===============================================
# SCENARIO A: DRY RACE ☀️
# ===============================================
print("\n" + "=" * 70)
print("☀️  SCENARIO A: DRY CONDITIONS")
print("=" * 70)

race_pace_dry = {
    "NOR": 80.8, "LEC": 80.4, "HAM": 81.0, "RUS": 81.2,
    "VER": 80.5, "ANT": 81.8, "SAI": 81.5, "PIA": 81.3, "HAD": 82.0
}

overtaking_dry = {
    "NOR": 0.2, "ANT": 0.1, "LEC": -0.8, "PIA": 0.0,
    "HAD": 0.2, "RUS": 0.0, "HAM": -0.7, "SAI": -0.5, "VER": -1.5
}

form_dry = {
    "NOR": 0.95, "LEC": 0.97, "HAM": 1.01, "RUS": 1.00,
    "VER": 1.00, "ANT": 1.02, "SAI": 1.00, "PIA": 1.00, "HAD": 1.03
}

reliability_dry = {
    "NOR": 1.00, "LEC": 1.00, "HAM": 1.00, "RUS": 1.00,
    "VER": 1.00, "ANT": 1.01, "SAI": 1.00, "PIA": 1.00, "HAD": 1.02
}

# Calculate DRY scenario
dry_results = qualifying_2025.copy()
dry_results["RacePace"] = dry_results["Driver"].map(race_pace_dry)
dry_results["OvertakingFactor"] = dry_results["Driver"].map(overtaking_dry)
dry_results["FormMultiplier"] = dry_results["Driver"].map(form_dry)
dry_results["ReliabilityFactor"] = dry_results["Driver"].map(reliability_dry)

dry_results["RaceScore"] = (
    dry_results["RacePace"] * 
    dry_results["FormMultiplier"] * 
    dry_results["ReliabilityFactor"] -
    (dry_results["OvertakingFactor"] * 0.3)
)

dry_results = dry_results.sort_values("RaceScore").reset_index(drop=True)
dry_results["PredictedPosition"] = range(1, len(dry_results) + 1)
dry_results["PositionChange"] = (
    dry_results["QualifyingPosition"] - dry_results["PredictedPosition"]
)

print("\n🏁 PREDICTED RESULTS (DRY RACE):\n")
print(dry_results[[
    "PredictedPosition", "Driver", "QualifyingPosition", "RaceScore"
]].to_string(index=False))

print("\n🏆 DRY RACE PODIUM:")
print(f"🥇 P1: {dry_results.iloc[0]['Driver']} (Quali P{dry_results.iloc[0]['QualifyingPosition']})")
print(f"🥈 P2: {dry_results.iloc[1]['Driver']} (Quali P{dry_results.iloc[1]['QualifyingPosition']})")
print(f"🥉 P3: {dry_results.iloc[2]['Driver']} (Quali P{dry_results.iloc[2]['QualifyingPosition']})")

# ===============================================
# SCENARIO B: WET RACE 🌧️ (MODERATE ADJUSTMENTS)
# ===============================================
print("\n" + "=" * 70)
print("🌧️  SCENARIO B: WET CONDITIONS (MODERATE RAIN)")
print("=" * 70)

# Wet pace - more conservative adjustments
race_pace_wet = {
    "NOR": 85.8,  # Slightly vulnerable but not terrible (+5.0s)
    "LEC": 85.5,  # Good wet pace (+5.1s)
    "HAM": 85.0,  # Rain master (+4.0s)
    "RUS": 86.2,  # Decent wet pace (+5.0s)
    "VER": 84.8,  # Elite wet pace (+4.3s)
    "ANT": 87.5,  # Rookie struggles (+5.7s)
    "SAI": 86.5,  # Average wet pace (+5.0s)
    "PIA": 86.3,  # Still learning (+5.0s)
    "HAD": 87.2   # Rookie struggles
}

# Wet overtaking - more conservative
overtaking_wet = {
    "NOR": 0.3,   # Slightly more vulnerable
    "ANT": 0.6,   # Rookie vulnerable
    "LEC": -0.7,  # Good wet skills
    "PIA": 0.1,   # Slight vulnerability
    "HAD": 0.4,   # Rookie struggles
    "RUS": 0.0,   # Neutral
    "HAM": -1.0,  # Strong recovery but moderate
    "SAI": -0.5,  # Moderate recovery
    "VER": -1.3,  # Strong but not extreme recovery
}

# Wet form - moderate boosts
form_wet = {
    "NOR": 0.98,  # Mexico win but slight wet concern
    "LEC": 0.97,  # Mexico P2 + decent wet
    "HAM": 0.95,  # 5% boost for rain skills
    "RUS": 1.00,  # Neutral
    "VER": 0.94,  # 6% boost for rain excellence
    "ANT": 1.06,  # 6% penalty for rookie in rain
    "SAI": 1.01,  # Slight penalty
    "PIA": 1.01,  # Learning
    "HAD": 1.05   # Rookie penalty
}

reliability_wet = {
    "NOR": 1.01, "LEC": 1.00, "HAM": 1.00, "RUS": 1.00,
    "VER": 0.99, "ANT": 1.08, "SAI": 1.02, "PIA": 1.01, "HAD": 1.06
}

# Weather and Safety Car factors (moderate impact)
weather_factor = {
    "VER": -0.8, "HAM": -0.7, "NOR": 0.3, "LEC": -0.2,
    "RUS": 0.1, "ANT": 0.7, "SAI": 0.2, "PIA": 0.1, "HAD": 0.4
}

safety_car_factor = {
    "VER": -0.4, "HAM": -0.3, "SAI": -0.3, "LEC": -0.1,
    "NOR": 0.2, "ANT": 0.3, "RUS": 0.0, "PIA": 0.1, "HAD": 0.1
}

# Calculate WET scenario
wet_results = qualifying_2025.copy()
wet_results["RacePace"] = wet_results["Driver"].map(race_pace_wet)
wet_results["OvertakingFactor"] = wet_results["Driver"].map(overtaking_wet)
wet_results["FormMultiplier"] = wet_results["Driver"].map(form_wet)
wet_results["ReliabilityFactor"] = wet_results["Driver"].map(reliability_wet)
wet_results["WeatherFactor"] = wet_results["Driver"].map(weather_factor)
wet_results["SafetyCarFactor"] = wet_results["Driver"].map(safety_car_factor)

wet_results["RaceScore"] = (
    wet_results["RacePace"] * 
    wet_results["FormMultiplier"] * 
    wet_results["ReliabilityFactor"] -
    (wet_results["OvertakingFactor"] * 0.35) +
    wet_results["WeatherFactor"] +
    wet_results["SafetyCarFactor"]
)

wet_results = wet_results.sort_values("RaceScore").reset_index(drop=True)
wet_results["PredictedPosition"] = range(1, len(wet_results) + 1)
wet_results["PositionChange"] = (
    wet_results["QualifyingPosition"] - wet_results["PredictedPosition"]
)

print("\n🏁 PREDICTED RESULTS (WET RACE):\n")
print(wet_results[[
    "PredictedPosition", "Driver", "QualifyingPosition", "RaceScore"
]].to_string(index=False))

print("\n🏆 WET RACE PODIUM:")
print(f"🥇 P1: {wet_results.iloc[0]['Driver']} (Quali P{wet_results.iloc[0]['QualifyingPosition']})")
print(f"🥈 P2: {wet_results.iloc[1]['Driver']} (Quali P{wet_results.iloc[1]['QualifyingPosition']})")
print(f"🥉 P3: {wet_results.iloc[2]['Driver']} (Quali P{wet_results.iloc[2]['QualifyingPosition']})")

# ===============================================
# COMPARISON & ANALYSIS
# ===============================================
print("\n" + "=" * 70)
print("📊 SCENARIO COMPARISON")
print("=" * 70)

# Create proper comparison by merging on Driver
dry_comparison = dry_results[["Driver", "QualifyingPosition", "PredictedPosition"]].copy()
dry_comparison.columns = ["Driver", "Qualifying", "Dry Finish"]

wet_comparison = wet_results[["Driver", "PredictedPosition"]].copy()
wet_comparison.columns = ["Driver", "Wet Finish"]

comparison = pd.merge(dry_comparison, wet_comparison, on="Driver")
comparison["Difference"] = comparison["Wet Finish"] - comparison["Dry Finish"]
comparison = comparison.sort_values("Qualifying")

print("\n" + comparison.to_string(index=False))

print("\n🔑 KEY INSIGHTS:")
print("\nDRY RACE (40% probability):")
biggest_gainer_dry = dry_results.sort_values("PositionChange", ascending=False).iloc[0]
print(f"   • Biggest Gainer: {biggest_gainer_dry['Driver']} "
      f"(P{int(biggest_gainer_dry['QualifyingPosition'])} → "
      f"P{int(biggest_gainer_dry['PredictedPosition'])}, "
      f"+{int(biggest_gainer_dry['PositionChange'])})")
print(f"   • Strategy: Standard race, overtaking crucial")

print("\nWET RACE (60% probability):")
biggest_gainer_wet = wet_results.sort_values("PositionChange", ascending=False).iloc[0]
print(f"   • Biggest Gainer: {biggest_gainer_wet['Driver']} "
      f"(P{int(biggest_gainer_wet['QualifyingPosition'])} → "
      f"P{int(biggest_gainer_wet['PredictedPosition'])}, "
      f"+{int(biggest_gainer_wet['PositionChange'])})")
print(f"   • Strategy: Wet tires, rain masters benefit, rookies struggle")

print("\n🎯 MOST LIKELY OUTCOME (Based on 60-70% rain forecast):")
print(f"   🥇 P1: {wet_results.iloc[0]['Driver']}")
print(f"   🥈 P2: {wet_results.iloc[1]['Driver']}")
print(f"   🥉 P3: {wet_results.iloc[2]['Driver']}")

# ===============================================
# VISUALIZATION
# ===============================================
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("2025 BRAZIL GP - DUAL SCENARIO PREDICTION", fontsize=16, fontweight='bold')

# 1. Side-by-side podium comparison
ax1 = axes[0, 0]
scenarios = ['DRY', 'WET']
p1_pos = [dry_results.iloc[0]['PredictedPosition'], wet_results.iloc[0]['PredictedPosition']]
p2_pos = [dry_results.iloc[1]['PredictedPosition'], wet_results.iloc[1]['PredictedPosition']]
p3_pos = [dry_results.iloc[2]['PredictedPosition'], wet_results.iloc[2]['PredictedPosition']]

x = np.arange(len(scenarios))
width = 0.25
ax1.bar(x - width, [1, 1], width, label=f"P1: {dry_results.iloc[0]['Driver']} / {wet_results.iloc[0]['Driver']}", color='gold')
ax1.bar(x, [1, 1], width, label=f"P2: {dry_results.iloc[1]['Driver']} / {wet_results.iloc[1]['Driver']}", color='silver')
ax1.bar(x + width, [1, 1], width, label=f"P3: {dry_results.iloc[2]['Driver']} / {wet_results.iloc[2]['Driver']}", color='chocolate')
ax1.set_ylabel('Podium Position', fontsize=11)
ax1.set_title('Predicted Podiums: Dry vs Wet', fontsize=12, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(scenarios)
ax1.legend()
ax1.set_ylim(0, 1.5)

# 2. Position comparison for all drivers
ax2 = axes[0, 1]
drivers = comparison["Driver"]
x_pos = np.arange(len(drivers))
ax2.plot(x_pos, comparison["Dry Finish"], 'o-', label='Dry Scenario', linewidth=2, markersize=8, color='orange')
ax2.plot(x_pos, comparison["Wet Finish"], 's-', label='Wet Scenario', linewidth=2, markersize=8, color='blue')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(drivers, rotation=45)
ax2.set_ylabel('Predicted Position', fontsize=11)
ax2.set_title('Dry vs Wet Finishing Positions', fontsize=12, fontweight='bold')
ax2.legend()
ax2.invert_yaxis()
ax2.grid(alpha=0.3)

# 3. Position changes comparison
ax3 = axes[1, 0]
dry_changes = dry_results.sort_values("Driver")["PositionChange"].values
wet_changes = wet_results.sort_values("Driver")["PositionChange"].values
drivers_sorted = dry_results.sort_values("Driver")["Driver"].values

x_pos = np.arange(len(drivers_sorted))
width = 0.35
ax3.barh(x_pos - width/2, dry_changes, width, label='Dry', color='orange', alpha=0.7)
ax3.barh(x_pos + width/2, wet_changes, width, label='Wet', color='blue', alpha=0.7)
ax3.set_yticks(x_pos)
ax3.set_yticklabels(drivers_sorted)
ax3.set_xlabel('Position Change', fontsize=11)
ax3.set_title('Position Changes: Dry vs Wet', fontsize=12, fontweight='bold')
ax3.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
ax3.legend()
ax3.grid(alpha=0.3, axis='x')

# 4. Weather impact factor
ax4 = axes[1, 1]
impact = comparison.copy()
impact["WeatherImpact"] = abs(impact["Difference"])
impact = impact.sort_values("WeatherImpact", ascending=False)
colors = ['darkred' if x >= 3 else 'orange' if x >= 1 else 'lightgreen' for x in impact["WeatherImpact"]]
ax4.barh(impact["Driver"], impact["WeatherImpact"], color=colors)
ax4.set_xlabel('Position Swing (Dry vs Wet)', fontsize=11)
ax4.set_title('Weather Impact on Each Driver', fontsize=12, fontweight='bold')
ax4.invert_yaxis()
ax4.grid(alpha=0.3, axis='x')

plt.tight_layout(rect=[0, 0.03, 1, 0.96])
plt.savefig("brazil_2025_dual_scenario.png", dpi=300, bbox_inches='tight')
print("\n📈 Visualization saved as 'brazil_2025_dual_scenario.png'")
print("=" * 70)