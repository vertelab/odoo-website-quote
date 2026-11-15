# odoo-website-quote — gren 19.0

> **Denna gren är avsiktligt tom.** Modulerna är INTE portade till Odoo 19.
> Grenen finns så att dev-miljöer (`hansolo19`) kan klona den utan att falla,
> men den påstår ingenting om att koden är portad.

## Baseline

| | |
|---|---|
| Källa | `20.0` |
| Moduler | **4** |
| Grenar i repot | `12.0`, `14.0`, `16.0`, `18.0`, `20.0`, `master`, `master10` |

## Moduler

- `website_quote_contract_project`
- `website_quote_header`
- `website_quote_monthly`
- `website_quote_monthly_uom`

## Blockerare

**1 externa beroenden saknas** i Odoo 19-kärnan och OCA 19.0:

| Beroende | Behövs av |
|---|---|
| `sale_quotation_builder` | `website_quote_header` |

### Prioritering

Ett beroende som blockerar många moduler ger mest nytta att lösa först:

- `sale_quotation_builder` — frisläpper **1** modul(er)

## Nästa steg

Portering sker på `*-pfile`-maskin med versionsagnostisk kod
(`.p.py` / `.p.xml`). Se `/skill:odoo-pfiles`.
