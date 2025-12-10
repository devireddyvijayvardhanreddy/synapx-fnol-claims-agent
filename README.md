# FNOL Claims Processing Agent

## Overview
Autonomous Insurance Claims Processing Agent - A lightweight Python application that processes First Notice of Loss (FNOL) documents, extracts key fields, classifies claims, and routes them based on predefined rules.

## Problem Statement
Build a lightweight agent that processes FNOL (First Notice of Loss) documents:
- Extract key fields from FNOL documents (policy info, incident details, insured parties, asset details)
- Identify missing or inconsistent information
- Classify claims and route them to appropriate queues (fast-track vs manual review)
- Provide clear explanations for all decisions

## Project Structure
```
synapx-fnol-claims-agent/
├── fnol_processor.py         # Main FNOL processor class
├── claim_classifier.py        # Claim classification logic
├── routing_engine.py          # Routing rules engine
├── field_extractor.py         # Field extraction utilities
├── validator.py               # Validation and error detection
├── main.py                    # Sample execution
├── requirements.txt           # Python dependencies
├── sample_data/
│   └── sample_fnol.json      # Sample FNOL data
└── README.md
```

## Key Features

### 1. Field Extraction
Extracts the following from FNOL documents:
- **Policy Information**: Policy Number, Carrier, Line of Business, Effective Dates
- **Incident Information**: Date, Time, Location, Description
- **Insured Party Details**: Name, Contact Info, Email Address
- **Asset Details**: Asset Type, Asset ID, Estimated Damage
- **Other Mandatory Fields**: Comments, Attachments, Initial Estimate

### 2. Claim Classification
- Validates mandatory fields
- Identifies missing/inconsistent data
- Flags suspicious claims based on rules
- Classifies claim type (auto, property, liability, etc.)

### 3. Routing Rules
- **Fast-track**: Estimated damage ≤ ₹25,000, all mandatory fields present
- **Manual Review**: If mandatory fields missing or description contains keywords like "fraud", "inconsistent", "staged"
- **Investigation Flag**: High-risk indicators

### 4. Output Format (JSON)
```json
{
  "extracted_fields": {
    "policy_number": "...",
    "incident_date": "...",
    ...
  },
  "missing_fields": [],
  "validation_errors": [],
  "claim_type": "auto",
  "routing": "fast-track",
  "risk_flags": [],
  "reasoning": "Brief explanation of decisions"
}
```

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/synapx-fnol-claims-agent.git
cd synapx-fnol-claims-agent

# Install dependencies
pip install -r requirements.txt
```

## Usage

```python
from fnol_processor import FNOLProcessor
import json

# Initialize processor
processor = FNOLProcessor()

# Process FNOL document
fnol_data = {
    "policy_number": "POL123456",
    "carrier": "ABC Insurance",
    "incident_date": "2025-12-10",
    "location": "Hyderabad, India",
    "description": "Minor fender bender",
    "estimated_damage": 15000
}

result = processor.process_fnol(fnol_data)
print(json.dumps(result, indent=2))
```

## Implementation Details

### FNOLProcessor
Main class coordinating the entire processing workflow:
- Orchestrates field extraction
- Runs validation checks
- Applies classification logic
- Invokes routing decisions

### Field Extractor
Handles extraction of predefined fields from unstructured/semi-structured data

### Claim Classifier
Logic tree for categorizing claims based on patterns and risk indicators

### Routing Engine
Rule-based system for directing claims to appropriate workflows

### Validator
Checks for missing fields, data consistency, and format validation

## Technologies Used
- **Language**: Python 3.8+
- **Data Processing**: JSON, Regex
- **Libraries**: Standard library (re, json, datetime)
- **Optional**: Pandas for large-scale document processing

## AI Tool Usage
- ChatGPT/GitHub Copilot for code generation and documentation
- Used for accelerating development of extraction logic
- Leveraged for creating comprehensive test cases

## Testing
Run sample test cases:
```bash
python main.py
```

## Future Enhancements
- OCR integration for image-based FNOL documents
- ML-based field extraction using NLP
- Integration with Azure Dataverse/Power Platform
- Real-time dashboard for claims monitoring
- Batch processing for multiple FNOLs
- API endpoint for external integrations

## Assessment Submission
This project demonstrates:
- ✅ Extraction of key fields from FNOL documents
- ✅ Identification of missing/inconsistent information
- ✅ Claim classification and routing logic
- ✅ Clear decision explanations in output
- ✅ Clean, well-structured code
- ✅ Effective use of AI tools for acceleration
- ✅ Problem-solving ability and logic clarity

## Author
Developed as an assessment for Synapx Junior Software Engineer position (Hyderabad, 5 LPA)

## License
MIT License
