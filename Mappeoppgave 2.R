

##MAPPEOPPGAVE 2
#JSON DATA
#COVID DEATHS SINCE ADULT VACCSINE

library(tidyverse)
library(dplyr)
library(ggplot2)
library(jsonlite)
library(ggrepel)
library(scales)


##OPPGAVE1--------------------------------------------------------------------
#DOWNLOADING FILE
D1 <- fromJSON("https://static01.nyt.com/newsgraphics/2021/12/20/us-coronavirus-deaths-2021/ff0adde21623e111d8ce103fedecf7ffc7906264/scatter.json")

#HIGHLIGTING STATES IN 2 LETTERS
D1$name <- state.abb[match(D1$name, state.name)]
D1[is.na(D1)] <- "DC"
#MAKING THE PLOT
D1 %>%
  ggplot(aes(fully_vaccinated_pct_of_pop, deaths_per_100k)) +
  geom_point(size = 5, pch = 20, col="blue", alpha = 0.25) +
  geom_text_repel(aes(label = name)) +
  
  scale_x_continuous(labels = scales::percent, limits=c(0.45, 0.80), breaks=seq(0.45, 0.80, by = 0.05)) +
  labs(title="Covid-19 deaths since universal adult vaccine eligibility compared with vaccination rates",
       x ="Share of total population fully vaccinated",
       y = "Monthly deaths per100,000") +
  theme_bw()


#SHOWS RESULTS-----------------------------------------------------------------

##OPPGAVE2---------------------------------------------------------------------
#MAKING THE NEW PLOT WITH LINE 
lm(deaths_per_100k ~ fully_vaccinated_pct_of_pop, D1)
D1 %>%
  ggplot(aes(fully_vaccinated_pct_of_pop, deaths_per_100k)) +
  geom_point(size = 5, pch = 20, col="blue", alpha = 0.25) +
  geom_smooth(method = lm, alpha = 0, col = "red") +
  geom_text_repel(aes(label = name)) +
  
  scale_x_continuous(labels = scales::percent, limits=c(0.45, 0.80), breaks=seq(0.45, 0.80, by = 0.05)) +
  labs(title="Covid-19 deaths since universal adult vaccine eligibility compared with vaccination rates",
       x ="Share of total population fully vaccinated",
       y = "Monthly deaths per100,000") +
  theme_bw()
#SHOWS RESULTS-----------------------------------------------------------------


