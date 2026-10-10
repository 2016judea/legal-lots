# Legal Lots — the idealized data model

Written 2026-10-10, step zero (`~/.claude/BUSINESS.md` rule 5), from the buyer's
need alone and before looking at what data we hold.

**The buyer.** A Minnesota cannabis licence holder with preliminary approval and no
building. They need a site the city will sign off on, and many lose their approval
on January 1, 2027. **The question the report answers:** *which lots in my city can
I legally open on, and who do I call about each one?*

## Entities

### City
| field | answers |
|---|---|
| name, county | which report this is |
| ordinance_url, ordinance_adopted | "says who?" — every rule is cited |
| allowed_districts[licence_type] | which zoning districts permit this use (retail, micro, mezzo, delivery…) |
| buffers[] → {sensitive_type, distance_ft, measured_from, measured_to, whole_lot_rule} | the exact distance rule, as the city measures it |
| retail_cap, registrations_issued | is there a slot left at all? |
| other_rules (hours, min spacing between stores, CUP needed) | what else stands between a lot and a yes |
| planner_contact | who confirms the reading |

### Zoning district (polygon)
| field | answers |
|---|---|
| code, name, geometry, source, as_of | is this lot inside an allowed district |

### Sensitive use (point or polygon)
| field | answers |
|---|---|
| type (K-12 school, licensed child care, treatment facility, park/playground, youth facility, existing store) | which buffer applies |
| name, address, geometry, source, as_of | which one disqualified a lot, by name |

### Parcel
| field | answers |
|---|---|
| pin, address, geometry | where it is |
| zoning_code (official city zoning) | allowed or not |
| land_use / property type, lot_sqft, building_sqft, year_built | could a shop physically go here |
| owner_name, owner_mailing_address | who to call or write |
| last_sale_date (years held), market_value | likelihood to lease/sell; rent proxy |
| vacant / for_lease / for_sale listing | is it actually available |
| current_occupant | is something already there |

### Eligibility (parcel × licence type × city rule)
| field | answers |
|---|---|
| eligible (yes/no) | the core answer |
| failing_rule, nearest_sensitive_use, distance_ft | why not, by name and feet |
| margin_ft | how close to the line — a planner check flag |

### Applicant (buyer)
| field | answers |
|---|---|
| business_name, person, licence_type, target_city | who buys which city |
| approval_date, expires_on | the deadline that sells it |
| own_public_record (url + quote) | the first line of the touch (distribution-channel rule 11) |
| contact_route | how a draft reaches them |

### Report (sale)
| field | answers |
|---|---|
| applicant, city, licence_type, parcels[], generated_at, price, paid_at, delivered_at | the transaction and its ledger row |

## Reality check — filled in below as it is tested
