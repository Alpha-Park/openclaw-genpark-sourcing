# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Sourcing - TOPSIS Multi-Criteria Supplier Selection & Volume Elasticity Curve
Standard Library only: math, typing.
Calculates multi-criteria TOPSIS relative closeness to ideal solutions across suppliers,
fits power-law volume discount elasticity curves, and evaluates geopolitical disruption risk indices.
"""

import math
from typing import Dict, List, Any

class OpenClawGenParkSourcing:
    def __init__(self):
        self.default_weights = {
            "unit_price": 0.35,       # cost (minimize)
            "defect_rate": 0.25,      # cost (minimize)
            "lead_time_days": 0.20,   # cost (minimize)
            "reliability_score": 0.20 # benefit (maximize)
        }

    def evaluate_topsis_suppliers(self, supplier_candidates: List[Dict[str, Any]],
                                  criteria_weights: Dict[str, float] = None) -> Dict[str, Any]:
        """
        Executes TOPSIS multi-criteria decision analysis across supplier candidates:
        C_i* = D_i^- / (D_i^* + D_i^-) where D^* is distance to Positive Ideal Solution.
        """
        if not supplier_candidates:
            return {"error": "Empty supplier list"}

        weights = criteria_weights or self.default_weights
        criteria_keys = list(weights.keys())

        # Vector normalization denominators: sqrt( sum_i x_ij^2 )
        denoms = {}
        for c in criteria_keys:
            sq_sum = sum(float(s.get(c, 1.0)) ** 2 for s in supplier_candidates)
            denoms[c] = math.sqrt(max(1e-9, sq_sum))

        # Normalized weighted values
        norm_matrix = []
        for s in supplier_candidates:
            row = {}
            for c in criteria_keys:
                raw_val = float(s.get(c, 1.0))
                norm_val = (raw_val / denoms[c]) * weights[c]
                row[c] = norm_val
            norm_matrix.append(row)

        # Ideal Positive (A*) and Ideal Negative (A-)
        # unit_price, defect_rate, lead_time_days are costs (min is ideal)
        # reliability_score is benefit (max is ideal)
        cost_criteria = {"unit_price", "defect_rate", "lead_time_days"}
        ideal_pos = {}
        ideal_neg = {}

        for c in criteria_keys:
            vals = [row[c] for row in norm_matrix]
            if c in cost_criteria:
                ideal_pos[c] = min(vals)
                ideal_neg[c] = max(vals)
            else:
                ideal_pos[c] = max(vals)
                ideal_neg[c] = min(vals)

        # Compute Euclidean distances D* and D-
        rankings = []
        for idx, row in enumerate(norm_matrix):
            d_pos = math.sqrt(sum((row[c] - ideal_pos[c]) ** 2 for c in criteria_keys))
            d_neg = math.sqrt(sum((row[c] - ideal_neg[c]) ** 2 for c in criteria_keys))
            closeness = d_neg / max(1e-9, (d_pos + d_neg))

            cand = supplier_candidates[idx]
            rankings.append({
                "supplier_id": cand.get("supplier_id", f"sup_{idx+1}"),
                "name": cand.get("name", "Unknown"),
                "topsis_score": round(closeness, 4),
                "distance_to_ideal": round(d_pos, 4),
                "distance_to_anti_ideal": round(d_neg, 4)
            })

        rankings.sort(key=lambda x: x["topsis_score"], reverse=True)

        return {
            "suppliers_evaluated_count": len(supplier_candidates),
            "top_supplier_selection": rankings[0]["supplier_id"],
            "top_supplier_name": rankings[0]["name"],
            "topsis_rankings": rankings
        }

    def fit_volume_discount_curve(self, quote_tiers: List[Dict[str, float]]) -> Dict[str, Any]:
        """
        Fits power-law volume discount elasticity: P(Q) = a * Q^(-b)
        ln(P) = ln(a) - b * ln(Q) via linear regression.
        """
        valid = [q for q in quote_tiers if q.get("quantity", 0) > 0 and q.get("unit_price", 0) > 0]
        if len(valid) < 2:
            return {"error": "Need at least 2 quote tiers"}

        ln_Q = [math.log(float(q["quantity"])) for q in valid]
        ln_P = [math.log(float(q["unit_price"])) for q in valid]

        mean_q = sum(ln_Q) / len(ln_Q)
        mean_p = sum(ln_P) / len(ln_P)

        cov_qp = sum((q - mean_q) * (p - mean_p) for q, p in zip(ln_Q, ln_P))
        var_q = sum((q - mean_q) ** 2 for q in ln_Q)

        slope_neg_b = cov_qp / max(1e-9, var_q)
        intercept_ln_a = mean_p - slope_neg_b * mean_q

        b_elasticity = -slope_neg_b
        a_baseline_price = math.exp(intercept_ln_a)

        return {
            "baseline_unit_price_a": round(a_baseline_price, 4),
            "volume_discount_elasticity_b": round(b_elasticity, 4),
            "is_discount_convex": b_elasticity > 0,
            "fitted_formula": f"Unit Price = {a_baseline_price:.2f} * Quantity^(-{b_elasticity:.3f})"
        }

    def assess_supplier_disruption_risk(self, geographic_concentration: float,
                                        financial_stability_score: float,
                                        lead_time_variance: float) -> Dict[str, Any]:
        """
        Calculates composite supply chain disruption hazard index [0, 100].
        """
        geo_hazard = min(1.0, max(0.0, geographic_concentration)) * 40.0
        fin_hazard = (1.0 - min(1.0, max(0.0, financial_stability_score))) * 35.0
        variance_hazard = min(1.0, max(0.0, lead_time_variance / 30.0)) * 25.0

        total_risk = geo_hazard + fin_hazard + variance_hazard

        if total_risk <= 30.0:
            rating = "TIER_A_RESILIENT_SUPPLIER"
        elif total_risk <= 60.0:
            rating = "TIER_B_MODERATE_SUPPLY_CHAIN_RISK"
        else:
            rating = "TIER_C_HIGH_DISRUPTION_HAZARD"

        return {
            "composite_disruption_risk_score": round(total_risk, 2),
            "resilience_rating": rating,
            "components": {
                "geographic_concentration_hazard": round(geo_hazard, 2),
                "financial_default_hazard": round(fin_hazard, 2),
                "lead_time_volatility_hazard": round(variance_hazard, 2)
            }
        }
