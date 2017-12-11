
<!-- rnb-text-begin -->

---
title: "Process all the data"
output: html_notebook
---

Step 0: Read in libraries 


<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuI3JtKGxpc3Q9bHMoKSlcbmxpYnJhcnkodGlkeXZlcnNlKVxuI2xpYnJhcnkocHVycnIpXG5saWJyYXJ5KGRhdGEudGFibGUpXG5saWJyYXJ5KGphbml0b3IpXG5saWJyYXJ5KG5vbmNlbnN1cylcbmxpYnJhcnkoem9vKVxuIyBsaWJyYXJ5KHBseXIpXG5cbiNsaWJyYXJ5KGxtdGVzdClcbiNsaWJyYXJ5KHBseXIpXG4jbGlicmFyeSh0aWR5dmVyc2UpXG4jbGlicmFyeShnZ3Bsb3QyKVxuI2xpYnJhcnkoZ2dyZXBlbClcbiNsaWJyYXJ5KEdHYWxseSlcbiNsaWJyYXJ5KGx1YnJpZGF0ZSlcbmBgYCJ9 -->

```r
#rm(list=ls())
library(tidyverse)
#library(purrr)
library(data.table)
library(janitor)
library(noncensus)
library(zoo)
# library(plyr)

#library(lmtest)
#library(plyr)
#library(tidyverse)
#library(ggplot2)
#library(ggrepel)
#library(GGally)
#library(lubridate)
```

<!-- rnb-source-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->



Step 2: Read in files

<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuIyBteS5kaXJlY3RvcnkgPC0gXCJ+L0RvY3VtZW50cy9EYXRhX1NjaWVuY2UvU3RhdF9JbmZlcmVuY2VfSS9wcm9qZWN0XzEvZGF0YS9cIlxubXkuZGlyZWN0b3J5IDwtIFwifi9Hb29nbGUgRHJpdmUvc3RhdC9VRk9UcmFja2VyL2RhdGFcIlxuIyBzZXR3ZChteS5kaXJlY3RvcnkpXG5zZXR3ZChteS5kaXJlY3RvcnkpXG5iZWVyLnBhdGggPC0gXCJyYXcvYnJld19jb3VudF9ieV9zdGF0ZV8xOTg0XzIwMTcuY3N2XCJcbm1vdmllcy5wYXRoIDwtIFwicmF3L2FsaWVuX21vdmllc19wZXJfeWVhci5jc3ZcIlxuZ2RwLnBhdGg8LSBcInJhdy9nZHBfcGVyX2NhcGl0YV9wZXJfeWVhci5jc3ZcIlxuaW50ZXJuZXQucnVyYWxpdHkucGF0aCA8LSBcInJhdy9pbnRlcm5ldF9ieV9ydXJhbGl0eS5jc3ZcIlxudXNhZmJhc2UucGF0aCA8LSBcInJhdy91c2FmX2Jhc2VfbG9jcy5jc3ZcIlxuc3RhdGVwb3BzLnBhdGggPC0gXCJyYXcvc3RhdGVfcG9wcy5jc3ZcIlxuc2lnaHRpbmdzLnBhdGggPC0gXCJyYXcvdWZvX3NpZ2h0aW5ncy5jc3ZcIlxuYWxsbW92aWVzLnBhdGggPC0gXCJyYXcvbnVtYmVyX29mX21vdmllc19wZXJfeWVhci5jc3ZcIlxuc3RhdGVwb3BzMy5wYXRoIDwtIFwicmF3L3N0YXRlcG9wcy5kYjMuY3N2XCJcblxuXG5iZWVyLnJhdyA8LSBmcmVhZChmaWxlLnBhdGgobXkuZGlyZWN0b3J5LCBiZWVyLnBhdGgpLCBoZWFkZXI9VFJVRSwgbmEuc3RyaW5ncz1jKFwiKlwiLCBcIlwiKSlcblxuc2lnaHRpbmdzLnJhdyA8LSBmcmVhZChmaWxlLnBhdGgobXkuZGlyZWN0b3J5LCBzaWdodGluZ3MucGF0aCksIGhlYWRlciA9IFRSVUUsIG5hLnN0cmluZ3MgPSBjKFwiXCIsIFwiVW5rbm93blwiLCBcIi0tXCIpKVxuXG5tb3ZpZXMucmF3IDwtIGZyZWFkKGZpbGUucGF0aChteS5kaXJlY3RvcnksIG1vdmllcy5wYXRoKSwgaGVhZGVyID0gVFJVRSlcblxuZ2RwLnJhdyA8LSBmcmVhZChmaWxlLnBhdGgobXkuZGlyZWN0b3J5LCBnZHAucGF0aCksIGhlYWRlciA9IFRSVUUpXG5cbmludGVybmV0LnJ1cmFsaXR5LnJhdyA8LSBmcmVhZChmaWxlLnBhdGgobXkuZGlyZWN0b3J5LCBpbnRlcm5ldC5ydXJhbGl0eS5wYXRoKSwgaGVhZGVyID0gVFJVRSlcblxudXNhZmJhc2UucmF3IDwtIGZyZWFkKGZpbGUucGF0aChteS5kaXJlY3RvcnksIHVzYWZiYXNlLnBhdGgpLCBoZWFkZXIgPSBUUlVFLCBuYS5zdHJpbmdzID0gYyhcIlwiKSlcblxuc3RhdGVwb3BzLnJhdyA8LSBmcmVhZChmaWxlLnBhdGgobXkuZGlyZWN0b3J5LCBzdGF0ZXBvcHMucGF0aCksIGhlYWRlciA9IFRSVUUpXG5cbiNhbGxfbW92aWVzIDwtIHJlYWQuY3N2KGZpbGUgPSBcIi4uLy4uL2RhdGEvcmF3L251bWJlcl9vZl9tb3ZpZXNfcGVyX3llYXIuY3N2XCIsIGhlYWQgPSBUUlVFKVxuYWxsbW92aWVzLnJhdyA8LSBmcmVhZChmaWxlLnBhdGgobXkuZGlyZWN0b3J5LCBhbGxtb3ZpZXMucGF0aCksIGhlYWRlciA9IFRSVUUpXG5cbnN0YXRlcG9wczMucmF3IDwtIHJlYWRfY3N2KGZpbGUucGF0aChteS5kaXJlY3RvcnksIHN0YXRlcG9wczMucGF0aCkpXG5cblxuYGBgIn0= -->

```r
# my.directory <- "~/Documents/Data_Science/Stat_Inference_I/project_1/data/"
my.directory <- "~/Google Drive/stat/UFOTracker/data"
# setwd(my.directory)
setwd(my.directory)
beer.path <- "raw/brew_count_by_state_1984_2017.csv"
movies.path <- "raw/alien_movies_per_year.csv"
gdp.path<- "raw/gdp_per_capita_per_year.csv"
internet.rurality.path <- "raw/internet_by_rurality.csv"
usafbase.path <- "raw/usaf_base_locs.csv"
statepops.path <- "raw/state_pops.csv"
sightings.path <- "raw/ufo_sightings.csv"
allmovies.path <- "raw/number_of_movies_per_year.csv"
statepops3.path <- "raw/statepops.db3.csv"


beer.raw <- fread(file.path(my.directory, beer.path), header=TRUE, na.strings=c("*", ""))

sightings.raw <- fread(file.path(my.directory, sightings.path), header = TRUE, na.strings = c("", "Unknown", "--"))

movies.raw <- fread(file.path(my.directory, movies.path), header = TRUE)

gdp.raw <- fread(file.path(my.directory, gdp.path), header = TRUE)

internet.rurality.raw <- fread(file.path(my.directory, internet.rurality.path), header = TRUE)

usafbase.raw <- fread(file.path(my.directory, usafbase.path), header = TRUE, na.strings = c(""))

statepops.raw <- fread(file.path(my.directory, statepops.path), header = TRUE)

#all_movies <- read.csv(file = "../../data/raw/number_of_movies_per_year.csv", head = TRUE)
allmovies.raw <- fread(file.path(my.directory, allmovies.path), header = TRUE)

statepops3.raw <- read_csv(file.path(my.directory, statepops3.path))

```

<!-- rnb-source-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->



Step 3: Data cleaning  


<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuIyBjbGVhbiB1cCBmaWxlXG5iZWVyLmRiIDwtIGJlZXIucmF3ICU+JSBcbiAgZmlsdGVyKCFpcy5uYShTVEFURSkpICU+JVxuICBmaWx0ZXIoU1RBVEUgIT0gXCJUb3RhbFwiKSAlPiUgXG4gIGZpbHRlcihTVEFURSAhPSBcIk90aGVyXCIpICU+JSBcbiAgZmlsdGVyKFNUQVRFICE9IFwiKiBObyByZXBvcnRhYmxlIGRhdGFcIikgJT4lIFxuICBmaWx0ZXIoU1RBVEUgIT0gXCLCq1RoaXMgbGlzdCB3aWxsIGJlIHVwZGF0ZWQgcXVhcnRlcmx5LlwiKSAlPiUgXG4gIHJlbmFtZShzdGF0ZSA9IFNUQVRFKSAlPiUgXG4gIG11dGF0ZShzdGF0ZSA9IGFzLmZhY3RvcihzdGF0ZSkpICU+JVxuICBnYXRoZXJfKFwieWVhclwiLCBcImJyZXdlcmllc1wiLCBhcy5jaGFyYWN0ZXIoc2VxKDE5ODQsIDIwMTcpKSkgJT4lXG4gIG11dGF0ZShicmV3ZXJpZXMgPSBhcy5udW1lcmljKGJyZXdlcmllcykpICU+JVxuICBmaWx0ZXIoeWVhciA+PSAxOTg0KSAlPiVcbiAgZmlsdGVyKHllYXIgPD0gMjAxNikgJT4lXG4gICMgZmlsdGVyKHN0YXRlID09IFwiRkxcIikgJT4lXG4gIG11dGF0ZSh5ZWFyID0gYXMubnVtZXJpYyh5ZWFyKSlcbiAgXG5gYGAifQ== -->

```r
# clean up file
beer.db <- beer.raw %>% 
  filter(!is.na(STATE)) %>%
  filter(STATE != "Total") %>% 
  filter(STATE != "Other") %>% 
  filter(STATE != "* No reportable data") %>% 
  filter(STATE != "«This list will be updated quarterly.") %>% 
  rename(state = STATE) %>% 
  mutate(state = as.factor(state)) %>%
  gather_("year", "breweries", as.character(seq(1984, 2017))) %>%
  mutate(breweries = as.numeric(breweries)) %>%
  filter(year >= 1984) %>%
  filter(year <= 2016) %>%
  # filter(state == "FL") %>%
  mutate(year = as.numeric(year))
  
```

<!-- rnb-source-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->


Group the states into regions.   

<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuZGF0YShzdGF0ZXMpXG5gYGAifQ== -->

```r
data(states)
```

<!-- rnb-source-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->



<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuIyB4ID0gc3RhdGVwb3BzLmRiJHllYXIgXG4jIHggLSAoeCAlJSAxMClcbmBgYCJ9 -->

```r
# x = statepops.db$year 
# x - (x %% 10)
```

<!-- rnb-source-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->



<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuc3RhdGVwb3BzLmRiIDwtIHN0YXRlcG9wcy5yYXcgJT4lIFxuICAjZ2F0aGVyXyhcIk5hbWVcIiwgXCJ5ZWFyXCIsIFwicG9wdWxhdGlvblwiKVxuICBnYXRoZXJfKFwieWVhclwiLCBcInBvcHVsYXRpb25cIiwgYXMuY2hhcmFjdGVyKHNlcSgxOTYwLDIwMTAsMTApKSkgJT4lIFxuICBmaWx0ZXIoTmFtZSAlaW4lIHN0YXRlLm5hbWUpICU+JSBcbiAgbXV0YXRlKHllYXIgPSBhcy5pbnRlZ2VyKHllYXIpKSAlPiUgXG4gIG11dGF0ZShwb3B1bGF0aW9uID0gYXMubnVtZXJpYyhnc3ViKFwiLFwiLCBcIlwiLCBwb3B1bGF0aW9uKSkpXG4gICMgbXV0YXRlKHBvcHVsYXRpb24gPSBhcy5pbnRlZ2VyKHBvcHVsYXRpb24pKVxuICAjIGdzdWIoXCIsXCIsIFwiXCIsIHBvcHVsYXRpb24pXG4gICMgbXV0YXRlKHBvcHVsYXRpb24gPSBhcy5udW1lcmljKGdzdWIoXCIsXCIsIFwiXCIsIHBvcHVsYXRpb24pKVxuICBcbmBgYCJ9 -->

```r
statepops.db <- statepops.raw %>% 
  #gather_("Name", "year", "population")
  gather_("year", "population", as.character(seq(1960,2010,10))) %>% 
  filter(Name %in% state.name) %>% 
  mutate(year = as.integer(year)) %>% 
  mutate(population = as.numeric(gsub(",", "", population)))
  # mutate(population = as.integer(population))
  # gsub(",", "", population)
  # mutate(population = as.numeric(gsub(",", "", population))
  
```

<!-- rnb-source-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->




<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuc3RhdGVwb3BzLmRiMiA8LSBzdGF0ZXBvcHMucmF3ICU+JSBcbiAgZmlsdGVyKE5hbWUgJWluJSBzdGF0ZS5uYW1lKSAgXG5zdGF0ZXBvcHMuZGIzIDwtIGRhdGEuZnJhbWUodChzdGF0ZXBvcHMuZGIyKSlcbmBgYCJ9 -->

```r
statepops.db2 <- statepops.raw %>% 
  filter(Name %in% state.name)  
statepops.db3 <- data.frame(t(statepops.db2))
```

<!-- rnb-source-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->



<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxubGlicmFyeShkYXRldGltZSlcbnlycyA8LSAxOTcwOjIwMTZcbnlycyA8LSB6b28oTkEsIGFzLnllYXIoeXJzKSlcbnpwb3BzIDwtIHpvbyhzZWxlY3Qoc3RhdGVwb3BzMy5yYXcsIC15ZWFyKSwgYXMueWVhcihzdGF0ZXBvcHMzLnJhdyR5ZWFyKSlcbnogPC0gbWVyZ2UoeXJzLCB6cG9wcylcbnogPC0gelssY29sbmFtZXMoeikgIT0gXCJ5cnNcIl1cbmludGVycHMgPC0gbmEuc3BsaW5lKHopXG5pbnRlcnBzIDwtIGFzLmRhdGEuZnJhbWUoaW50ZXJwcylcbmludGVycHMkeWVhciA8LSByb3duYW1lcyhpbnRlcnBzKVxuY29sbmFtZXMoaW50ZXJwcykgPC0gbWFwdmFsdWVzKGNvbG5hbWVzKGludGVycHMpLCBzdGF0ZS5uYW1lLCBzdGF0ZS5hYmIpXG5pbnRlcnBzIDwtIGludGVycHMgJT4lXG4gICAgZmlsdGVyKHllYXIgPj0gMTk3NClcbndyaXRlX2NzdihpbnRlcnBzLCBcIi4vcmF3L2ludGVycG9sYXRlZF9wb3BzLmNzdlwiKVxuYGBgIn0= -->

```r
library(datetime)
yrs <- 1970:2016
yrs <- zoo(NA, as.year(yrs))
zpops <- zoo(select(statepops3.raw, -year), as.year(statepops3.raw$year))
z <- merge(yrs, zpops)
z <- z[,colnames(z) != "yrs"]
interps <- na.spline(z)
interps <- as.data.frame(interps)
interps$year <- rownames(interps)
colnames(interps) <- mapvalues(colnames(interps), state.name, state.abb)
interps <- interps %>%
    filter(year >= 1974)
write_csv(interps, "./raw/interpolated_pops.csv")
```

<!-- rnb-source-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->




<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuc2lnaHRpbmdzLnJhdyA8LSByZWFkX2NzdihcIi4vcmF3L3Vmb19zaWdodGluZ3MuY3N2XCIpXG5gYGAifQ== -->

```r
sightings.raw <- read_csv("./raw/ufo_sightings.csv")
```

<!-- rnb-source-end -->

<!-- rnb-output-begin eyJkYXRhIjoiTWlzc2luZyBjb2x1bW4gbmFtZXMgZmlsbGVkIGluOiAnWDEnIFsxXVBhcnNlZCB3aXRoIGNvbHVtbiBzcGVjaWZpY2F0aW9uOlxuY29scyhcbiAgWDEgPSBjb2xfaW50ZWdlcigpLFxuICBjaXR5ID0gY29sX2NoYXJhY3RlcigpLFxuICBkYXRlX3RpbWUgPSBjb2xfY2hhcmFjdGVyKCksXG4gIGR1cmF0aW9uID0gY29sX2NoYXJhY3RlcigpLFxuICBwb3N0ZWQgPSBjb2xfY2hhcmFjdGVyKCksXG4gIHNoYXBlID0gY29sX2NoYXJhY3RlcigpLFxuICBzdGF0ZSA9IGNvbF9jaGFyYWN0ZXIoKSxcbiAgc3VtbWFyeSA9IGNvbF9jaGFyYWN0ZXIoKVxuKVxuIn0= -->

```
Missing column names filled in: 'X1' [1]Parsed with column specification:
cols(
  X1 = col_integer(),
  city = col_character(),
  date_time = col_character(),
  duration = col_character(),
  posted = col_character(),
  shape = col_character(),
  state = col_character(),
  summary = col_character()
)
```



<!-- rnb-output-end -->

<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuc2lnaHRpbmdzLmRiIDwtIHNpZ2h0aW5ncy5yYXcgJT4lIFxuICAjZmlsdGVyKHN0YXRlPT0nRkwnKSAlPiUgXG4gIGRwbHlyOjptdXRhdGUoc3RhdGUgPSB0b3VwcGVyKHN0YXRlKSkgJT4lIFxuICBkcGx5cjo6bXV0YXRlKHllYXIgPSBhcy5udW1lcmljKGZvcm1hdChhcy5EYXRlKGRhdGVfdGltZSwgZm9ybWF0PVwiJW0vJWQvJXlcIiksXCIlWVwiKSkpICU+JSBcbiAgZHBseXI6OmZpbHRlcihzdGF0ZSAlaW4lIHN0YXRlLmFiYikgJT4lIFxuICBkcGx5cjo6ZmlsdGVyKHllYXIgPj0gMTk3NCkgJT4lIFxuICBkcGx5cjo6ZmlsdGVyKHllYXIgPD0gMjAxNikgJT4lXG4gIGRwbHlyOjpjb3VudCh5ZWFyLCBzdGF0ZSkgJT4lIFxuICBkcGx5cjo6cmVuYW1lKG51bV9zaWdodGluZ3MgPSBuKSAlPiVcbiAgZHBseXI6OmxlZnRfam9pbihzdGF0ZXMsIGJ5ID0gYyhcInN0YXRlXCIgPSBcInN0YXRlXCIpKSAlPiVcbiAgZHBseXI6OnNlbGVjdCgtYXJlYSwgLXBvcHVsYXRpb24sIC1kaXZpc2lvbiwgLWNhcGl0YWwpICU+JVxuICBkcGx5cjo6bXV0YXRlKGRlY2FkZSA9IHllYXIgLSAoeWVhciAlJSAxMCkpXG5gYGAifQ== -->

```r
sightings.db <- sightings.raw %>% 
  #filter(state=='FL') %>% 
  dplyr::mutate(state = toupper(state)) %>% 
  dplyr::mutate(year = as.numeric(format(as.Date(date_time, format="%m/%d/%y"),"%Y"))) %>% 
  dplyr::filter(state %in% state.abb) %>% 
  dplyr::filter(year >= 1974) %>% 
  dplyr::filter(year <= 2016) %>%
  dplyr::count(year, state) %>% 
  dplyr::rename(num_sightings = n) %>%
  dplyr::left_join(states, by = c("state" = "state")) %>%
  dplyr::select(-area, -population, -division, -capital) %>%
  dplyr::mutate(decade = year - (year %% 10))
```

<!-- rnb-source-end -->

<!-- rnb-output-begin eyJkYXRhIjoiQ29sdW1uIGBzdGF0ZWAgam9pbmluZyBjaGFyYWN0ZXIgdmVjdG9yIGFuZCBmYWN0b3IsIGNvZXJjaW5nIGludG8gY2hhcmFjdGVyIHZlY3RvclxuIn0= -->

```
Column `state` joining character vector and factor, coercing into character vector
```



<!-- rnb-output-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->


### Normalize the number of sightings by the population of each state df$sightings_per_thousand <- (df$sightings / df$pop) * 1000

<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuaW50ZXJwcyA8LSBtZWx0KGludGVycHMpXG5gYGAifQ== -->

```r
interps <- melt(interps)
```

<!-- rnb-source-end -->

<!-- rnb-output-begin eyJkYXRhIjoiVXNpbmcgeWVhciBhcyBpZCB2YXJpYWJsZXNcbiJ9 -->

```
Using year as id variables
```



<!-- rnb-output-end -->

<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuaW50ZXJwcyR5ZWFyIDwtIGFzLm51bWVyaWMoaW50ZXJwcyR5ZWFyKVxuc2lnaHRpbmdzLmRiMiA8LSBhcy5kYXRhLmZyYW1lKHNpZ2h0aW5ncy5kYikgJT4lIFxuICAgIGRwbHlyOjpsZWZ0X2pvaW4oaW50ZXJwcywgYnk9YyhcInllYXJcIj1cInllYXJcIiwgXCJzdGF0ZVwiPVwidmFyaWFibGVcIikpICU+JVxuICAgIGRwbHlyOjptdXRhdGUoc2lnaHRpbmdzX3Blcl8xMDBrPSgobnVtX3NpZ2h0aW5ncy92YWx1ZSkgKiAxMDAwMDApKSAlPiUgXG4gICAgZHBseXI6OnNlbGVjdCh5ZWFyLCBzdGF0ZSwgcmVnaW9uLCBzaWdodGluZ3NfcGVyXzEwMGspXG5gYGAifQ== -->

```r
interps$year <- as.numeric(interps$year)
sightings.db2 <- as.data.frame(sightings.db) %>% 
    dplyr::left_join(interps, by=c("year"="year", "state"="variable")) %>%
    dplyr::mutate(sightings_per_100k=((num_sightings/value) * 100000)) %>% 
    dplyr::select(year, state, region, sightings_per_100k)
```

<!-- rnb-source-end -->

<!-- rnb-output-begin eyJkYXRhIjoiQ29sdW1uIGBzdGF0ZWAvYHZhcmlhYmxlYCBqb2luaW5nIGNoYXJhY3RlciB2ZWN0b3IgYW5kIGZhY3RvciwgY29lcmNpbmcgaW50byBjaGFyYWN0ZXIgdmVjdG9yXG4ifQ== -->

```
Column `state`/`variable` joining character vector and factor, coercing into character vector
```



<!-- rnb-output-end -->

<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxud3JpdGVfY3N2KHNpZ2h0aW5ncy5kYjIsIFwiLi9yYXcvc2lnaHRpbmdzX2RiMi5jc3ZcIilcbmBgYCJ9 -->

```r
write_csv(sightings.db2, "./raw/sightings_db2.csv")
```

<!-- rnb-source-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->



<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuIyBzdGF0ZXBvcHMucmF3JE5hbWUgPC0gbWFwdmFsdWVzKHN0YXRlcG9wcy5yYXckTmFtZSwgc3RhdGUubmFtZSwgc3RhdGUuYWJiKVxuIyBzdGF0ZV9wb3BzIDwtIHN0YXRlcG9wcy5yYXcgJT4lXG4jICAgICBmaWx0ZXIoTmFtZSAlaW4lIHN0YXRlLmFiYikgJT4lXG4jICAgICBzZWxlY3Qob25lX29mKGMoXCIxOTcwXCIsIFwiMTk4MFwiLCBcIjE5OTBcIiwgXCIyMDAwXCIsIFwiMjAxMFwiKSkpICU+JVxuIyAgICAgYXBwbHkoMSwgbWVhbilcbmBgYCJ9 -->

```r
# statepops.raw$Name <- mapvalues(statepops.raw$Name, state.name, state.abb)
# state_pops <- statepops.raw %>%
#     filter(Name %in% state.abb) %>%
#     select(one_of(c("1970", "1980", "1990", "2000", "2010"))) %>%
#     apply(1, mean)
```

<!-- rnb-source-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->


# Normalize Movies By Total Movies That Year

<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuI2FsbF9tb3ZpZXMgPC0gYWxsbW92aWVzLnJhd1tucm93KGFsbG1vdmllcy5yYXcpOjEsXVxuYWxsbW92aWVzLnJhdyA8LSBhbGxtb3ZpZXMucmF3ICU+JSBcbiAgZmlsdGVyKHllYXIgPj0gMTk3NCkgJT4lIFxuICBmaWx0ZXIoeWVhciA8PSAyMDE2KVxuYGBgIn0= -->

```r
#all_movies <- allmovies.raw[nrow(allmovies.raw):1,]
allmovies.raw <- allmovies.raw %>% 
  filter(year >= 1974) %>% 
  filter(year <= 2016)
```

<!-- rnb-source-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->


divide number of alien mobies that year divide by total box office movies that came out that year.

The number is small, so interepretability may be an issue here. Careful!  

<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxubW92aWVzLmRiIDwtIG1vdmllcy5yYXcgJT4lIFxuICBmaWx0ZXIoeWVhciA+PSAxOTc0KSAlPiUgXG4gIGZpbHRlcih5ZWFyIDw9IDIwMTYpICU+JSBcbiAgbGVmdF9qb2luKGFsbG1vdmllcy5yYXcsIGJ5PWMoXCJ5ZWFyXCI9XCJ5ZWFyXCIpKSAlPiUgXG4gIG11dGF0ZShhbGllbm1vdmllc19wZXJfeWVhciA9IG51bV9tb3ZpZXMvdG90YWxfbW92aWVzKSAlPiUgXG4gIHNlbGVjdCh5ZWFyLCBhbGllbm1vdmllc19wZXJfeWVhcilcbmBgYCJ9 -->

```r
movies.db <- movies.raw %>% 
  filter(year >= 1974) %>% 
  filter(year <= 2016) %>% 
  left_join(allmovies.raw, by=c("year"="year")) %>% 
  mutate(alienmovies_per_year = num_movies/total_movies) %>% 
  select(year, alienmovies_per_year)
```

<!-- rnb-source-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->




<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuZ2RwLmRiIDwtIGdkcC5yYXcgJT4lIFxuICBjbGVhbl9uYW1lcygpICU+JSBcbiAgZHBseXI6OnJlbmFtZSh5ZWFyID0geWVhcl9hbmRfY2F0ZWdvcnkpICU+JSBcbiAgZmlsdGVyKHllYXIgPj0gMTk3NCkgJT4lIFxuICBzZWxlY3QoeWVhciwgcGVyX2NhcGl0YV9nZHBfY3VycmVudClcbmBgYCJ9 -->

```r
gdp.db <- gdp.raw %>% 
  clean_names() %>% 
  dplyr::rename(year = year_and_category) %>% 
  filter(year >= 1974) %>% 
  select(year, per_capita_gdp_current)
```

<!-- rnb-source-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->



<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuaW50ZXJuZXQucnVyYWxpdHkuZGIgPC0gaW50ZXJuZXQucnVyYWxpdHkucmF3ICU+JSBcbiAgZHBseXI6OnJlbmFtZSh5ZWFyPVllYXIpXG5gYGAifQ== -->

```r
internet.rurality.db <- internet.rurality.raw %>% 
  dplyr::rename(year=Year)
```

<!-- rnb-source-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->



<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxudXNhZmJhc2UuZGIgPC0gdXNhZmJhc2UucmF3ICU+JSBcbiAgI2ZpbHRlcihTdGF0ZSA9PSBcIkZMXCIpICU+JSBcbiAgIyByZW5hbWUoc3RhdGUgPSBTdGF0ZSkgJT4lIFxuICBncm91cF9ieShTdGF0ZSkgJT4lXG4gIGRwbHlyOjpjb3VudCgpICU+JVxuICBtZXJnZShzdGF0ZS5hYmIsIGJ5Lng9XCJTdGF0ZVwiLCBieS55PTEsIGFsbD1UKSAlPiVcbiAgbXV0YXRlKG49cmVwbGFjZShuLCBpcy5uYShuKSwgMCkpICU+JVxuICBmaWx0ZXIoIWlzLm5hKFN0YXRlKSkgJT4lIFxuICBkcGx5cjo6cmVuYW1lKGFmYmFzZV9wZXJfc3RhdGUgPSBuKSAlPiUgXG4gIGRwbHlyOjpyZW5hbWUoc3RhdGUgPSBTdGF0ZSlcbmBgYCJ9 -->

```r
usafbase.db <- usafbase.raw %>% 
  #filter(State == "FL") %>% 
  # rename(state = State) %>% 
  group_by(State) %>%
  dplyr::count() %>%
  merge(state.abb, by.x="State", by.y=1, all=T) %>%
  mutate(n=replace(n, is.na(n), 0)) %>%
  filter(!is.na(State)) %>% 
  dplyr::rename(afbase_per_state = n) %>% 
  dplyr::rename(state = State)
```

<!-- rnb-source-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->



## Join files together

<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuYWxsLnN0YXRlcy5ub3JtYWxpemVkLmRmIDwtIHNpZ2h0aW5ncy5kYjIgJT4lIFxuICAgIGxlZnRfam9pbihiZWVyLmRiLCBieT1jKFwieWVhclwiID0gXCJ5ZWFyXCIsIFwic3RhdGVcIj0gXCJzdGF0ZVwiKSkgJT4lIFxuICAgIGxlZnRfam9pbihtb3ZpZXMuZGIsIGJ5ID0gYyhcInllYXJcIiA9IFwieWVhclwiKSkgJT4lIFxuICAgIGxlZnRfam9pbihnZHAuZGIsIGJ5ID0gYyhcInllYXJcIiA9IFwieWVhclwiKSkgJT4lXG4gICAgbGVmdF9qb2luKGludGVybmV0LnJ1cmFsaXR5LmRiLCBieT1jKFwieWVhclwiID0gXCJ5ZWFyXCIpKSAlPiUgXG4gICAgbGVmdF9qb2luKHVzYWZiYXNlLmRiLCBieT1jKFwic3RhdGVcIiA9IFwic3RhdGVcIikpICU+JVxuICAgIGxlZnRfam9pbihpbnRlcnBzLCBieT1jKFwieWVhclwiPVwieWVhclwiLCBcInN0YXRlXCI9XCJ2YXJpYWJsZVwiKSkgJT4lXG4gICAgZHBseXI6OnJlbmFtZShwb3B1bGF0aW9uPXZhbHVlKSAlPiVcbiAgICBtdXRhdGUobm9ybWFsaXplZF9hZmJfY291bnQ9YWZiYXNlX3Blcl9zdGF0ZS9wb3B1bGF0aW9uKjEwMDAwMDApICU+JVxuICAgIHNlbGVjdChvbmVfb2YoXCJzdGF0ZVwiLCBcInllYXJcIiwgXCJyZWdpb25cIiwgXCJzaWdodGluZ3NfcGVyXzEwMGtcIiwgXCJhbGllbm1vdmllc19wZXJfeWVhclwiLCBcInBlcl9jYXBpdGFfZ2RwX2N1cnJlbnRcIiwgXCJVcmJhblwiLCBcIlN1YnVyYmFuXCIsIFwiUnVyYWxcIiwgXCJub3JtYWxpemVkX2FmYl9jb3VudFwiKSlcbmBgYCJ9 -->

```r
all.states.normalized.df <- sightings.db2 %>% 
    left_join(beer.db, by=c("year" = "year", "state"= "state")) %>% 
    left_join(movies.db, by = c("year" = "year")) %>% 
    left_join(gdp.db, by = c("year" = "year")) %>%
    left_join(internet.rurality.db, by=c("year" = "year")) %>% 
    left_join(usafbase.db, by=c("state" = "state")) %>%
    left_join(interps, by=c("year"="year", "state"="variable")) %>%
    dplyr::rename(population=value) %>%
    mutate(normalized_afb_count=afbase_per_state/population*1000000) %>%
    select(one_of("state", "year", "region", "sightings_per_100k", "alienmovies_per_year", "per_capita_gdp_current", "Urban", "Suburban", "Rural", "normalized_afb_count"))
```

<!-- rnb-source-end -->

<!-- rnb-output-begin eyJkYXRhIjoiQ29sdW1uIGBzdGF0ZWAgam9pbmluZyBjaGFyYWN0ZXIgdmVjdG9yIGFuZCBmYWN0b3IsIGNvZXJjaW5nIGludG8gY2hhcmFjdGVyIHZlY3RvckNvbHVtbiBgc3RhdGVgL2B2YXJpYWJsZWAgam9pbmluZyBjaGFyYWN0ZXIgdmVjdG9yIGFuZCBmYWN0b3IsIGNvZXJjaW5nIGludG8gY2hhcmFjdGVyIHZlY3RvclxuIn0= -->

```
Column `state` joining character vector and factor, coercing into character vectorColumn `state`/`variable` joining character vector and factor, coercing into character vector
```



<!-- rnb-output-end -->

<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuYWxsLnN0YXRlcy5ub3JtYWxpemVkLmRmW2lzLm5hKGFsbC5zdGF0ZXMubm9ybWFsaXplZC5kZildID0gMFxuYGBgIn0= -->

```r
all.states.normalized.df[is.na(all.states.normalized.df)] = 0
```

<!-- rnb-source-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->




<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuYWxsLnN0YXRlcy5ub3JtYWxpemVkLmRmIDwtIGFsbC5zdGF0ZXMubm9ybWFsaXplZC5kZiAlPiVcbiAgICBmaWx0ZXIoeWVhciA+PSAxOTg1ICYgeWVhciA8PSAyMDE0KVxuYGBgIn0= -->

```r
all.states.normalized.df <- all.states.normalized.df %>%
    filter(year >= 1985 & year <= 2014)
```

<!-- rnb-source-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->



Step 4: Write out

<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxud3JpdGVfY3N2KGFsbC5zdGF0ZXMubm9ybWFsaXplZC5kZiwgXCJyYXcvYWxsX3N0YXRlc19ub3JtYWxpemVkLmNzdlwiKVxuYGBgIn0= -->

```r
write_csv(all.states.normalized.df, "raw/all_states_normalized.csv")
```

<!-- rnb-source-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->





<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxud3JpdGVfY3N2KHN0YXRlcG9wcy5kYjMsIFwicmF3L3N0YXRlcG9wcy5kYjMuY3N2XCIpXG5gYGAifQ== -->

```r
write_csv(statepops.db3, "raw/statepops.db3.csv")
```

<!-- rnb-source-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->



<!-- rnb-text-end -->

