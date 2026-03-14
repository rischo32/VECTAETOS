name: Epistemic Observatory

on:
  push:
    branches:
      - main

permissions:
  contents: write
  pull-requests: write

jobs:

  observatory:

    runs-on: ubuntu-latest

    steps:

      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip

      - name: Generate ontology hash
        run: |
          python scripts/generate_ontology_hash.py

      - name: Update epistemic observatory
        run: |
          python scripts/ontology_observatory.py

      - name: Epistemic Drift Detection
        run: |
          python scripts/epistemic_drift.py || true

      - name: Φ Field Monitor
        run: |
          python scripts/phi_field_monitor.py || true

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v6
        with:
          commit-message: update epistemic observatory
          title: Epistemic Observatory Update
          body: |
            Automated update of:
            - ontology hash
            - observatory timeline
            - drift metrics
            - Φ field state
          branch: observatory-update
          delete-branch: true
