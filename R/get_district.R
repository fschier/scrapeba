
#' Split a string
#'
#' @param x A character vector with one element.
#' @param split What to split on.
#'
#' @return A character vector.
#' @export
#'
#' @examples
#' x <- "alfa,bravo,charlie,delta"
#' strsplit(x, split = ",")
strsplit1 <- function(x, split) {
  strsplit(x, split = split)[[1]]
}



get_district <- function(id = "09571", year = "2021", month = "10"){

  file <- paste0("https://statistik.arbeitsagentur.de/Statistikdaten/Detail/",
                 yearmonth,
                 "/ama/amr-amr/amr-",
                 id,
                 "-0-202110-xlsx.xlsx?__blob=publicationFile&v=1")

  data <- rio::import(
    file = file,
    format = "xlsx",
    which = 5
    ) %>%
    select(1,4)

  district  <- data[3,1]

  data <- data %>%
    mutate(
      district = district,
      year = year,
      month = month
    )

}


x %>%
  select(1,4) %>% View() %>%
  mutate(landkreis = )

# https://statistik.arbeitsagentur.de/Statistikdaten/Detail/202110/ama/amr-amr/amr-09571-0-202110-xlsx.xlsx?__blob=publicationFile&v=1



