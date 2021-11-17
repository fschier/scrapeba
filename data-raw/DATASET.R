## code to prepare `DATASET` dataset goes here

# Alle politisch selbständigen Gemeinden mit ausgewählten Merkmalen
# https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/_inhalt.html
library(readxl)
library(tidyverse)

if (!file.exists("data-raw/AuszugGV3QAktuell.xlsx")) {
  download.file("https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/GVAuszugQ/AuszugGV3QAktuell.xlsx?__blob=publicationFile", "AuszugGV3QAktuell.xlsx", quiet = TRUE)
}


DATASET <- read_excel(path = "data-raw/AuszugGV3QAktuell.xlsx", sheet = 2, skip = 6, col_names = FALSE) %>%
  select(3:5, 8) %>%
  unite(id , 1:3, sep = "") %>%
  rename(landkreis = 2) %>%
  filter(!str_detect(id, pattern = "NA")) %>%
  distinct(id, .keep_all = TRUE)


usethis::use_data(DATASET, internal = TRUE, overwrite = TRUE)
