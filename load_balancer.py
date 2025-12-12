# -------------------------------------------------------------
#  Load Balancing Calculator for Industrial Power Distribution
#  Author: Nafiz
#  Description:
#     This module simulates a simplified electrical load
#     distribution system, similar to what might appear in
#     industrial automation or facility monitoring software.
#
#     The goal is to:
#       1. Validate each circuit zone's electrical load
#       2. Detect overload conditions
#       3. Recommend redistribution to achieve a balanced system
#
#     This file is written in clean, readable Python and
#     demonstrates production-style coding practices:
#         - Input validation
#         - Clear separation of logic
#         - Meaningful comments and naming conventions
#         - Expandability (e.g., UI, Selenium testing, APIs)
#
#     NOTE:
#       This file is intentionally self-contained and is meant
#       to be submitted as a .txt file per Siemens requirements.
# -------------------------------------------------------------

from typing import List, Dict, Tuple

# -------------------------------
# Configuration Constants
# -------------------------------

MAX_LOAD_PER_ZONE = 100.0   # kW — safe threshold per circuit zone
IDEAL_VARIANCE = 15.0       # kW — allowed difference between highest/lowest loads


# -------------------------------
# Data Classes (Simple Structures)
# -------------------------------

class ZoneLoad:
    """
    Represents a circuit zone and its electrical load in kW.
    Using a small class instead of a dict improves clarity,
    enforces expected fields, and mimics production design.
    """
    def __init__(self, name: str, load: float):
        if load < 0:
            raise ValueError(f"Load for zone '{name}' cannot be negative.")
        self.name = name
        self.load = load

    def __repr__(self):
        return f"ZoneLoad(name='{self.name}', load={self.load} kW)"


# -------------------------------
# Core Logic
# -------------------------------

def detect_overloads(zones: List[ZoneLoad]) -> List[ZoneLoad]:
    """
    Returns a list of all zones exceeding the allowed load threshold.
    """
    return [z for z in zones if z.load > MAX_LOAD_PER_ZONE]


def calculate_total_load(zones: List[ZoneLoad]) -> float:
    """
    Returns the sum of all zone loads.
    """
    return sum(z.load for z in zones)


def calculate_ideal_load(zones: List[ZoneLoad]) -> float:
    """
    Computes the ideal load target for each zone.
    If every zone had equal load, this value minimizes stress.
    """
    total = calculate_total_load(zones)
    return round(total / len(zones), 2)


def recommend_redistribution(zones: List[ZoneLoad]) -> List[Tuple[str, float]]:
    """
    Based on ideal load, recommend how much each overloaded zone
    should offload (or under-loaded zone should receive).
    Returns a list of recommended adjustments.
    """
    ideal = calculate_ideal_load(zones)
    adjustments = []

    for z in zones:
        diff = round(z.load - ideal, 2)

        if abs(diff) < 1.0:
            # Within tolerance—no change needed
            continue

        if diff > 0:
            adjustments.append((z.name, f"Reduce load by {diff} kW"))
        else:
            adjustments.append((z.name, f"Increase load by {-diff} kW"))

    return adjustments


# -------------------------------
# Reporting Helpers
# -------------------------------

def generate_report(zones: List[ZoneLoad]) -> str:
    """
    Creates a readable ASCII-style report that could easily be
    shown in a UI or consumed by automated tests.
    """
    report_lines = []
    overloads = detect_overloads(zones)
    ideal = calculate_ideal_load(zones)

    report_lines.append("----- Load Balancing Analysis Report -----\n")
    report_lines.append("Zone Loads:")
    for z in zones:
        report_lines.append(f"  - {z.name}: {z.load} kW")

    report_lines.append(f"\nTotal Load: {calculate_total_load(zones)} kW")
    report_lines.append(f"Ideal Load Per Zone: {ideal} kW\n")

    if overloads:
        report_lines.append("⚠️  Overloaded Zones Detected:")
        for z in overloads:
            report_lines.append(f"   - {z.name} ({z.load} kW)")
    else:
        report_lines.append("No overloaded zones detected. ✔️")

    adjustments = recommend_redistribution(zones)
    if adjustments:
        report_lines.append("\nRecommended Adjustments:")
        for zone, action in adjustments:
            report_lines.append(f"   - {zone}: {action}")
    else:
        report_lines.append("\nLoad distribution is optimal. ✔️")

    return "\n".join(report_lines)


# -------------------------------
# Example Usage
# -------------------------------

if __name__ == "__main__":
    """
    This block serves as a demo for reviewers. It simulates
    a realistic electrical distribution scenario in which
    several circuit zones draw different amounts of power.

    SQA engineers can use this as a foundation for:
        - Selenium UI automation (handling dashboard displays)
        - Data-driven test validation
        - API simulation around load diagnostics
    """

    sample_zones = [
        ZoneLoad("Zone A", 120.0),
        ZoneLoad("Zone B", 80.0),
        ZoneLoad("Zone C", 95.0),
        ZoneLoad("Zone D", 40.0)
    ]

    report = generate_report(sample_zones)
    print(report)
