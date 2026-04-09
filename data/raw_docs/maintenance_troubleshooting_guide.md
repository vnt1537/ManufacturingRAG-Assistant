# Maintenance and Troubleshooting Guide
Document ID: MTG-ALB-017
Equipment: Assembly Line B Torque and Housing Fit Station
Revision: A
Effective Date: 2026-03-01
Department: Maintenance Engineering
Approved By: J. Hoffmann

## 1. Purpose
This guide supports troubleshooting of recurring issues during assembly of MH-204-A servo motor housing units on Assembly Line B.

## 2. Common Fault Conditions
### Fault 1: Torque below lower limit
Symptom:
Measured torque below 9.5 Nm during verification

Possible causes:
- torque program not loaded correctly
- worn screwdriver bit
- calibration drift
- incorrect screw type
- thread contamination

Required actions:
1. Verify torque program setting is 10.0 Nm nominal
2. Inspect screwdriver bit for wear
3. Verify screw batch and part number
4. Clean thread area if contamination is present
5. Repeat verification with approved torque checker
6. If failure persists for two consecutive checks, stop production and notify maintenance

### Fault 2: Torque above upper limit
Symptom:
Measured torque above 10.5 Nm

Possible causes:
- incorrect program selected
- tool controller malfunction
- operator override
- misconfigured tool parameter after restart

Required actions:
1. Stop line for immediate tool verification
2. Compare active program with approved process setting
3. Lock tool until maintenance release is complete
4. Reinspect last 10 assemblies produced since previous accepted check

### Fault 3: Cover not flush after tightening
Symptom:
Visible gap around housing cover perimeter

Possible causes:
- seal twisted during placement
- cover misalignment
- burr on sealing edge
- foreign particle trapped on sealing face

Required actions:
1. Disassemble unit
2. Inspect seal and groove
3. Measure burr height
4. Clean sealing face
5. Reassemble using standard diagonal tightening sequence

### Fault 4: Repeated burr-related rejects
Symptom:
Burr height exceeds 0.05 mm on multiple parts in same batch

Possible causes:
- upstream machining tool wear
- deburring process deviation
- incorrect raw material edge condition

Required actions:
1. Quarantine affected batch
2. Inform machining supervisor
3. Inspect previous 20 parts
4. Start containment inspection at 100 percent until release by quality

## 3. Preventive Maintenance Schedule
- Torque screwdriver calibration verification: weekly
- Bit replacement inspection: every Monday and Thursday
- Fixture alignment check: weekly
- Tool controller backup verification: monthly
- Air supply moisture inspection: weekly

## 4. Escalation Matrix
Production Operator:
Initiates first check and informs line leader

Line Leader:
Stops production if repeated failure occurs

Quality Engineer:
Reviews suspect parts and disposition actions

Maintenance Technician:
Verifies tool, calibration, controller settings, and fixture condition

Production Engineering:
Approves process restart if root cause affects standard work

## 5. Documentation Requirements
Every maintenance-related stop shall record:
- date and time
- line and station
- fault type
- batch affected
- immediate action taken
- release signature before restart