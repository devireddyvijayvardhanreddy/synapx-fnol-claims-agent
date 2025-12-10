#!/usr/bin/env python3
"""
FNOL Claims Processing Agent
Autonomous Insurance Claims Processing Agent - Processes FNOL documents,
extracts key fields, classifies claims, and routes them based on predefined rules.
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Tuple


class FNOLProcessor:
    """Main FNOL processor class that orchestrates the entire processing workflow."""
    
    # Mandatory fields that must be present
    MANDATORY_FIELDS = [
        'policy_number', 'carrier', 'incident_date', 'location', 
        'insured_name', 'contact_email', 'description', 'estimated_damage'
    ]
    
    # Risk keywords that flag for manual review
    RISK_KEYWORDS = ['fraud', 'staged', 'inconsistent', 'suspicious', 'unclear', 'missing']
    
    # Fast-track damage threshold
    FAST_TRACK_THRESHOLD = 25000
    
    def __init__(self):
        """Initialize the FNOL processor."""
        self.field_extractor = FieldExtractor()
        self.validator = FieldValidator()
        self.classifier = ClaimClassifier()
        self.router = RoutingEngine()
    
    def process_fnol(self, fnol_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a FNOL document through the complete workflow.
        
        Args:
            fnol_data: Dictionary containing FNOL document data
            
        Returns:
            Dictionary with extracted fields, validation results, and routing decision
        """
        # Extract fields
        extracted_fields = self.field_extractor.extract(fnol_data)
        
        # Validate fields
        missing_fields, validation_errors = self.validator.validate(extracted_fields)
        
        # Classify claim
        claim_type = self.classifier.classify(extracted_fields, fnol_data)
        
        # Route claim
        routing_decision, risk_flags = self.router.route(
            extracted_fields, missing_fields, validation_errors, claim_type
        )
        
        # Generate reasoning
        reasoning = self._generate_reasoning(
            missing_fields, validation_errors, routing_decision, risk_flags
        )
        
        # Compile result
        result = {
            "extracted_fields": extracted_fields,
            "missing_fields": missing_fields,
            "validation_errors": validation_errors,
            "claim_type": claim_type,
            "routing": routing_decision,
            "risk_flags": risk_flags,
            "reasoning": reasoning,
            "processed_at": datetime.now().isoformat()
        }
        
        return result
    
    def _generate_reasoning(self, missing_fields: List[str], 
                           validation_errors: List[str],
                           routing_decision: str,
                           risk_flags: List[str]) -> str:
        """Generate a human-readable explanation of the processing decision."""
        reasons = []
        
        if missing_fields:
            reasons.append(f"Missing fields detected: {', '.join(missing_fields)}.")
        
        if validation_errors:
            reasons.append(f"Validation issues: {'; '.join(validation_errors)}.")
        
        if risk_flags:
            reasons.append(f"Risk indicators flagged: {', '.join(risk_flags)}.")
        
        if routing_decision == "fast-track":
            reasons.append("All mandatory fields present with clean validation - routed to fast-track processing.")
        else:
            reasons.append("Manual review required due to missing/inconsistent data or risk indicators.")
        
        return " ".join(reasons) if reasons else "Claim ready for processing."


class FieldExtractor:
    """Handles extraction of predefined fields from FNOL data."""
    
    def extract(self, fnol_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and normalize key fields from FNOL document."""
        extracted = {}
        
        # Policy Information
        extracted['policy_number'] = fnol_data.get('policy_number', '').strip()
        extracted['carrier'] = fnol_data.get('carrier', '').strip()
        extracted['line_of_business'] = fnol_data.get('line_of_business', 'general').strip()
        extracted['effective_date'] = fnol_data.get('effective_date', '').strip()
        
        # Incident Information
        extracted['incident_date'] = fnol_data.get('incident_date', '').strip()
        extracted['incident_time'] = fnol_data.get('incident_time', '').strip()
        extracted['location'] = fnol_data.get('location', '').strip()
        extracted['description'] = fnol_data.get('description', '').strip()
        
        # Insured Party Details
        extracted['insured_name'] = fnol_data.get('insured_name', '').strip()
        extracted['contact_number'] = fnol_data.get('contact_number', '').strip()
        extracted['contact_email'] = fnol_data.get('contact_email', '').strip()
        
        # Asset Details
        extracted['asset_type'] = fnol_data.get('asset_type', '').strip()
        extracted['asset_id'] = fnol_data.get('asset_id', '').strip()
        extracted['estimated_damage'] = fnol_data.get('estimated_damage', 0)
        
        # Other fields
        extracted['comments'] = fnol_data.get('comments', '').strip()
        extracted['attachments'] = fnol_data.get('attachments', []) if isinstance(fnol_data.get('attachments'), list) else []
        
        return extracted


class FieldValidator:
    """Validates extracted fields for completeness and consistency."""
    
    MANDATORY_FIELDS = [
        'policy_number', 'carrier', 'incident_date', 'location',
        'insured_name', 'contact_email', 'description', 'estimated_damage'
    ]
    
    def validate(self, extracted_fields: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Validate extracted fields and return missing fields and errors."""
        missing = []
        errors = []
        
        # Check for missing mandatory fields
        for field in self.MANDATORY_FIELDS:
            if not extracted_fields.get(field) or str(extracted_fields.get(field)).strip() == '':
                missing.append(field)
        
        # Validate email format
        email = extracted_fields.get('contact_email', '')
        if email and not self._is_valid_email(email):
            errors.append(f"Invalid email format: {email}")
        
        # Validate damage estimate
        try:
            damage = float(extracted_fields.get('estimated_damage', 0))
            if damage < 0:
                errors.append("Estimated damage cannot be negative")
        except (ValueError, TypeError):
            errors.append("Estimated damage must be a number")
        
        # Validate date format
        incident_date = extracted_fields.get('incident_date', '')
        if incident_date and not self._is_valid_date(incident_date):
            errors.append(f"Invalid incident date format: {incident_date}")
        
        return missing, errors
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Check if email format is valid."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def _is_valid_date(date_str: str) -> bool:
        """Check if date string is in valid format."""
        formats = ['%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y', '%Y/%m/%d']
        for fmt in formats:
            try:
                datetime.strptime(date_str, fmt)
                return True
            except ValueError:
                continue
        return False


class ClaimClassifier:
    """Classifies claims based on patterns and risk indicators."""
    
    def classify(self, extracted_fields: Dict[str, Any], original_data: Dict[str, Any]) -> str:
        """Classify the claim type based on asset and incident details."""
        asset_type = extracted_fields.get('asset_type', '').lower()
        description = extracted_fields.get('description', '').lower()
        
        # Simple classification logic
        if 'vehicle' in asset_type or 'car' in asset_type or 'auto' in description:
            return 'automobile'
        elif 'property' in asset_type or 'building' in asset_type or 'home' in asset_type:
            return 'property'
        elif 'liability' in description:
            return 'liability'
        else:
            return 'general'


class RoutingEngine:
    """Rule-based system for directing claims to appropriate workflows."""
    
    RISK_KEYWORDS = ['fraud', 'staged', 'inconsistent', 'suspicious', 'unclear']
    FAST_TRACK_THRESHOLD = 25000
    
    def route(self, extracted_fields: Dict[str, Any], 
              missing_fields: List[str],
              validation_errors: List[str],
              claim_type: str) -> Tuple[str, List[str]]:
        """Determine routing decision and flag risks."""
        risk_flags = []
        
        # Check for missing fields
        if missing_fields:
            risk_flags.append("missing_mandatory_fields")
            return "manual-review", risk_flags
        
        # Check for validation errors
        if validation_errors:
            risk_flags.append("validation_errors")
            return "manual-review", risk_flags
        
        # Check damage threshold
        try:
            damage = float(extracted_fields.get('estimated_damage', 0))
            if damage > self.FAST_TRACK_THRESHOLD:
                risk_flags.append(f"high_damage_amount ({damage})")
                return "manual-review", risk_flags
        except (ValueError, TypeError):
            return "manual-review", risk_flags
        
        # Check for risk keywords in description
        description = extracted_fields.get('description', '').lower()
        for keyword in self.RISK_KEYWORDS:
            if keyword in description:
                risk_flags.append(f"risk_keyword_detected: {keyword}")
                return "investigation-flag", risk_flags
        
        # All checks passed - fast-track
        return "fast-track", risk_flags


if __name__ == "__main__":
    # Example usage
    sample_fnol = {
        "policy_number": "POL-2025-001234",
        "carrier": "ABC Insurance",
        "incident_date": "2025-12-10",
        "location": "Hyderabad, India",
        "insured_name": "John Doe",
        "contact_email": "john@example.com",
        "description": "Minor vehicle collision",
        "estimated_damage": 15000,
        "asset_type": "vehicle"
    }
    
    processor = FNOLProcessor()
    result = processor.process_fnol(sample_fnol)
    print(json.dumps(result, indent=2))
