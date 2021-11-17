## code to prepare `DATASET` dataset goes here

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




# Search for all available ids that give a response
get_resp <- function(id){
  httr::status_code(httr::GET(paste0("https://statistik.arbeitsagentur.de/Statistikdaten/Detail/202108/ama/amr-amr/amr-", id,"-0-202108-xlsx.xlsx?__blob=publicationFile&v=1")))
}


available_districts <- DATASET %>%
  dplyr::mutate(resp = purrr::map_chr(id, get_resp))


usethis::use_data(DATASET, available_districts, internal = TRUE,  overwrite = TRUE)
# All functions within the package can freely access the DATASET and available_districts datasets, but the user won’t see them.
# to access the data within the package use: mypackage:::x
