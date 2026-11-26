#!/usr/bin/env python3
"""Validate the planning baseline's traceability, not implementation correctness."""
import csv
import json
import re
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
errors = []
def check(condition, message):
    if not condition:
        errors.append(message)
def read(path):
    p = ROOT / path
    if not p.is_file():
        errors.append(f"missing file: {path}")
        return ""
    return p.read_text(encoding="utf-8-sig")
def main():
    for path in ("proposal.md", "design.md", "requirements-matrix.md", "tasks.md", "AGENTS.md", "README.md", "CLAUDE.md"):
        read(path)
    data = json.loads(read("docs/validation/traceability.json"))
    features = {f["id"]: f for f in data["features"]}
    check(len(features) == len(data["features"]) and len(features) >= 5, "feature IDs or count invalid")
    prd = read("docs/prd/PRD.md")
    tasks = read("tasks.md")
    catalog = read("docs/validation/test-catalog.md")
    matrix = read("requirements-matrix.md")
    release = read("docs/validation/release-contract.md")
    for f in features.values():
        check(f["id"] in prd and f["provides"] and f["consumes"], f"missing provides/consumes {f['id']}")
        for dep in f["dependsOn"]:
            check(dep in features, f"unknown dependency {dep}")
            if dep in features:
                check(features[dep]["wave"] < f["wave"], f"cycle/non-earlier dependency {dep}->{f['id']}")
        for name in ("spec.md", "plan.md", "contract.md"):
            read(f"{f['path']}/{name}")
    check(max(Counter(f["wave"] for f in features.values()).values()) >= 2, "no parallel wave")
    expected_edges = {(dep, f["id"]) for f in features.values() for dep in f["dependsOn"]}
    actual_edges = {(x["provider"], x["consumer"]) for x in data["cross"] if x["kind"] == "dependency"}
    check(expected_edges == actual_edges, f"dependency coverage mismatch {expected_edges ^ actual_edges}")
    all_items = data["criteria"] + data["cross"] + data["process"]
    ids = [c["id"] for c in all_items]
    check(len(ids) == len(set(ids)), "duplicate criteria")
    for key in ("contract", "test"):
        values = [c[key] for c in all_items]
        check(len(values) == len(set(values)), f"duplicate {key} IDs")
    rules = {r for c in all_items for r in c["rules"]}
    check({f"R{i:02}" for i in range(1, 14)} <= rules, "R01-R13 not fully covered")
    expected_rows = set()
    for c in all_items:
        ident = c["id"]
        check(re.search(rf"\b{ident}\b", prd) is not None, f"criterion absent in PRD: {ident}")
        check(c["test"] in catalog, f"test absent in catalog: {ident}")
        check(c["task"] in tasks, f"task absent: {ident}")
        fid = c.get("feature", c.get("consumer"))
        contract = read(f"{features[fid]['path']}/contract.md") if fid in features else release
        check(c["contract"] in contract and ident in contract, f"contract mapping missing: {ident}")
        if fid in features:
            check(ident in read(f"{features[fid]['path']}/plan.md") or c["task"] in tasks, f"plan/task absent {ident}")
        for rule in c["rules"]:
            expected_rows.add((rule, ident, c["contract"], c["test"], c["task"]))
            check(f"| {rule} | {ident} |" in matrix, f"markdown row missing: {rule}/{ident}")
    with (ROOT / "requirements-matrix.csv").open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    actual_rows = {(r["Requisito"],r["Critério PRD"],r["Item contrato"],r["Teste"],r["Tarefa"]) for r in rows}
    check(actual_rows == expected_rows and len(rows) == len(expected_rows), "CSV rows inconsistent")
    state = json.loads(read("state/project-state.json"))
    check({f["id"] for f in state["features"]} == set(features), "state feature set mismatch")
    for f in state["features"]:
        report = f.get("latestEvaluation")
        if report:
            path = (ROOT / report).resolve()
            check(path.is_relative_to(ROOT) and path.is_file(), f"missing/unsafe report {report}")
        if f["status"] == "completed":
            check(bool(report and f.get("mergedCommit") and f.get("pr")), f"completed without evidence: {f['id']}")
        if f["status"] == "planned":
            check(report is None and f.get("implementationCommit") is None, f"planned feature has fake/early evidence: {f['id']}")
    for name in re.findall(r"`([a-z]+(?:-[a-z]+)+)`", tasks):
        if name in {"prd-and-traceability","architecture-review","wave-coordinator","independent-evaluator","integration-release"}:
            read(f".agents/skills/{name}/SKILL.md")
    for skill in ("harness","implement-feature","secure-web","transactional-domain","partner-contract"):
        read(f".agents/skills/{skill}/SKILL.md")
    if errors:
        for error in errors:
            print("FAIL:", error, file=sys.stderr)
        return 1
    print(f"PASS docs: {len(features)} features, {len(data['criteria'])} local criteria, {len(data['cross'])} cross criteria, {len(data['process'])} process criteria, {len(expected_edges)} edges, {len(rows)} traceability rows.")
    print("Structural validation only; no product, API, Mermaid rendering, GitHub history or independent evaluation was tested.")
    return 0
if __name__ == "__main__":
    sys.exit(main())
