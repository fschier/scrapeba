#' Get data for all districts
#'
#' @param year A string or numeric value containing the year.
#' @param month A string or numeric value containing the month.
#'
#' @return A data.frame.
#' @export
#'
#' @examples
#' get_data(id = c("09571", "05558"), year = "2021", month = "10")

get_data <- function(year = "2021", month = "10"){

 id <- scrapeba:::available_districts %>%
    dplyr::filter(resp == 200) %>%
    dplyr::pull(id)

 pb = utils::txtProgressBar(min = 0, max = 400, initial = 0)
 stepi = 0

  for(i in id){
    tmp <- get_district(id = i,  year = year, month = month)

    if (!exists("data_output")) {
      data_output <- tmp
      } else {
      data_output <- rbind(data_output, tmp)
      }

    stepi = stepi + 1
    utils::setTxtProgressBar(pb, stepi)
    base::close(pb)
    base::Sys.sleep(1)
  }

  return(data_output)
}
