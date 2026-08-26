"""Documentation-only descriptions used by build_schema_reference.py.

This module contains data only. It does not generate or modify website files.
"""

HINTS = {'matspec': {'root': {'matspec': 'Format discriminator and MatSpecJSON version. Consumers use it to reject '
                                 'unsupported formats rather than partially interpreting them.',
                      'specification': 'Identity and scope of the source material specification, including '
                                       'designation, title, edition, product form, and whether the file '
                                       'describes a product specification or a general-requirements '
                                       'specification.',
                      'provenance': 'Where the extracted requirements came from and how the file was '
                                    'produced. Provenance describes the source, not whether a reviewer has '
                                    'verified the extraction.',
                      'references': 'Other specifications, general-requirements documents, test methods, or '
                                    'adopted source standards referenced by this specification.',
                      'manufacturing': 'Specification-wide requirements for manufacture, process route, '
                                       'workmanship, certification, marking, dimensions, and related '
                                       'controls.',
                      'grades': 'The grade-centric acceptance requirements. Each entry identifies a grade, '
                                'class, type, condition, or process variant and carries chemistry, '
                                'mechanical, hardness, impact, heat-treatment, and other requirements.',
                      'required_tests': 'Tests required at the specification level rather than only for one '
                                        'grade. Frequency, method, and source are preserved where available.',
                      'supplementary_requirements': 'Optional, purchaser-invoked, or ASME-mandated '
                                                    'supplementary requirements associated with the '
                                                    'specification.',
                      'notes': 'Reusable source notes keyed by identifier so individual values can reference '
                               'explanatory text without duplicating it.',
                      'extensions': 'Namespaced implementation data outside the MatSpec conformance surface. '
                                    'Conforming readers preserve or ignore extensions they do not '
                                    'understand.'},
             'defs': {'notExtracted': 'An explicit extraction gap. It means the source may contain a '
                                      'requirement that has not yet been captured; it is not the same as a '
                                      'confirmed absence of a requirement.',
                      'unit': 'Controlled units permitted for structured acceptance values.',
                      'value': 'One cited acceptance bound or range, optionally narrowed by applicability '
                               'selectors.',
                      'valueSet': 'Sibling values supplied by the source in different unit systems. The '
                                  'values are source statements, not assumed mathematical conversions.',
                      'band': 'A bounded applicability interval, such as a thickness, diameter, temperature, '
                              'composition, or size range.',
                      'appliesWhen': 'Selectors that determine when a value or requirement applies. Every '
                                     'populated selector must match.',
                      'grade': 'A named material grade, class, type, condition, or process variant and its '
                               'acceptance criteria.',
                      'test': 'A required material test, including whether it is mandatory, its method, '
                              'frequency, and source.',
                      'alternatives': 'Alternative acceptance values where satisfying any listed member is '
                                      'sufficient, such as equivalent hardness limits on different scales.',
                      'valueOrAlternatives': 'A union allowing either one acceptance value or a formally '
                                             'identified alternatives block.'}},
 'matreq': {'root': {'schema_version': 'Format discriminator and MatReqJSON schema version.',
                     'document': 'Identity, edition, type, and publication metadata for the governing code, '
                                 'standard, recommended practice, technical report, or purchaser '
                                 'specification.',
                     'invocation_model': 'How the governing document or a scoped part of it becomes '
                                         'contractually active through a material requisition or other '
                                         'contract document.',
                     'scope': 'The equipment, industries, materials, services, and lifecycle stages '
                              'addressed by the source document.',
                     'references': 'Referenced external documents and the precise role each reference plays, '
                                   'such as full invocation, test method only, or informative guidance.',
                     'requisition_interface': 'Purchaser decisions or values that the governing document '
                                              'expects the material requisition to resolve when associated '
                                              'rules are active.',
                     'rules': 'Atomic material-related rules with targets, activation logic, typed '
                              'requirements, verification evidence, and source provenance.',
                     'provenance': 'Source-document and extraction metadata for the MatReq package.',
                     'notes': 'Supplemental explanatory notes used by rules or the package as a whole.',
                     'extensions': 'Namespaced implementation data outside the MatReq conformance surface.',
                     'coverage': 'Declared extraction scope, included sections, exclusions, unresolved gaps, '
                                 'and review status.'},
            'defs': {'document': 'Identity and publication metadata for the governing document represented '
                                 'by this MatReq file.',
                     'edition': 'Edition, publication date, addenda, errata, and reaffirmation metadata.',
                     'invocationModel': 'Rules for whole-document, section, annex, clause, or '
                                        'direct-requirement invocation from a material requisition.',
                     'documentScope': 'Structured statement of the source document scope.',
                     'rule': 'One atomic material-related rule that can be independently activated, '
                             'evaluated, and traced to its source.',
                     'normativity': "The source document's normative strength and modal wording, kept "
                                    'separate from project activation.',
                     'targets': 'Materials, grades, product forms, equipment components, weld regions, '
                                'sides, services, and fabrication states to which a rule can apply.',
                     'activation': 'How a rule becomes active for a purchase, including always-active, '
                                   'conditionally active, purchaser-invoked, or scoped invocation.',
                     'conditionExpr': 'A Boolean expression tree built from condition leaves and all/any/not '
                                      'operators.',
                     'conditionLeaf': 'One comparison against requisition, service, material, component, or '
                                      'fabrication data.',
                     'requirement': 'The typed behavior imposed by the rule, such as a limit, test, '
                                    'examination, heat treatment, document field, prohibition, or decision '
                                    'procedure.',
                     'calculation': 'A machine-readable formula, required inputs, units, and result '
                                    'semantics.',
                     'effect': 'How a MatReq rule supplements, restricts, replaces, selects, prohibits, or '
                               'otherwise interacts with a base MatSpec requirement.',
                     'verification': 'Evidence types, checking method, and result behavior used to '
                                     'demonstrate compliance.',
                     'dependencies': 'Other rules, decisions, or external documents needed before this rule '
                                     'can be evaluated.',
                     'referenceTarget': 'A structured target for an invoked document, section, annex, '
                                        'clause, table, figure, or requirement.',
                     'documentReference': 'An external standard reference together with its invocation role.',
                     'requisitionInput': 'A value or decision the material requisition must provide when an '
                                         'associated rule is active.',
                     'sourceRef': 'A clause, table, figure, page, or other source location supporting a '
                                  'rule.',
                     'provenance': 'Package-level source and extraction provenance.',
                     'coverage': 'Extraction coverage, exclusions, unresolved areas, and review status.'}},
 'core': {'root': {},
          'defs': {'identifier': 'A stable identifier used across MatJSON profiles.',
                   'quantity': 'A typed numeric quantity with unit and optional source context.',
                   'source': 'Reusable provenance for a requirement, value, evidence item, or result.',
                   'expression': 'A machine-readable Boolean or numeric expression.',
                   'extensionContainer': 'A namespaced container for domain-specific additions.'}},
 'matrecord': {'root': {'matjson': 'MatJSON profile and version discriminator for this normalized evidence '
                                   'record.',
                        'record': 'Identity and issuer information for the source MTR, CMTR, certificate, '
                                  'report, or evidence document.',
                        'materials': 'Normalized material identities and reported test results.',
                        'evidence': 'References to source evidence used to create the normalized record.',
                        'extensions': 'Namespaced implementation data outside the draft conformance '
                                      'surface.'},
               'defs': {}},
 'matcheck': {'root': {'matjson': 'MatJSON profile and version discriminator for this compliance result.',
                       'check': 'Identity and provenance of the compliance evaluation.',
                       'results': 'Requirement-by-requirement applicability, evidence, comparison, result, '
                                  'and explanation.',
                       'summary': 'Machine-readable counts and overall result.',
                       'extensions': 'Namespaced implementation data outside the draft conformance surface.'},
              'defs': {}}}

COMMON_FIELD_HINTS = {'id': 'Stable identifier for this object within its containing MatJSON document.',
 'title': 'Short human-readable name displayed in documentation and review tools.',
 'description': 'Human-readable explanation of the object, rule, input, or scope.',
 'type': 'Controlled category used by consumers to determine how the value is interpreted.',
 'unit': 'Unit associated with the numeric value or limit. Use the unit exactly as published by the '
         'applicable profile vocabulary.',
 'value': 'The value supplied, required, reported, or compared at this location.',
 'values': 'List of values associated with this requirement or schema construct.',
 'minimum': 'Lower acceptance bound or minimum required value.',
 'maximum': 'Upper acceptance bound or maximum permitted value.',
 'notes': 'Additional explanatory notes that do not replace the structured requirement.',
 'source': 'Structured source location or provenance supporting this object.',
 'extensions': 'Namespaced implementation-specific data outside the profile conformance surface.',
 'method': 'Method, test procedure, examination technique, or process used to satisfy the requirement.',
 'frequency': 'Sampling or performance frequency for the required activity.',
 'basis': 'Basis used to select, activate, calculate, or interpret this requirement.',
 'document': 'Document or evidence record associated with this object.',
 'fields': 'Specific document fields or reported data elements required by the rule.',
 'procedure': 'Procedure that must be followed or documented.',
 'timing': 'Required point in manufacture, fabrication, heat treatment, examination, or review when the '
           'activity occurs.',
 'location': 'Material, component, weld, specimen, or document location to which the requirement applies.',
 'scope': 'Boundary of the requirement or the items covered by it.',
 'reporting': 'Information that must be recorded, certified, or included in the evidence package.',
 'specimen': 'Test-specimen type, orientation, dimensions, or preparation requirements.',
 'alternatives': 'Alternative ways of satisfying the same requirement. The rule defines whether one or all '
                 'alternatives are needed.',
 'lookup': 'Structured reference to a source table, figure, curve, or decision aid that must be consulted.',
 'subject': 'Material, component, weld, document, or other subject acted on by this requirement.',
 'operator': 'Comparison operator used when evaluating the required or reported value.',
 'field': 'Path or named input evaluated by the condition.',
 'op': 'Boolean or comparison operator applied to the condition field.',
 'page': 'Printed or electronic source page supporting the requirement.',
 'table': 'Source table identifier supporting the requirement.',
 'figure': 'Source figure identifier supporting the requirement.',
 'clause': 'Clause or paragraph identifier supporting the requirement.',
 'included': 'Material-related sections or topics included in the extraction.',
 'excluded': 'Topics deliberately outside the extraction scope.',
 'limitations': 'Known limitations that affect completeness or automated use.'}

PROPERTY_HINTS = {'matspec': {'notExtracted.extracted': 'Always false. The object explicitly records that a potentially '
                                       'applicable source requirement has not yet been extracted.',
             'notExtracted.note': 'Explanation of what is missing and where a reviewer should look in the '
                                  'source.',
             'value.min': 'Minimum accepted value. Null means the source states no lower bound for this '
                          'value.',
             'value.max': 'Maximum accepted value. Null means the source states no upper bound for this '
                          'value.',
             'value.source': 'Clause, table, note, or other locator supporting this individual acceptance '
                             'value.',
             'value.basis': 'Whether the limit applies to heat analysis, product analysis, or both.',
             'value.applies_when': 'Selectors that must match before this acceptance value is used.',
             'value.notes': 'Identifiers of reusable notes that qualify or explain this value.',
             'valueSet.values': 'One or more source-stated values, commonly parallel customary and SI '
                                'requirements.',
             'band.min': 'Lower endpoint of the applicability interval.',
             'band.max': 'Upper endpoint of the applicability interval.',
             'appliesWhen.thickness': 'Thickness interval for which the value or requirement applies.',
             'appliesWhen.diameter': 'Diameter interval for which the value or requirement applies.',
             'appliesWhen.temperature': 'Temperature interval or test temperature for which the value or '
                                        'requirement applies.',
             'appliesWhen.product_form': 'Product form that must match, such as plate, tube, pipe, bar, '
                                         'fitting, or forging.',
             'appliesWhen.condition': 'Material condition or processing state that must match, such as '
                                      'annealed, normalized, or stress relieved.',
             'appliesWhen.gauge_length': 'Gauge length or proportional specimen basis used for the stated '
                                         'elongation requirement.',
             'appliesWhen.specimen_size': 'Specimen-size designation associated with the stated test '
                                          'requirement.',
             'appliesWhen.orientation': 'Required specimen orientation relative to the principal working '
                                        'direction.',
             'grade.id': 'Stable normalized identifier for the grade, class, type, condition, or process '
                         'variant.',
             'grade.designation': 'Source designation details, such as grade, class, type, UNS number, '
                                  'condition, or process.',
             'grade.aliases': 'Alternative designations by which the same normalized grade entry may be '
                              'identified.',
             'grade.chemistry': 'Heat- and/or product-analysis acceptance requirements for the grade, or an '
                                'explicit extraction-gap marker.',
             'grade.mechanical': 'Tensile, yield, elongation, reduction-of-area, or related mechanical '
                                 'acceptance requirements.',
             'grade.hardness': 'Hardness limits, including formally represented alternatives where the '
                               'source permits different scales.',
             'grade.impact': 'Impact energy, test temperature, specimen, orientation, and applicability '
                             'requirements.',
             'grade.heat_treatment': 'Required thermal condition, temperature, cooling route, applicability, '
                                     'and source.',
             'test.test': 'Human-readable name of the required test or examination.',
             'test.required': 'True when the test is mandatory under the represented specification and '
                              'stated applicability.',
             'test.frequency': 'Number of tests and the lot, heat, length, piece, or other population each '
                               'test represents.',
             'test.method': 'Test standard, examination technique, or source-described procedure.',
             'test.source': 'Clause, table, or note that establishes the test requirement.',
             'alternatives.any_of': 'Acceptance values for which satisfying any one listed alternative is '
                                    'sufficient.',
             'alternatives.note': 'Explanation of how or why the alternatives are permitted.'},
 'matreq': {'document.organization': 'Standards body, regulator, owner-user, or purchaser that issued the '
                                     'represented document.',
            'document.document_type': 'Nature of the governing publication, used to interpret its role and '
                                      'authority.',
            'document.edition': 'Edition, publication date, addenda, errata, reaffirmation, and related '
                                'revision metadata for the governing document.',
            'document.title': 'Published title of the governing document.',
            'edition.number': 'Published edition number or other edition designation.',
            'edition.addenda': 'Addenda incorporated into the represented document package, with identifiers '
                               'and publication dates where known.',
            'edition.reaffirmed': 'Date or year the edition was reaffirmed without technical revision, or '
                                  'null when not applicable.',
            'edition.errata': 'Errata incorporated into the represented document package.',
            'edition.other_revisions': 'Other revision notices not represented as addenda or errata.',
            'invocationModel.document_reference': 'Wording patterns and behavior for invoking the entire '
                                                  'governing document from a requisition.',
            'invocationModel.scoped_reference': 'Wording patterns and behavior for invoking only a named '
                                                'part, section, annex, appendix, table, figure, or clause.',
            'invocationModel.direct_rule_reference': 'Behavior when the requisition states a requirement '
                                                     'directly, whether or not it cites the source document.',
            'invocationModel.cross_reference_policy': 'Rules for deciding whether an internal reference '
                                                      'imports another document fully, only a method or '
                                                      'criterion, or merely guidance.',
            'documentScope.equipment': 'Equipment classes addressed by the source document.',
            'documentScope.industries': 'Industries or application sectors within the represented scope.',
            'documentScope.services': 'Service environments or damage mechanisms addressed by the source.',
            'documentScope.material_families': 'Broad material families covered by the represented '
                                               'extraction.',
            'documentScope.product_forms': 'Material product forms covered by the represented extraction.',
            'documentScope.description': 'Plain-language summary of the document scope relevant to material '
                                         'requirements.',
            'documentScope.included_sections': 'Sections explicitly included in the MatReq extraction.',
            'documentScope.excluded_topics': 'Document topics intentionally excluded because they are not '
                                             'material-related or are outside the declared extraction.',
            'rule.id': 'Stable rule identifier used for invocation, dependencies, checking, and result '
                       'traceability.',
            'rule.title': 'Short human-readable statement of the rule.',
            'rule.category': 'Controlled material-requirement category used for filtering and downstream '
                             'processing.',
            'rule.normativity': 'Source authority and modal wording for the rule, kept separate from '
                                'project-specific activation.',
            'rule.targets': 'Structured material, product-form, component, region, service, and fabrication '
                            'selectors for the rule.',
            'rule.activation': 'Logic establishing when the rule becomes applicable to a particular '
                               'requisition or material item.',
            'rule.requirement': 'Typed statement of what must be satisfied when the rule is active.',
            'rule.effect': 'How the rule interacts with a base MatSpec requirement or another effective '
                           'requirement.',
            'rule.verification': 'Evidence and checking instructions used to determine compliance.',
            'rule.dependencies': 'Other rules or decisions that must resolve before, or are activated by, '
                                 'this rule.',
            'rule.references': 'External documents invoked or used by this rule, together with the precise '
                               'reference role.',
            'rule.source': 'Primary source locator for the rule. Use sources when multiple noncontiguous '
                           'locations jointly establish it.',
            'rule.notes': 'Additional interpretation or extraction notes that do not replace the structured '
                          'rule.',
            'rule.group_id': 'Identifier linking related atomic rules that originate from one larger source '
                             'requirement or decision sequence.',
            'rule.structured_level': 'Degree to which the source requirement has been converted into '
                                     'executable structure rather than preserved text or a lookup.',
            'rule.sources': 'One or more source locations jointly supporting the rule.',
            'rule.extensions': 'Namespaced workflow or domain data associated with this rule.',
            'normativity.source_level': 'Normative strength of the requirement in its source document.',
            'normativity.source_modal': 'Modal word used by the external source. MatJSON-authored '
                                        'requirements use must/must not, while this field preserves source '
                                        'wording.',
            'targets.material': 'Material-family, specification, grade, type, class, UNS, or related '
                                'selectors identifying the affected material.',
            'targets.product_forms': 'Affected product forms, such as plate, pipe, tube, forging, casting, '
                                     'bar, bolting, fitting, or consumable.',
            'targets.components': 'Equipment components to which the rule applies.',
            'targets.regions': 'Material or weld regions to which the rule applies, such as base metal, weld '
                               'metal, HAZ, overlay, cladding, or bend.',
            'targets.pressure_retaining': 'Whether the target must be a pressure-retaining item.',
            'targets.process_wetted': 'Whether the target must contact the process fluid.',
            'targets.joint_types': 'Weld or joint configurations to which the rule applies.',
            'targets.weld_processes': 'Welding processes to which the rule applies.',
            'targets.services': 'Named services or environmental conditions that select the rule.',
            'targets.service_sides': 'Equipment side or fluid circuit to which the rule applies.',
            'targets.conditions': 'Additional controlled or source-preserved target conditions.',
            'activation.basis': 'How document invocation, scoped invocation, and stated conditions combine '
                                'to activate the rule.',
            'activation.when': 'Boolean condition expression that must be satisfied for the rule to apply.',
            'activation.notes': 'Additional explanation of activation behavior.',
            'conditionLeaf.field': 'Path to the requisition, service, material, component, or fabrication '
                                   'fact being tested.',
            'conditionLeaf.op': 'Comparison performed against the condition field.',
            'conditionLeaf.value': 'Comparison value used by the condition.',
            'conditionLeaf.unit': 'Unit for a numeric comparison value.',
            'requirement.kind': 'Typed requirement behavior that tells a checker how the remaining '
                                'requirement fields should be interpreted.',
            'requirement.property': 'Named material property, document field, condition, or characteristic '
                                    'controlled by the requirement.',
            'requirement.operator': 'Comparison operator used for the stated value or limit.',
            'requirement.value': 'Single required value when the requirement is not a range.',
            'requirement.minimum': 'Minimum required value or lower bound.',
            'requirement.maximum': 'Maximum permitted value or upper bound.',
            'requirement.unit': 'Unit for the stated requirement values.',
            'requirement.values': 'Permitted, prohibited, or otherwise enumerated values associated with the '
                                  'requirement.',
            'requirement.text': 'Source-preserved or human-readable requirement text when full executable '
                                'structure is not available or when explanation is needed.',
            'requirement.fields': 'Fields that must appear in an MTR, CMTR, report, certificate, '
                                  'requisition, or other evidence document.',
            'requirement.calculation': 'Formula, required inputs, result unit, and source used for a '
                                       'computed requirement.',
            'requirement.referenced_standard': 'External standard or scoped part with which compliance is '
                                               'required.',
            'requirement.method': 'Required test, examination, calculation, fabrication, or qualification '
                                  'method.',
            'requirement.frequency': 'Required testing, examination, sampling, or reporting frequency.',
            'requirement.sampling': 'Population, lot, heat, piece, weld length, location, or '
                                    'sample-selection rules.',
            'requirement.acceptance_criteria': 'Criteria used to decide whether the test, examination, '
                                               'qualification, or material is acceptable.',
            'requirement.procedure': 'Required procedure or procedural controls.',
            'requirement.timing': 'Point in the manufacturing or fabrication sequence when the requirement '
                                  'must be performed.',
            'requirement.location': 'Physical or documentary location at which the requirement applies or '
                                    'evidence is taken.',
            'requirement.scope': 'Extent of items, surfaces, welds, lots, or records covered by the '
                                 'requirement.',
            'requirement.reporting': 'Results, certifications, traceability, or records that must be '
                                     'provided.',
            'requirement.specimen': 'Test-specimen preparation, dimensions, orientation, or source location.',
            'requirement.alternatives': 'Alternative methods or acceptance paths permitted by the source.',
            'requirement.lookup': 'Table, figure, curve, chart, or decision aid required to resolve the '
                                  'rule.',
            'requirement.basis': 'Basis for the stated limit, selection, calculation, or source decision.',
            'requirement.subject': 'Material, component, weld, document, or evidence item controlled by the '
                                   'rule.',
            'calculation.id': 'Stable identifier for the calculation or formula.',
            'calculation.expression': 'Machine-readable or source-preserved mathematical expression.',
            'calculation.inputs': 'Required chemistry, design, service, dimensional, or other input paths.',
            'calculation.result_unit': 'Unit of the calculated result.',
            'calculation.source': 'Source location defining the formula and its use.',
            'effect.relationship': 'How this rule changes or supplements the base MatSpec requirement.',
            'effect.base_requirement': 'Structured pointer to the base MatSpec requirement affected by the '
                                       'rule.',
            'effect.conflict_resolution': 'Authorized method for resolving this rule with overlapping '
                                          'requirements. Most-stringent is used only when the source '
                                          'expressly requires it.',
            'verification.mode': 'How compliance is checked: direct comparison, calculation, record review, '
                                 'cross-document review, or manual engineering review.',
            'verification.result_if_missing': 'Result returned when the required evidence or requisition '
                                              'input is absent.',
            'verification.notes': 'Additional evidence-review instructions.',
            'verification.checkability': 'Where and how the rule can be checked, such as directly from an '
                                         'MTR, from a supporting report, or only by manual evaluation.',
            'verification.evidence_fields': 'Specific evidence fields needed to evaluate the rule.',
            'dependencies.requires_rule_ids': 'Rules that must be resolved before this rule can be '
                                              'evaluated.',
            'dependencies.activates_rule_ids': 'Rules activated when this rule or decision resolves true.',
            'referenceTarget.designation': 'Designation of the referenced external document.',
            'referenceTarget.edition': 'Edition of the referenced document when the reference is '
                                       'edition-specific.',
            'referenceTarget.scope_type': 'Type of scoped source location being referenced.',
            'referenceTarget.scope_id': 'Identifier of the referenced part, section, clause, annex, '
                                        'appendix, table, or figure.',
            'documentReference.target': 'Document and optional scoped location being referenced.',
            'documentReference.effect': 'Role of the reference, such as full invocation, scoped invocation, '
                                        'test method only, acceptance criteria only, or guidance.',
            'documentReference.activation_when': 'Condition under which the external reference becomes '
                                                 'active.',
            'documentReference.source': 'Location in the current document that makes the external reference.',
            'documentReference.notes': 'Additional explanation of the external reference role.',
            'requisitionInput.id': 'Stable identifier used by rules to request the purchaser decision or '
                                   'value.',
            'requisitionInput.description': 'Plain-language description of the information the requisition '
                                            'must provide.',
            'requisitionInput.type': 'Expected data or invocation type for the purchaser-supplied input.',
            'requisitionInput.unit': 'Unit required for the purchaser-supplied numeric value.',
            'requisitionInput.required_when': 'Condition under which omission of this requisition input is a '
                                              'requisition gap.',
            'requisitionInput.allowed_values': 'Permitted purchaser selections when the input is '
                                               'constrained.',
            'requisitionInput.source': 'Source location requiring the purchaser to supply the input.',
            'sourceRef.clause': 'Clause or paragraph identifier in the source document.',
            'sourceRef.page': 'Source page number or page label.',
            'sourceRef.table': 'Table identifier in the source document.',
            'sourceRef.figure': 'Figure identifier in the source document.',
            'sourceRef.text_type': 'Normative or informative role of the cited source material.',
            'sourceRef.notes': 'Additional citation or locator details.',
            'provenance.source': 'Human-readable identity of the source document represented by the package.',
            'provenance.extracted_on': 'Date the MatReq extraction was produced.',
            'provenance.extraction_method': 'Whether extraction was manual, assisted, automated, or mixed.',
            'provenance.review_status': 'Current technical review maturity of the MatReq package.',
            'provenance.review_notes': 'Reviewer comments, limitations, or outstanding verification work.',
            'provenance.rules_generated': 'Count of rules generated in this package.',
            'provenance.unresolved_items': 'Known requirements or source areas that remain unresolved.',
            'provenance.source_file': 'Filename or controlled source identifier used for extraction.',
            'provenance.coverage': 'Brief package-level statement describing the material-related extraction '
                                   'coverage.',
            'coverage.material_scope_status': 'Whether material-related extraction is full, targeted, or '
                                              'partial.',
            'coverage.included': 'Material-related sections and topics included in the package.',
            'coverage.excluded': 'Topics deliberately excluded from the package.',
            'coverage.lookup_required': 'Source tables, figures, curves, or decision aids that still require '
                                        'lookup during evaluation.',
            'coverage.limitations': 'Known limitations on completeness, structure, automation, or '
                                    'verification.'},
 'core': {'quantity.value': 'Numeric magnitude of the quantity.',
          'quantity.unit': 'Unit identifier associated with the magnitude.',
          'quantity.basis': 'Optional basis or measurement context used to interpret the quantity.',
          'source.document': 'Document designation or stable document identifier.',
          'source.edition': 'Edition or publication identifier of the source document.',
          'source.locator': 'Clause, table, field, page range, or other source locator.',
          'source.page': 'Printed or electronic page supporting the value or statement.',
          'source.text_role': 'Normative role of the cited source text.'},
 'matrecord': {'root.matjson': 'MatJSON profile and version discriminator for this normalized evidence '
                               'record.',
               'root.record': 'Identity, issuer, date, document type, and source-file metadata for the MTR, '
                              'CMTR, certificate, or report.',
               'root.materials': 'Normalized materials and their reported specification, grade, heat/lot '
                                 'identity, product form, chemistry, mechanical results, heat treatment, and '
                                 'tests.',
               'root.evidence': 'Source-document references and extraction-confidence information supporting '
                                'the normalized record.',
               'root.extensions': 'Namespaced implementation data outside the future MatRecord conformance '
                                  'surface.'},
 'matcheck': {'root.matjson': 'MatJSON profile and version discriminator for this compliance result '
                              'document.',
              'root.check': 'Identity, time, tool, and reviewer associated with the compliance evaluation.',
              'root.results': 'Requirement-by-requirement outcomes, evidence, required and reported values, '
                              'and explanations.',
              'root.summary': 'Overall status and aggregate result counts for the evaluation.',
              'root.extensions': 'Namespaced implementation data outside the future MatCheck conformance '
                                 'surface.'}}

