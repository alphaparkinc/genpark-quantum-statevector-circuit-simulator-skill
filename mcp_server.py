import sys
import json
from client import QuantumStatevector

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "simulate_quantum_circuit",
                        "description": "Simulate quantum circuit operations (H, CNOT) and compute state probabilities",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "num_qubits": {"type": "integer", "default": 2},
                                "operations": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "gate": {"type": "string", "enum": ["H", "CNOT"]},
                                            "target": {"type": "integer"},
                                            "control": {"type": "integer"}
                                        },
                                        "required": ["gate"]
                                    }
                                }
                            },
                            "required": ["operations"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "simulate_quantum_circuit":
            n = args.get("num_qubits", 2)
            sim = QuantumStatevector(num_qubits=n)
            for op in args["operations"]:
                g = op["gate"]
                if g == "H":
                    sim.apply_hadamard(op["target"])
                elif g == "CNOT":
                    sim.apply_cnot(op["control"], op["target"])
            probs = sim.get_probabilities()
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"probabilities": probs})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if line.strip():
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
