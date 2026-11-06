# Launch the R notebook from the repository root.
data_dir <- path.expand(Sys.getenv("HSSC_DATA_DIR", "data"))
output_dir <- path.expand(Sys.getenv("HSSC_OUTPUT_DIR", "outputs"))

read_input <- function(name) {
  plain <- file.path(data_dir, name)
  zipped <- paste0(plain, ".zip")
  if (file.exists(plain)) return(read.csv(plain))
  if (file.exists(zipped)) {
    members <- unzip(zipped, list = TRUE)$Name
    csv_members <- members[grepl("\\.csv$", members, ignore.case = TRUE)]
    if (length(csv_members) != 1L) stop("The input ZIP must contain exactly one CSV: ", zipped)
    connection <- unz(zipped, csv_members[[1]])
    on.exit(close(connection))
    return(read.csv(connection))
  }
  stop("Required input is missing: ", plain, " (or .zip). See README.md.")
}

output_file <- function(name) {
  dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
  file.path(output_dir, name)
}
