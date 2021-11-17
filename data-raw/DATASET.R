# 1. DATASET --------------------------------------------------------------

# Alle politisch selbständigen Gemeinden mit ausgewählten Merkmalen
# https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/_inhalt.html
library(readxl)
library(tidyverse)

if (!file.exists("data-raw/AuszugGV3QAktuell.xlsx")) {
  download.file("https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/GVAuszugQ/AuszugGV3QAktuell.xlsx?__blob=publicationFile", "AuszugGV3QAktuell.xlsx", quiet = TRUE)
}


DATASET <- readxl::read_excel(path = "data-raw/AuszugGV3QAktuell.xlsx", sheet = 2, skip = 6, col_names = FALSE) %>%
  dplyr::select(3:5, 8) %>%
  tidyr::unite(id , 1:3, sep = "") %>%
  dplyr::rename(landkreis = 2) %>%
  dplyr::filter(!stringr::str_detect(id, pattern = "NA")) %>%
  dplyr::distinct(id, .keep_all = TRUE)



# 2. available_districts --------------------------------------------------

# Search for all available ids that give a response
get_resp <- function(id){
  httr::status_code(httr::GET(paste0("https://statistik.arbeitsagentur.de/Statistikdaten/Detail/202108/ama/amr-amr/amr-", id,"-0-202108-xlsx.xlsx?__blob=publicationFile&v=1")))
}


available_districts <- DATASET %>%
  dplyr::mutate(resp = purrr::map_chr(id, get_resp))




# kpi_names ---------------------------------------------------------------

kpi_names <- c(
  "arbeitssuchend", # 13, # Bestand an Arbeitssuchenden
  "arbeitslos", # 15, # Bestand an Arbeitslosen
  "arbeitslos_m", # 16, # Arbeitslosen M
  "arbeitslos_w", # 17, # Arbeitslosen W
  "arbeitslos_zugang", # 28, # Zugang an Arbeitslosen
  "arbeitslos_abgang", # 35, # Abgang an Arbeitslosen
  "arbeitslos_quote", # 42, # ALQ
  "arbeitsstellen_zugang", # 62, # Zugang Gemeldete Arbeitstellen
  "arbeitsstellen_jahreszugang", # 63, # Zugang seit Jahresbeginn
  "arbeitsstellen" # 64, # Bestand gemeldete Arbeitstellen
)


usethis::use_data(DATASET, available_districts, kpi_names, internal = TRUE,  overwrite = TRUE)
# All functions within the package can freely access the DATASET and available_districts datasets, but the user won’t see them.
# to access the data within the package use: mypackage:::x
