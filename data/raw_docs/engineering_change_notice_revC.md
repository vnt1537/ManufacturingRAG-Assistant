# Engineering Change Notice
Document ID: ECN-MH-204-C
Affected Component: Servo Motor Housing Assembly
Previous Revision: B
New Revision: C
Release Date: 2026-03-05
Requested By: Product Engineering
Approved By: S. Wagner

## 1. Reason for Change
Recurring field feedback indicated insufficient robustness of inspection intervals for torque verification and occasional ambiguity in cosmetic surface acceptance for externally visible non-customer-facing surfaces.

## 2. Summary of Changes
### Change 1: Torque Verification Frequency
Previous requirement:
Torque verification at batch start and every 2 hours during production

New requirement:
Torque verification at batch start and every 1 hour during production

Rationale:
Reduced interval improves early detection of tool drift and reduces batch-level rework risk.

### Change 2: Surface Classification Clarification
Previous wording:
Externally visible non-functional outer surfaces classified under general cosmetic acceptance

New wording:
Externally visible non-customer-facing surfaces shall be explicitly classified as Class B surfaces

Rationale:
Removes interpretation differences between line inspectors and final quality inspectors.

### Change 3: Batch Start Inspection Clarification
Previous wording:
First article inspection mandatory for first 5 parts of each new batch

New wording:
First article inspection mandatory for first 5 parts of each new batch and first 3 parts after any tool replacement affecting critical dimensions

Rationale:
Additional check reduces risk after tooling interventions.

## 3. Impact Assessment
### Documents Requiring Update
- Product Specification Sheet PS-MH-204
- Quality Inspection Checklist QIC-MH-204
- SOP-ALB-017 where verification frequency is referenced

### Production Impact
No change to part geometry, material, or approved torque range.
No ERP material master update required.
Operator retraining required before release of Revision C.

### Inventory Impact
Existing Revision B stock may continue to be used if geometry and labeling remain compliant.
Process controls shall follow Revision C from effective release date onward.

## 4. Effective Date
Revision C process controls become mandatory on 2026-03-12 for all new production batches.

## 5. Implementation Actions
- Update controlled documents
- Retrain production and quality personnel
- Replace outdated line copies
- Verify torque log sheet reflects 1-hour verification frequency
- Audit first 3 batches after implementation

## 6. Approval Notes
This change does not affect torque range, material specification, or dimensional tolerances.
This change only affects process control, inspection interpretation, and verification frequency.