epistemic-shield/
+ ├── README.md
+ ├── BOUNDARY_COMPLIANCE_NOTE.md
+ ├── ARCHITECTURE.md
+ ├── IMPLEMENTATION_GUIDE.md
+ ├── USER_GUIDE.md
+ │
+ ├── src/
+ │   ├── __init__.py
+ │   ├── core/
+ │   │   ├── document_parser.py
+ │   │   ├── pattern_detector.py
+ │   │   ├── finding_classifier.py
+ │   │   └── indicator_mapper.py
+ │   ├── modules/
+ │   │   ├── module_A_hidden_authority.py
+ │   │   ├── module_B_semantic_drift.py
+ │   │   ├── module_C_prescriptive_drift.py
+ │   │   ├── module_D_self_reference.py
+ │   │   └── module_E_representability_risk.py
+ │   ├── guardrails/
+ │   │   ├── operation_validator.py
+ │   │   ├── non_authoritative_validator.py
+ │   │   └── defensive_boundary_validator.py
+ │   ├── humility/
+ │   │   └── humility_injector.py
+ │   └── report_generator.py
+ │
+ ├── tests/
+ │   ├── test_modules/
+ │   ├── test_guardrails/
+ │   ├── test_humility/
+ │   ├── evaluation_set/
+ │   │   ├── safe_inputs/
+ │   │   └── boundary_inputs/
+ │   └── conftest.py
+ │
+ ├── data/
+ │   ├── evaluation_cases.json
+ │   └── example_documents/
+ │
+ └── docs/
  +  ├── EXAMPLE_OUTPUTS.md
  +  └── API_REFERENCE.md
