#' Get labour data for district and timestamp
#'
#' @param id A string or numeric value containing the district id.
#' @param year A string or numeric value containing the year.
#' @param month A string or numeric value containing the month.
#'
#' @return A data.frame.
#' @export
#'
#' @examples
#' get_district(id = "09571", year = "2021", month = "10")


get_district <- function(id = "09571", year = "2021", month = "10"){

  # declase file url based on given 'id', 'year' and month'
  file <- paste0("https://statistik.arbeitsagentur.de/Statistikdaten/Detail/",
                 year,
                 month,
                 "/ama/amr-amr/amr-",
                 id,
                 "-0-202110-xlsx.xlsx?__blob=publicationFile&v=1")


  #import file and wrangle dataset
  data <- base::suppressMessages(base::suppressWarnings(
    rio::import(
      file = file,
      format = "xlsx",
      which = 5
      ))) %>%
    dplyr::select(1,4)

  district  <- data[3,1]

  data <- data %>%
    dplyr::mutate(
      district = district,
      year = year,
      month = month
    )

  return(data)

}




# https://statistik.arbeitsagentur.de/Statistikdaten/Detail/202110/ama/amr-amr/amr-09571-0-202110-xlsx.xlsx?__blob=publicationFile&v=1



