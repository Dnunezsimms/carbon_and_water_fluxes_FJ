# 01. Reference diagnosis

Date: 2026-06-17  
Source file: `C:\projects\carbon_and_water_fluxes_FJ_public\docs\Nunez-Simms manuscript-revised.docx`

## Summary

- References heading detected: `References`
- Raw non-empty items after heading: `91`
- Supplementary items detected after references: `6`
- True references after separating supplementary material and fixing one merged line: `92`

## Main inconsistencies detected

- Mixed year formatting: some references used `(Year)` while others used `, Year.`
- Mixed author formatting: initials appeared both compact (`J.R.`) and spaced (`J. R.`)
- Extra commas before the year in several entries
- Inconsistent source punctuation before volume details
- Mixed treatment of URLs and DOIs
- One merged reference entry was detected and separated manually: `CONAF, 2014...` + `Collins et al. (2014)`
- The section continues into `Supplementary Material`, so references do not extend to the end of the document

## Pattern counts

- References with year outside parentheses: `18`
- References with extra comma before year: `39`
- References with compact initials needing spacing cleanup: `34`
- References containing URL / available-at style links: `5`
- References using `et al.` in the reference list itself: `3`
- References manually fixed because generic normalization was not enough: `28`

## References likely needing manual verification

- Armesto, J. J., Vidiella, P. E., & Gutierrez, J. R. (1993). Plant communities of the fog-free coastal desert of Chile: Plant strategies in a fluctuating environment. Revista Chilena de Historia Natural, 66, 271–282. Available at: https://rchn.biologiachile.cl/pdfs/1993/3/Armesto_et_al_1993.pdf
- CEAZA (2025). Ceazamet climate bulletin – Coquimbo Region. Available at: https://boletin.ceazamet.cl/index.php?pag=historicos
- CONAF (2014). Regional file 68063: Coquimbo region. Available at: https://sit.conaf.cl/exp/ficha.php.
- General Water Directorate of Chile (DGA) (2021). Development of a 3D groundwater storage model for drought management in the Limarí River basin. Technical report, Ministry of Public Works, Chile. Available at: https://aguasubterranealimari.cl/ Accessed December 16, 2025.
- Gutiérrez, J.R., Troncoso, A.J., Milstead, B., Previtali, A., & Meserve, P.L. (2006–2024). Monthly precipitation dataset for Bosque Fray Jorge National Park (Fray Jorge LTSER). Universidad de La Serena & CEAZAMET. Unpublished curated dataset.
- Meteorological Directorate of Chile (2013). Historical Records of annual precipitation in Chile (1913–2013). Available at: https://climatologia.meteochile.gob.cl
- Moreno, A., et al. (2021). Satellite-based estimation of ecosystem carbon fluxes in drylands: Model evaluation and uncertainty analysis. Agricultural and Forest Meteorology, 297, 108273. https://doi.org/10.1016/j.agrformet.2020.108273
- Previtali, A., & Gutiérrez, J.R. (1990–2005). Historical precipitation Records for Bosque Fray Jorge National Park (CONAF weather station and field notes). Fray Jorge LTSER, Chile. Unpublished dataset.
- Reed, S. C., et al. (2015). Shrubland carbon sinks in southern Africa: Implications for global dryland carbon balance. Global Change Biology, 21(7), 2549–2560. https://doi.org/10.1111/gcb.12863
- Zhou, Q., et al. (2019). A machine learning approach in a semi-arid landscape. Scientific Reports, 9(1), 1–10. https://doi.org/10.1038/s41598-019-38639-y

## Probable non-journal or gray-literature references

- General Water Directorate of Chile (DGA) (2021). Development of a 3D groundwater storage model for drought management in the Limarí River basin. Technical report, Ministry of Public Works, Chile. Available at: https://aguasubterranealimari.cl/. Accessed December 16, 2025.
- Gutiérrez, J.R., Troncoso, A.J., Milstead, B., Previtali, A., & Meserve, P.L. (2006–2024). Monthly precipitation dataset for Bosque Fray Jorge National Park (Fray Jorge LTSER). Universidad de La Serena & CEAZAMET. Unpublished curated dataset.
- Previtali, A., & Gutiérrez, J.R. (1990–2005). Historical precipitation Records for Bosque Fray Jorge National Park (CONAF weather station and field notes). Fray Jorge LTSER, Chile. Unpublished dataset.
- Sala, O.E., Yahdjian, L., Havstad, K., & Aguiar, M.R., (2012). Rangeland ecosystem services: Nature’s supply and humans’ demand. In Rangeland Systems (pp. 467–489). Springer. https://doi.org/10.1007/978-3-319-46709-2_13
- Soil Survey Staff. (2022). Soil Taxonomy: A Basic System of Soil Classification for Making and Interpreting Soil Surveys (2nd ed.). USDA–Natural Resources Conservation Service, Washington, DC.
- Squeo, F.A. & F.A. Méndez. 2019. Reserva de Biósfera Fray Jorge: más que un bosque relicto de neblina. En: (C. Smith-Ramírez y F.A. Squeo, eds) Biodiversidad y Ecología de los Bosques Costeros de Chile: 223-237. Editorial Universidad de Los Lagos, Osorno, Chile
- Stull, R.B., (1988). An Introduction to Boundary Layer Meteorology. Springer. https://doi.org/10.1007/978-94-009-3027-8
- Therneau, T., & Atkinson, B., (2019). rpart: Recursive partitioning and regression trees (R package version 4.1-15). Comprehensive R Archive Network (CRAN). https://CRAN.R-project.org/package=rpart

## Duplicates

No exact probable duplicates were detected after normalization.

## Editorial decision used for homogenization

Because no explicit bibliography style was identified in the document text, the references were normalized to a consistent author-year style close to Harvard / APA-like formatting:

`Surname, A. A., Surname, B. B., & Surname, C. C. (Year). Title. Source, volume(issue), pages. DOI/URL`

This was applied conservatively without inventing missing bibliographic fields.
