# -*- coding: utf-8 -*-
import sys, json
from client import OpenClawGenParkSourcing

client = OpenClawGenParkSourcing()

TOOLS = [
    {
        "name": "evaluate_topsis_suppliers",
        "description": "Executes TOPSIS multi-criteria decision analysis across supplier candidates.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "supplier_candidates": {"type": "array", "items": {"type": "object"}},
                "criteria_weights": {"type": "object"}
            },
            "required": ["supplier_candidates"]
        }
    },
    {
        "name": "fit_volume_discount_curve",
        "description": "Fits power-law volume discount elasticity curve across quote tiers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "quote_tiers": {"type": "array", "items": {"type": "object"}}
            },
            "required": ["quote_tiers"]
        }
    },
    {
        "name": "assess_supplier_disruption_risk",
        "description": "Calculates composite supply chain disruption hazard index and resilience rating.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "geographic_concentration": {"type": "number"},
                "financial_stability_score": {"type": "number"},
                "lead_time_variance": {"type": "number"}
            },
            "required": ["geographic_concentration", "financial_stability_score", "lead_time_variance"]
        }
    }
]

def handle_request(req):
    method = req.get("method")
    rid = req.get("id")
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    elif method == "tools/call":
        params = req.get("params", {})
        tname = params.get("name")
        args = params.get("arguments", {})
        if tname == "evaluate_topsis_suppliers":
            res = client.evaluate_topsis_suppliers(args["supplier_candidates"], args.get("criteria_weights"))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "fit_volume_discount_curve":
            res = client.fit_volume_discount_curve(args["quote_tiers"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "assess_supplier_disruption_risk":
            res = client.assess_supplier_disruption_risk(args["geographic_concentration"], args["financial_stability_score"], args["lead_time_variance"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32600, "message": "Invalid Request"}}

def main():
    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
