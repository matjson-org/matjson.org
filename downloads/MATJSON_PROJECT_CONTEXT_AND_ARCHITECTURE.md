# MatJSON Project Context and Architecture

**Status:** Working architecture and public-website starter package  
**Date:** 2026-08-24  
**Project domain:** `matjson.org`

## 1. Purpose of this document

This file preserves the design decisions, terminology, architecture, and roadmap developed for MatJSON so the project can be resumed in a new conversation or handed to another contributor without losing context.

MatJSON began with a practical engineering need: material specifications and application standards contain thousands of acceptance criteria, tests, conditions, exceptions, documentation requirements, and purchaser decisions, but these requirements are generally published only in human-readable documents. That makes consistent automation, API exchange, MTR review, and AI-assisted querying unnecessarily difficult.

MatJSON is intended to address that problem through an open, vendor-neutral family of JSON schemas.

> **Working definition:** MatJSON is an open, vendor-neutral family of JSON schemas and semantic rules for representing material specifications, application-specific material requirements, material-compliance evidence, and compliance results in a form usable by humans, APIs, automation systems, and artificial intelligence.

A concise public tagline is:

> **Material standards, structured for software.**

A supporting description is:

> **An open interchange format for material specifications, application requirements, and compliance data.**

## 2. The central idea

MatJSON should be treated as an interoperability protocol, not merely a database of files.

A database says, “Here are our material files.”

An interoperability specification says, “Here is how any organization can structure, identify, validate, reference, extend, exchange, and process material requirements.”

The long-term objective is that owner-users, manufacturers, EPCs, mills, inspection providers, software vendors, standards bodies, universities, and AI systems can produce and consume conforming MatJSON documents with reusable tools.

## 3. The MatJSON schema family

| Profile | Purpose | File extension | Current status |
| --- | --- | --- | --- |
| **MatJSON Core** | Shared values, units, provenance, expressions, selectors, citations, identifiers, vocabularies, and extension rules | Internal/common schema | Architecture defined; schema draft/TBC |
| **MatSpecJSON** | Intrinsic requirements of a material or product specification | `.matspec.json` | Working schema and draft data library exist |
| **MatReqJSON** | Additional material requirements imposed by codes, service standards, equipment standards, recommended practices, and purchaser specifications | `.matreq.json` | Working schema and draft data library exist |
| **MatRecordJSON** | Normalized representation of actual MTRs, CMTRs, test reports, and other evidence | `.matrecord.json` | Concept accepted; detailed schema TBC |
| **MatCheckJSON** | Machine-readable compliance results | `.matcheck.json` | Concept accepted; detailed schema TBC |

Only MatSpecJSON and MatReqJSON are mature enough to contain substantive engineering data today. MatJSON Core, MatRecordJSON, and MatCheckJSON are included in the website and architecture so the ecosystem has a coherent direction, but their current website schemas are placeholders and must not be treated as production standards.

## 4. Fundamental separation of responsibilities

### 4.1 MatSpecJSON

MatSpecJSON answers:

> What must a material satisfy to comply with its base material or product specification?

Typical content includes:

- material grades and classifications;
- heat and product chemistry;
- tensile and yield properties;
- elongation and reduction of area;
- hardness;
- impact properties;
- heat treatment;
- dimensional tolerances;
- required tests and test frequencies;
- certification and test reports;
- marking and traceability;
- imported general-requirement specifications;
- specification-specific ASME adoption overlays.

MatSpecJSON is grade-centric because product specifications usually define identifiable grades, classes, types, and conditions.

### 4.2 MatReqJSON

MatReqJSON answers:

> What additional, restrictive, conditional, documentary, fabrication, or service-specific material requirements are imposed by another governing document?

Typical sources include:

- equipment standards such as API 660 and API 663;
- service standards such as NACE MR0175 and MR0103;
- fabrication standards and recommended practices such as API 582 and API 934-series documents;
- technical reports or annexes when contractually invoked;
- design codes such as ASME Section VIII Divisions 1 and 2;
- purchaser specifications and special material requirements.

MatReqJSON is rule-centric rather than grade-centric. A rule has applicability, targets, activation, requirement behavior, verification evidence, and source provenance.

### 4.3 Material requisition as the project-specific source of truth

A separate MatCtxJSON profile was considered and deliberately rejected.

The material requisition, purchase specification, or special material requirement document already contains the project-specific service conditions, purchaser decisions, invoked standards, acceptance values, and exceptions. Duplicating those decisions in another context JSON would create competing sources of truth.

The intended effective-requirements stack is therefore:

```text
MatSpecJSON
    +
Invoked MatReqJSON documents
    +
Direct material requisition / purchaser requirements
    =
Effective material requirements
```

The effective requirements are then evaluated against an MTR, CMTR, and supporting reports.

## 5. Invocation and activation model

A material requisition may invoke MatReq content in several ways.

### 5.1 Whole-document invocation

Example:

```text
Material shall comply with NACE MR0175 / ISO 15156.
```

The corresponding MatReq file is loaded and all applicable rules are evaluated.

### 5.2 Scoped invocation

Example:

```text
Material shall meet API TR 938-C Appendix A.
```

Only the rules within that appendix are activated, together with dependencies explicitly required by those rules.

### 5.3 Section or clause invocation

Example:

```text
Carbon steel materials shall comply with API 663 Section 8.2.
```

The applicable rules under that section are activated.

### 5.4 Direct purchaser requirement

Example:

```text
Carbon equivalent shall not exceed 0.43.
```

This direct requisition requirement becomes part of the effective requirement set even if the source clause is not separately cited.

### 5.5 Reference-only language

References such as “see,” “refer to,” or “for guidance” should not automatically impose the entire referenced document. MatReq cross-references therefore need typed roles such as:

- `invokes_all_applicable`;
- `invokes_scoped`;
- `test_method_only`;
- `acceptance_criteria_only`;
- `definition_only`;
- `guidance_only`;
- `informative_only`.

### 5.6 Contractual elevation

An informative or example annex can become contractually mandatory when the material requisition explicitly invokes it using mandatory language. The MatReq representation must preserve both facts:

1. the source document labels the content informative or exemplary; and
2. the purchaser contractually invoked that content.

## 6. Rule model for MatReqJSON

Each atomic MatReq rule should ultimately carry these concepts:

- stable `id`;
- `category`;
- source `normativity` such as mandatory, recommended, permitted, or informative;
- project `activation` such as always, when invoked, or purchaser-defined;
- `targets`, including material families, specifications, grades, product forms, components, and weld regions;
- a Boolean `when` expression;
- typed `requirement` behavior;
- `effect` on a base MatSpec requirement;
- `verification` evidence and checkability;
- complete `source` provenance;
- maturity/review status.

Representative requirement kinds include:

- `property_limit`;
- `composition_limit`;
- `computed_limit`;
- `required_condition`;
- `required_test`;
- `required_examination`;
- `required_heat_treatment`;
- `required_product_form`;
- `required_manufacturing_route`;
- `required_document`;
- `required_report_field`;
- `required_traceability`;
- `required_marking`;
- `prohibited`;
- `allowed_only`;
- `relationship_constraint`;
- `reference_compliance`;
- `purchaser_defined`;
- `decision_procedure`.

## 7. Material components and product forms

MatJSON must keep equipment components separate from material product forms.

Examples:

| Component | Potential product forms |
| --- | --- |
| Shell | plate, pipe |
| Nozzle | pipe, forging, fabricated plate |
| Girth flange | forging, plate |
| Tubesheet | plate, forging |
| Tube | tube |
| Bolting | bar or bolting product |
| Fitting | fitting |
| Weld | weld metal / consumable |

A tubesheet is a component, not a product form. This distinction is necessary for reliable applicability and for comparing requirements with actual procurement data.

## 8. Conditions and Boolean logic

MatReq applicability often requires combinations such as:

```text
carbon steel
AND pressure retaining
AND process wetted
AND sour service
AND shell side
```

The condition model should therefore support expression trees using operators such as:

- `all`;
- `any`;
- `not`;
- `eq` and `ne`;
- `gt`, `gte`, `lt`, and `lte`;
- `in` and `not_in`;
- `exists`;
- `contains`.

This is more capable than the simpler grade-property selectors used by MatSpecJSON.

## 9. Effects on base material requirements

MatReq rules should explicitly state how they interact with MatSpec requirements. Useful relationships include:

- `supplements`;
- `restricts`;
- `replaces`;
- `requires_additional_test`;
- `requires_additional_reporting`;
- `invokes`;
- `prohibits`;
- `selects`;
- `purchaser_defined`;
- `relationship_constraint`.

The engine should not globally apply “whichever is more stringent.” That resolution is valid only when a governing source explicitly requires it or when the requirements are mathematically comparable under a defined merge rule.

## 10. Formulas and computed properties

Material compliance frequently depends on calculated quantities, including:

- carbon equivalent;
- PREN;
- J-factor;
- X-bar;
- Larson-Miller parameters;
- stabilization ratios;
- elemental sums;
- hydrostatic formulas;
- elongation equations.

MatJSON Core should eventually provide a safe, typed expression model with declared inputs, units, rounding, and source provenance. Free-text formulas are not sufficient for deterministic automation.

## 11. Decision procedures and dependencies

Some requirements cannot be represented as one static limit.

Examples include:

- ASME VIII-1 UCS-66 impact-test exemptions;
- UG-84 impact-test procedures;
- UHA-51 high-alloy toughness requirements;
- ASME VIII-2 Part 3 material toughness rules;
- NACE environmental service envelopes;
- API 941 Nelson curves.

These require executable decision graphs, table lookups, curve datasets, branch logic, exemptions, and rule dependencies.

## 12. Verification and evidence

Every requirement should indicate what evidence can demonstrate compliance. Common evidence classes include:

- MTR / CMTR;
- certificate of compliance;
- chemistry report;
- PMI report;
- NDE report;
- hardness report;
- impact report;
- heat-treatment chart;
- WPS;
- PQR;
- production test plate report;
- traceability record;
- inspection record.

Not every requirement can be verified from an MTR. MatJSON must distinguish between a material failure and missing or inappropriate evidence.

Useful future compliance outcomes include:

- `pass`;
- `fail`;
- `not_applicable`;
- `needs_project_input`;
- `missing_evidence`;
- `requisition_gap`;
- `manual_review_required`.

## 13. MatRecordJSON concept

MatRecordJSON will normalize the evidence supplied for one material or component. It is intended to represent:

- document identity and source;
- material specification, grade, heat, lot, and condition;
- reported chemistry;
- reported mechanical properties;
- heat treatment;
- tests and results;
- NDE;
- certifications;
- traceability;
- linked supporting documents;
- extraction confidence and provenance.

The goal is to convert many different mill and inspection document layouts into one common evidence representation before checking.

The detailed MatRecord schema remains TBC.

## 14. MatCheckJSON concept

MatCheckJSON will store the output of comparing effective requirements with normalized evidence. It should preserve:

- evaluated requirement identifier;
- requirement origin;
- applicability decision;
- evidence used;
- reported and required values;
- comparison method;
- result status;
- explanation;
- missing inputs or evidence;
- reviewer and tool metadata;
- overall summary without hiding individual failures.

The detailed MatCheck schema remains TBC.

## 15. Versioning

MatJSON requires two separate version dimensions.

### 15.1 Profile/schema version

This identifies the MatJSON data format:

```json
{
  "matjson": {
    "profile": "matspec",
    "version": "0.2.10"
  }
}
```

### 15.2 Source-document edition

This identifies the engineering standard being represented:

```json
{
  "document": {
    "organization": "API",
    "designation": "663",
    "edition": {
      "number": 2,
      "publication": "2022-08"
    }
  }
}
```

A new source edition does not necessarily change the MatJSON schema version, and a new schema version does not change the source edition.

## 16. File naming

Recommended examples:

```text
api-663-2022.matreq.json
api-663-2014.matreq.json
api-rp-934-a-2025.matreq.json
api-tr-938-c-2024.matreq.json
api-660-2015-a1-2020.matreq.json
asme-bpvc-viii-1-2025.matreq.json
```

Reaffirmation should be recorded in metadata rather than replacing the technical publication/addendum identity.

## 17. Canonical URLs and identifiers

Recommended stable schema URLs:

```text
https://matjson.org/schema/core/0.1/schema.json
https://matjson.org/schema/matspec/0.2.10/schema.json
https://matjson.org/schema/matreq/0.2/schema.json
https://matjson.org/schema/matrecord/0.1/schema.json
https://matjson.org/schema/matcheck/0.1/schema.json
```

Recommended identifier patterns:

```text
https://matjson.org/id/document/api/663/2022
https://matjson.org/id/rule/api/663/2022/8.2.2
https://matjson.org/id/document/asme/sa-516/2025
https://matjson.org/id/material/asme/sa-516/2025/grade-70
```

The versioned URL should be the canonical JSON Schema `$id`. A `latest` convenience URL may return the current version but should not replace immutable identifiers.

## 18. Conformance levels

Schema validity does not establish engineering accuracy. MatJSON should distinguish at least:

1. **Syntactically conforming** — valid JSON and valid against the declared schema.
2. **Semantically conforming** — controlled identifiers, units, selectors, and rule semantics are used correctly.
3. **Source-complete** — the declared extraction scope has no unresolved mandatory content.
4. **Technically reviewed** — an identified reviewer compared the content with the governing source.
5. **Verified publication** — the package passed an approved MatJSON publication process.

A generated draft should never be presented as verified solely because it passes JSON Schema validation.

## 19. Controlled vocabularies

MatJSON Core should publish controlled vocabularies for:

- material families;
- product forms;
- equipment components;
- weld regions;
- testing methods;
- heat-treatment processes;
- evidence types;
- service conditions;
- units;
- document types;
- normativity;
- activation;
- compliance outcomes.

Stable identifiers should carry semantic meaning, while human-readable labels can be localized.

## 20. Extensions

Industry-specific extensions should be namespaced. A conforming reader should process core fields, preserve unknown namespaced extensions, ignore extensions it does not understand, and never infer that an extension silently changes a core requirement.

Example:

```json
{
  "extensions": {
    "https://example-aircraft.org/matjson": {
      "fatigue_classification": "A3"
    }
  }
}
```

## 21. Public website architecture

Recommended public navigation:

```text
/
/spec/
/schemas/
/profiles/core/
/profiles/matspec/
/profiles/matreq/
/profiles/matrecord/
/profiles/matcheck/
/registry/
/examples/
/tools/
/guides/
/resources/
/governance/
/about/
```

The starter website created with this document implements those routes as a static, deployable site.

## 22. Copyright and publication boundary

The MatJSON schemas, architecture, vocabularies, software, and synthetic examples can be published as original project assets. Complete derived data packages based on proprietary standards may be subject to the source publisher's licensing and copyright terms.

The public site should therefore separate:

### Public/open project content

- MatJSON specification;
- JSON schemas;
- controlled vocabularies;
- validators and SDKs;
- synthetic examples;
- public metadata registry;
- governance and RFCs.

### Rights-controlled content

- complete extracted API, ASME, AMPP/NACE, ASTM, ISO, or other proprietary standards packages;
- reproduced source text and tables;
- licensed acceptance-criteria libraries where redistribution permission is unclear.

A public registry can describe the existence, source edition, profile, verification status, and access policy of a package without redistributing its protected contents.

The website should include a non-affiliation notice and should not use standards-organization marks or imply that MatJSON files are approved by the source organizations.

## 23. Governance and licensing direction

A lightweight governance model can begin with:

- MatJSON editor;
- technical reviewers;
- implementation contributors;
- an industry advisory group.

Major changes should be documented through RFCs, for example:

```text
MJ-RFC-0001 Core terminology and profiles
MJ-RFC-0002 Units and quantities
MJ-RFC-0003 Rule applicability expressions
MJ-RFC-0004 Source-document invocation
MJ-RFC-0005 Compliance evidence model
```

A proposed licensing arrangement is:

- schemas and software: Apache License 2.0;
- specification documentation and vocabularies: CC BY 4.0 or another approved open-content license;
- synthetic examples: CC0 or CC BY 4.0;
- standards-derived packages: governed by source rights.

This licensing model remains a proposal until formally adopted.

## 24. Tooling roadmap

Potential reference tooling:

```text
matjson validate file.json
matjson inspect file.json
matjson resolve requisition.json
matjson compare record.json requirements.json
matjson migrate --from 0.2 --to 0.3 file.json
```

Initial SDK priorities:

- Python;
- TypeScript / JavaScript.

Potential API routes:

```http
GET /api/v1/schemas
GET /api/v1/documents
GET /api/v1/documents/api/663/2022
GET /api/v1/rules/api/663/2022/8.2.2
GET /api/v1/vocabularies/product-form
POST /api/v1/validate
```

Static versioned schemas and a command-line validator are sufficient for the first release; a hosted API can follow.

## 25. Suggested release sequence

### MatJSON 0.1 public architecture release

- project charter and scope;
- MatJSON Core concepts;
- MatSpecJSON schema;
- MatReqJSON schema;
- identifiers and versioning;
- conformance specification;
- extension policy;
- synthetic examples;
- validator CLI;
- governance and contribution policy;
- publication/copyright policy.

### Subsequent work

- extract common primitives into MatJSON Core;
- formalize formulas and statistical acceptance;
- add executable decision graphs and curve/table datasets;
- define MatRecordJSON;
- define MatCheckJSON;
- build effective-requirements resolver;
- build MTR/evidence normalization tools;
- establish independent engineering review and package verification;
- pursue cross-industry contributors and implementations.

## 26. Current artifacts and status

Existing work includes:

- MatSpecJSON schema v0.2.10;
- MatReqJSON schema v0.2;
- draft MatSpec and MatReq libraries;
- audit reports identifying numeric, provenance, completeness, and schema issues;
- this MatJSON website starter;
- placeholder Core, MatRecord, and MatCheck schemas for architectural continuity.

All current standards-derived data files should remain marked draft until independently audited and publication rights are resolved.

## 27. Decisions that should remain stable unless deliberately revisited

1. MatJSON is an interoperability specification, not merely a hosted database.
2. MatSpec defines intrinsic material-specification requirements.
3. MatReq defines requirements imposed by other governing documents.
4. MatReq is rule-centric.
5. The material requisition remains the project-specific source of truth.
6. No separate MatCtx profile is currently planned.
7. Source normativity and project activation are separate concepts.
8. Component and product-form ontologies are separate.
9. Verification evidence is first-class.
10. Schema validation does not equal technical verification.
11. Proprietary standards data and open MatJSON schemas must be treated separately.
12. MatRecord and MatCheck are part of the architecture but remain TBC.

## 28. Copy-paste context for a new ChatGPT conversation

Use the following prompt to resume the project:

> I am developing MatJSON at matjson.org, an open, vendor-neutral family of JSON schemas for machine-readable materials data. MatSpecJSON (`.matspec.json`) captures intrinsic requirements of material/product specifications. MatReqJSON (`.matreq.json`) captures additional material requirements imposed by equipment codes, service standards, fabrication practices, and purchaser specifications. The material requisition is the project-specific source of truth; we deliberately do not use a separate MatCtx schema. MatRecordJSON (`.matrecord.json`) will normalize MTRs, CMTRs, and test evidence, and MatCheckJSON (`.matcheck.json`) will store machine-readable compliance results; both are currently TBC. MatJSON Core will provide shared units, provenance, identifiers, selectors, expressions, vocabularies, and extension rules. MatJSON is intended as an open interoperability protocol, not just a database. Requirements must preserve source provenance, normativity, activation, applicability, evidence, and review status. Public schemas and synthetic examples must be separated from rights-controlled standards-derived data. Please use the attached `MATJSON_PROJECT_CONTEXT_AND_ARCHITECTURE.md` and website package as the governing project context.

---

**End of preserved project context.**
