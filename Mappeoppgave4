#Oppgave 4 
rm(list=ls())
library(rvest)
library(tidyverse)
library(ggrepel)
library(dplyr)
library(scales)
library(rlist)
library(ggplot2)
library(janitor)
library(purrr)
#------------------------------------------------------------------------------
sok_1005 <- read_html("https://timeplan.uit.no/emne_timeplan.php?sem=22v&module%5B%5D=SOK-1005-1&week=1-20&View=list")
sok_1006 <- read_html("https://timeplan.uit.no/emne_timeplan.php?sem=22v&module%5B%5D=SOK-1006-1&week=1-20&View=list")
sok_1016 <- read_html("https://timeplan.uit.no/emne_timeplan.php?sem=22v&module%5B%5D=SOK-1016-1&week=1-20&View=list")
#Legges sammen i en------------------------------------------------------------
emner <- list(sok_1005,sok_1006,sok_1016)
#------------------------------------------------------------------------------
scrape <- function(emner) {
  A1 <- html_nodes(emner, "table") %>%
    html_table(., fill=TRUE) %>%  
    list.stack(.)  
  colnames(A1) <- A1[1,] 
  liste <- A1 %>% filter(!Dato=="Dato") %>%
#Skildrer imellom dag/dato og sette d for dag, m for mnd og y for år-----------
#bruker rekkfølge for å sette ønsket/ eget oppsett av diverse overskrifter-----
    separate(Dato, into = c("Dag", "Dato"), sep = "(?<=[A-Za-z])(?=[0-9])") 
  liste$Dato <- as.Date(liste$Dato, format="%d.%m.%Y") 
  liste$Uke <- strftime(liste$Dato, format = "%V")
  rekkefølge <- c("Dato", "Dag" , "Uke"  , "Emnekode" , "Tid" , "Rom", "Lærer")
  liste <- liste[, rekkefølge]
  return(liste)
}
plan <- map(emner, scrape) %>% bind_rows()
plan
#------------------------------------------------------------------------------
