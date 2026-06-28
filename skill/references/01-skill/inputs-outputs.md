# Inputs And Outputs

Use this file to define what the skill needs and what it should produce.

## Inputs

Required or inferred inputs:

- website URL, page list, sitemap, screenshots, user journey, or written brief;
- business goal and analysis needs when known;
- expected user actions and success signals;
- existing tracking-plan template, naming convention, or previous GA4/GTM
  documentation when available;
- analytics platform scope: GA4 by default, Piano Analytics only when requested
  or clearly in scope;
- implementation context, such as GTM, dataLayer, gtag.js, CMS, ecommerce
  platform, SPA routing, server-side tagging, or unknown;
- available data, such as page metadata, product data, cart/order data, form
  metadata, user state, and consent state;
- privacy, PII, legal, regional, or technical constraints;
- historical tracking plans only as generic learning material.

If implementation context is unknown, assume standard GTM web container plus
dataLayer and flag the assumption.

## Outputs

Possible outputs:

- human-readable XLSX tracking plan;
- structured JSON plan for validation and future automation;
- long-format CSV for review, diffing, or QA ingestion;
- measurement brief and assumptions;
- measurement strategy and scalability notes;
- journey-grouped Event Matrix;
- Parameter Reference with value rules and examples;
- GTM Protocol;
- Screenshot Register;
- QA Cases;
- key event recommendations;
- custom definition recommendations;
- not-tracked decisions;
- documentation sources checked.

## Default Workbook

The XLSX workbook is the main human deliverable. The Event Matrix should be the
main working tab. Overview, GTM Protocol, Parameter Reference, Screenshot
Register, and QA Cases should support the Event Matrix without becoming dense
or filled with internal reasoning.
