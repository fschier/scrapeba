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
      which = 5,
      col_names = FALSE
      ))) %>%
    dplyr::select(1,4) %>%
    dplyr::rename(kpi = 1, value = 2)

  district  <- data[4,1]

  data <- data %>%
    dplyr::slice(
      13, # Bestand an Arbeitssuchenden
      15, # Bestand an Arbeitslosen
      16, # Arbeitslosen M
      17, # Arbeitslosen W
      28, # Zugang an Arbeitslosen
      35, # Abgang an Arbeitslosen
      42, # ALQ
      62, # Zugang Gemeldete Arbeitstellen
      63, # Zugang seit Jahresbeginn
      64, # Bestand gemeldete Arbeitstellen
    ) %>%
    dplyr::mutate(
      district = district,
      year = year,
      month = month
    ) %>%
    base::cbind(kpi_names = scrapeba:::kpi_names) %>%
    dplyr::select(-kpi) %>%
    tidyr::pivot_wider(names_from = kpi_names, values_from = value)

  return(data)

}




# https://statistik.arbeitsagentur.de/Statistikdaten/Detail/202110/ama/amr-amr/amr-09571-0-202110-xlsx.xlsx?__blob=publicationFile&v=1



