import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set style
plt.style.use('ggplot')

# ===============================================
# HEADER AND SCENARIO
# ===============================================
print("=" * 70)
print("🇶🇦 2025 QATAR GP PREDICTION - FINAL RACE DAY MODEL 🇶🇦")
print("=" * 70)
print("☀️ SCENARIO: WARM & STABLE (Max 28°C) - Tire Wear CRITICAL")
print("🔧 REGULATION: Mandatory 25-Lap Stint Limit (Pure Pace Race)")
print("🚀 STRATEGY: 100% Push, Clean Air is King")
print("=" * 70)

# ===============================================
# 1. DATA INPUT (Qualifying Focus)
# ===============================================
qualifying_qatar = pd.DataFrame({
    "Driver": [
        "PIA", "NOR", "VER", "RUS", "ANT", 
        "HAD", "SAI", "ALO", "GAS", "LEC"
    ],
    "QualifyingPosition": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "QualifyingGap": [0.00, 0.10, 0.25, 0.26, 0.45, 0.70, 0.85, 0.95, 1.00, 1.10]
})

# ===============================================
# 2. MODEL PARAMETERS (ADJUSTED FOR WARM TRACK)
# ===============================================

# RACE PACE (Lower is Faster) - Adjusted for Warm Track Wear
race_pace_qatar = {
    "PIA": 94.8, # P1 Clean Air Bonus
    "NOR": 94.9, # P2 Clean Air (mostly)
    "VER": 95.1, # Excellent tire management in heat
    "RUS": 95.3, # ADJUSTED: Penalty for warm track tire deg
    "ANT": 95.6, # ADJUSTED: Penalty for warm track tire deg
    "HAD": 96.0, 
    "SAI": 96.2, 
    "ALO": 96.3, 
    "GAS": 96.4, 
    "LEC": 96.6  # ADJUSTED: Penalty for Ferrari tire inconsistency in warm temps
}

# Traffic/Dirty Air Penalty (Crucial at Lusail)
traffic_penalty = {
    "PIA": 0.00, "NOR": 0.05, "VER": 0.20, "RUS": 0.25, "ANT": 0.30,
    "HAD": 0.40, "SAI": 0.50, "ALO": 0.50, "GAS": 0.60, "LEC": 0.70
}

# Form / Driver Confidence (Piastri on Pole = High Confidence)
form_qatar = {
    "PIA": 0.98, "NOR": 0.99, "VER": 1.00, "RUS": 1.00, "ANT": 1.02,
    "HAD": 1.01, "SAI": 1.00, "ALO": 1.00, "GAS": 1.00, "LEC": 1.05
}

# ===============================================
# 3. CALCULATION
# ===============================================
qatar_results = qualifying_qatar.copy()
qatar_results["RacePace"] = qatar_results["Driver"].map(race_pace_qatar)
qatar_results["TrafficPenalty"] = qatar_results["Driver"].map(traffic_penalty)
qatar_results["Form"] = qatar_results["Driver"].map(form_qatar)

# Formula: Pace * Form + Traffic Penalty
qatar_results["RaceScore"] = (
    qatar_results["RacePace"] * qatar_results["Form"] + 
    qatar_results["TrafficPenalty"]
)

qatar_results = qatar_results.sort_values("RaceScore").reset_index(drop=True)
qatar_results["PredictedPosition"] = range(1, len(qatar_results) + 1)
qatar_results["PositionChange"] = qatar_results["QualifyingPosition"] - qatar_results["PredictedPosition"]

# ===============================================
# 4. TEXT OUTPUT
# ===============================================
print("\n🏁 PREDICTED RESULTS (QATAR GP - WARM & STABLE):\n")
print(qatar_results[[
    "PredictedPosition", "Driver", "QualifyingPosition", "RaceScore"
]].to_string(index=False))

print("\n" + "=" * 70)
print("🏆 QATAR GP PODIUM PREDICTION")
print("=" * 70)
print(f"🥇 P1: {qatar_results.iloc[0]['Driver']} (Start: P{qatar_results.iloc[0]['QualifyingPosition']})")
print(f"🥈 P2: {qatar_results.iloc[1]['Driver']} (Start: P{qatar_results.iloc[1]['QualifyingPosition']})")
print(f"🥉 P3: {qatar_results.iloc[2]['Driver']} (Start: P{qatar_results.iloc[2]['QualifyingPosition']})")

print("\n🔮 ANALYSIS:")
if qatar_results.iloc[0]['Driver'] == "PIA":
    print("Analysis: Piastri converts Pole to Victory! The 'Clean Air' advantage")
    print("at Lusail allows him to dictate the pace while Norris and Verstappen")
    print("fight in his wake. Verstappen is unable to split the McLarens due to")
    print("the slight pace degradation of the Mercedes behind him.")

# ===============================================
# 5. VISUALIZATION DASHBOARD
# ===============================================
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("2025 QATAR GP - FINAL PREDICTION DASHBOARD", fontsize=18, fontweight='bold', color='darkred')

# --- Chart 1: The Podium (Top 3) ---
ax1 = axes[0, 0]
top3 = qatar_results.head(3)
colors = ['gold', 'silver', 'chocolate']
ax1.bar(top3["Driver"], [3, 2, 1], color=colors, alpha=0.8)
ax1.set_ylim(0, 4)
ax1.set_yticks([])
ax1.set_title('Predicted Podium (P1 - P2 - P3)', fontsize=12, fontweight='bold')
for i, rect in enumerate(ax1.patches):
    height = rect.get_height()
    ax1.text(rect.get_x() + rect.get_width()/2., height - 0.5,
             f"P{i+1}\n{top3.iloc[i]['Driver']}",
             ha='center', va='bottom', fontsize=14, fontweight='bold', color='black')

# --- Chart 2: Grid Evolution (Quali vs Race) ---
ax2 = axes[0, 1]
grid_order = qatar_results.sort_values("QualifyingPosition")
ax2.plot(grid_order["Driver"], grid_order["QualifyingPosition"], 'o--', color='gray', label='Start (Quali)')
ax2.plot(grid_order["Driver"], grid_order["PredictedPosition"], 's-', color='darkred', linewidth=2, label='Finish (Pred)')
ax2.invert_yaxis()
ax2.set_title('Race Evolution: Start vs Finish', fontsize=12, fontweight='bold')
ax2.set_ylabel('Position')
ax2.legend()
ax2.grid(True, alpha=0.3)

# --- Chart 3: Impact of Traffic/Warmth Penalty ---
ax3 = axes[1, 0]
# Combined factors of TrafficPenalty + (Form * RacePace - Base RacePace)
# Let's just focus on the Traffic Penalty as it's the biggest variable differentiator
ax3.bar(qatar_results["Driver"], qatar_results["TrafficPenalty"], color='maroon', alpha=0.7)
ax3.set_ylabel('Traffic/Dirty Air Penalty (Seconds)', fontsize=10)
ax3.set_title('Impact of Track Position Penalty', fontsize=12, fontweight='bold')
ax3.grid(axis='y', alpha=0.3)

# --- Chart 4: Position Gainers/Losers ---
ax4 = axes[1, 1]
changes = qatar_results.sort_values("PositionChange")
colors_gain = ['red' if x < 0 else 'green' if x > 0 else 'gray' for x in changes["PositionChange"]]
ax4.barh(changes["Driver"], changes["PositionChange"], color=colors_gain)
ax4.set_title('Net Position Changes', fontsize=12, fontweight='bold')
ax4.set_xlabel('Positions Gained (+) / Lost (-)')
ax4.axvline(0, color='black', linewidth=0.8)

plt.tight_layout(rect=[0, 0.03, 1, 0.96])
plt.savefig("qatar_2025_prediction.png", dpi=300, bbox_inches='tight')
print("\n📈 Visualization saved as 'qatar_2025_prediction.png'")
print("=" * 70)
plt.show()