get_data <- function(id = "09571",  year = "2021", month = "10"){

  for(i in id){
    tmp <- get_district(id = i,  year = year, month = month)

    if (!exists("data_output")) {
      data_output <- tmp
      } else {
      data_output <- rbind(data_output, tmp)
      }
  }

  return(data_output)
}
