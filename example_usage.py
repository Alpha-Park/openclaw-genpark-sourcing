# -*- coding: utf-8 -*-
from client import OpenClawGenParkSourcing

sourcing = OpenClawGenParkSourcing()

# 1. TOPSIS Supplier Selection
candidates = [
    {"supplier_id": "sup_alpha", "name": "Apex Microchips", "unit_price": 42.0, "defect_rate": 0.008, "lead_time_days": 14, "reliability_score": 0.96},
    {"supplier_id": "sup_beta", "name": "Boreal Foundry", "unit_price": 38.0, "defect_rate": 0.025, "lead_time_days": 28, "reliability_score": 0.88},
    {"supplier_id": "sup_gamma", "name": "Cascade Silicon", "unit_price": 45.0, "defect_rate": 0.005, "lead_time_days": 10, "reliability_score": 0.99}
]
topsis = sourcing.evaluate_topsis_suppliers(candidates)
print(f"Top Supplier Selected: {topsis['top_supplier_name']} (TOPSIS Closeness: {topsis['topsis_rankings'][0]['topsis_score']})")

# 2. Volume Discount Curve
quote_tiers = [
    {"quantity": 100, "unit_price": 50.0},
    {"quantity": 500, "unit_price": 42.0},
    {"quantity": 2500, "unit_price": 34.0},
    {"quantity": 10000, "unit_price": 28.0}
]
curve = sourcing.fit_volume_discount_curve(quote_tiers)
print(f"\nVolume Curve: {curve['fitted_formula']} (Elasticity b={curve['volume_discount_elasticity_b']})")

# 3. Disruption Risk
risk = sourcing.assess_supplier_disruption_risk(geographic_concentration=0.75, financial_stability_score=0.85, lead_time_variance=12.0)
print(f"\nDisruption Risk Score: {risk['composite_disruption_risk_score']}/100 ({risk['resilience_rating']})")
