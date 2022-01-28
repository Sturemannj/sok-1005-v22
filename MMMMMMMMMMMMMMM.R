library(data.table)
library(tidyverse)
library(ggplot2)
library(dplyr)
library(cowplot)
library(corrr)
library(httr)
library(zoo)
library(scales)


global_temps <- fread("http://vortex.nsstc.uah.edu/data/msu/v6.0/tlt/uahncdc_lt_6.0.txt", header = TRUE) 

## Oppgave1

global_temps1 <-
  global_temps %>% 
  select(Year, Globe, Mo) %>% 
  rename(Temperature = Globe) %>%
  group_by(Year) 

chars <- 
  global_temps1 %>% 
  c("Temperature", 1948:2021)  

temp <- as.numeric(chars$Temperature)

year <- as.numeric(global_temps1$Year)

month <- as.numeric(global_temps1$Mo)

data <- data.frame(temp, year, month,             
                   global_temps1)

data1 <- subset(data, select = -c(Temperature, Year, Mo)) %>% 
  rename(Temperature = temp, Year = year, Month = month)

EN <- 
  data1 %>% 
  mutate(Gjentemp=rollmean(Temperature, k= 13, fill = NA, align = "right"),
         dag = as.yearmon(paste(data1$Year, data1$Month), "%Y %m"))

ggplot(EN, aes(x= dag, y= Temperature)) + 
  geom_line(y = as.numeric(EN$Gjentemp), color="red",
            size = 1) +
  geom_point (color = "blue2", size= 0.5) +
  geom_line( color= "orange", size= 0.3) +
  geom_hline(yintercept=0, color = "dark grey") +
  scale_linetype_manual(values=c("twodash", "dotted")) +
  labs(title = "Global Average Tropospheric Temperatures", 
       x = " ", 
       y= "T Departure from 91-20 Avg. (deg.C) ") +
  theme_bw() +
  scale_x_continuous(breaks = scales::pretty_breaks(n = 40)) +
  theme(axis.text.x=element_text(angle=90, hjust=0.5)) +
  scale_y_continuous(breaks = scales::pretty_breaks(n = 20))

##oppgave 2 

GP <- fread("http://vortex.nsstc.uah.edu/data/msu/v6.0/tlt/uahncdc_lt_6.0.txt")
MT <- fread("http://vortex.nsstc.uah.edu/data/msu/v6.0/tmt/uahncdc_mt_6.0.txt")
TR <- fread("http://vortex.nsstc.uah.edu/data/msu/v6.0/ttp/uahncdc_tp_6.0.txt")  
LS <- fread("http://vortex.nsstc.uah.edu/data/msu/v6.0/tls/uahncdc_ls_6.0.txt")

Lower_tro <- 
  GP %>% 
  select(Year, Mo, NoPol) %>% 
  mutate(Where = "Lower_tro")

Mid_tro <- 
  MT %>% 
  select(Year, Mo, NoPol) %>% 
  mutate(Where = "Mid_tro")

Trop <-
  TR %>% 
  select(Year, Mo, NoPol) %>% 
  mutate(Where = "Trop")

Lower_strat <-
  LS %>% 
  select(Year, Mo, NoPol) %>% 
  mutate(Where = "Lower_strat")


Lower_strat$Year <- as.character(Lower_strat$Year)

Lower_strat$Mo <- as.character(Lower_strat$Mo)

Lower_strat$NoPol <- as.character(Lower_strat$NoPol)

Lower_strat$Where <- as.character(Lower_strat$Where)

H <- merge(Lower_tro, Mid_tro, all = TRUE)
G <- merge(Trop, Lower_strat, all = TRUE)

