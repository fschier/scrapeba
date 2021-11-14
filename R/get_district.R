
strsplit1 <- function(x, split) {
  strsplit(x, split = split)[[1]]
}



get_district <- function(){
  rio::import(
    file = paste0("https://statistik.arbeitsagentur.de/Statistikdaten/Detail/202110/ama/amr-amr/amr-09571-0-202110-xlsx.xlsx?__blob=publicationFile&v=1"),
    format = "xlsx",
    which = 5
    )
}




# https://statistik.arbeitsagentur.de/Statistikdaten/Detail/202110/ama/amr-amr/amr-09571-0-202110-xlsx.xlsx?__blob=publicationFile&v=1



