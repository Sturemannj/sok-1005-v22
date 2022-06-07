library(data.table)
library(tidyverse)
library(ggplot2)
library(dplyr)
library(readr)
library(lubridate)
library(cowplot)
library(corrr)
library(httr)
library(zoo)
library(scales)
library(stringr)
library(hrbrthemes)
library(janitor)
#-----------------------------------------------------------------------------
#Oppgave 1
#plasserer filer der de kan finnes av reader.
#gir dem navn. 
A1 <- read_csv("D:/Eksamen/AppWichStoreAttributes.csv")
A2 <- read_csv("D:/Eksamen/county_crime.csv")
A3 <- read_csv("D:/Eksamen/county_demographic.csv")
A4 <- read_csv("D:/Eksamen/county_employment.csv")
A5 <- read_csv("D:/Eksamen/weekly_sales_10stores.csv")
A6 <- read_csv("D:/Eksamen/weekly_weather.csv")

#renamer de og bruker (merge) til å sette  dem sammen.
#-----------------------------------------------------------------------------
A1 <- rename(A1, Store_num = Store_Num)
#-----------------------------------------------------------------------------
A2 <- rename(A2, county_crime = county_crime)
#-----------------------------------------------------------------------------
J1 <- merge(A5, A1) 
#-----------------------------------------------------------------------------
J2 <- merge(J1, A2) 
#-----------------------------------------------------------------------------
J3 <- merge(J2, A3)
#-----------------------------------------------------------------------------
J4 <- merge(J3, A4) 
#-----------------------------------------------------------------------------
A6 <- rename(A6, Store_Weather_Station = Weather_Station)
#-----------------------------------------------------------------------------
FD1 <- union_all(J4, A6) 
#-----------------------------------------------------------------------------
FD1$Date <- mdy(FD1$Date)
#-----------------------------------------------------------------------------
FD1 <- FD1 %>% filter(!is.na(Description))
#-----------------------------------------------------------------------------

#Oppgave 2 / task 2 
#salgsraport for uke
sum(A5$Profit)
sum(FD1$Profit, na.rm=T)
#-----------------------------------------------------------------------------
#Den totale Profiten til butikk 2 for best salg og mest kriminalitet 
FD1 %>% 
  filter(Store_num==2) %>% 
  group_by(Description) %>%
  summarise(Profit = sum(Profit)) %>%
  arrange(desc(Profit))
#-----------------------------------------------------------------------------
#Katogoriserer type mat som selges og viser det i profit
FD1 %>% filter(Date=="2013-03-24") %>% 
  filter(Store_num==2) %>% 
  group_by(Description) %>%
  summarise(Profit = sum(Profit)) %>%
  arrange(desc(Profit))
#-----------------------------------------------------------------------------
#viser anntal enhenter av forkjellige produkter som er solgt innenfor 1 uke 
head(FD1 %>% filter(Date=="2013-03-24") %>% 
       filter(Store_num==2) %>%
       group_by(Description) %>%
       summarise(Sold = sum(Sold)) %>%
       arrange(desc(Sold)),10)
# De mest solgte produktene
head(FD1 %>% filter(Date=="2013-03-24") %>% 
       group_by(Description) %>%
       summarise(Sold = sum(Sold)) %>%
       arrange(desc(Sold)),12)
#-----------------------------------------------------------------------------
store_2 <- FD1 %>% select(Description,Profit,Date,Store_num) %>% 
  filter(Date=="2013-03-24",Store_num==2)
head(store_2)
#-----------------------------------------------------------------------------
#Higligter forksleige varer er solgt i enheter av 10.
CHIPS <- FD1 %>% filter(grepl('CHIPS', Description)) %>% 
  select(Description,Sold,Date,Day,Store_num) %>%  
  mutate(Description = ifelse(grepl('CHIPS', Description), 'CHIPS')) 
#-----------------------------------------------------------------------------
COOKIE <- FD1 %>% filter(grepl('COOKIE', Description)) %>% 
  select(Description,Sold,Date,Day,Store_num) %>%  
  mutate(Description = ifelse(grepl('COOKIE', Description), 'COOKIE'))
#-----------------------------------------------------------------------------
DRINK <- FD1 %>% filter(grepl('DRINK', Description)) %>% 
  select(Description,Sold,Date,Day,Store_num) %>%  
  mutate(Description = ifelse(grepl('DRINK', Description), 'DRINK'))
#-----------------------------------------------------------------------------
CHICKEN <- FD1 %>% filter(grepl('CHICKEN', Description)) %>% 
  select(Description,Sold,Date,Day,Store_num) %>%  
  mutate(Description = ifelse(grepl('CHICKEN', Description), 'CHICKEN'))
#-----------------------------------------------------------------------------
TURKEY <- FD1 %>% filter(grepl('TURKEY', Description)) %>% 
  select(Description,Sold,Date,Day,Store_num) %>%  
  mutate(Description = ifelse(grepl('TURKEY', Description), 'TURKEY'))
#-----------------------------------------------------------------------------
HAM <- FD1 %>% filter(grepl('HAM', Description)) %>% 
  select(Description,Sold,Date,Day,Store_num) %>%  
  mutate(Description = ifelse(grepl('HAM', Description), 'HAM'))
#-----------------------------------------------------------------------------
CHIP <- FD1 %>% filter(grepl('CHIP', Description)) %>% 
  select(Description,Sold,Date,Day,Store_num) %>%  
  mutate(Description = ifelse(grepl('CHIP', Description), 'CHIP'))
#-----------------------------------------------------------------------------
BOTTLE <- FD1 %>% filter(grepl('BOTTLE', Description)) %>% 
  select(Description,Sold,Date,Day,Store_num) %>%  
  mutate(Description = ifelse(grepl('BOTTLE', Description), 'BOTTLE'))
#-----------------------------------------------------------------------------
BEVERAGE <- FD1 %>% filter(grepl('BEVERAGE', Description)) %>% 
  select(Description,Sold,Date,Day,Store_num) %>%  
  mutate(Description = ifelse(grepl('BEVERAGE', Description), 'BEVERAGE'))
#-----------------------------------------------------------------------------
MUSHROOM <- FD1 %>% filter(grepl('MUSHROOM', Description)) %>% 
  select(Description,Sold,Date,Day,Store_num) %>%  
  mutate(Description = ifelse(grepl('MUSHROOM', Description), 'MUSHROOM'))
#her er det 2 verdier som er (DRINK).
#her er også 2 verdier (COOKIE)
#-----------------------------------------------------------------------------
BP2 <- bind_rows(CHIPS, COOKIE, DRINK, CHICKEN, TURKEY, HAM, CHIP, BOTTLE, BEVERAGE, MUSHROOM)
BP2 <- BP2 %>% filter(Date=="2013-03-24")
BP2 <- setNames(aggregate(BP2$Sold, by=list(MATTYPE=BP2$Description), 
                                  FUN=sum),c("MATTYPE", "Sold"))
#-----------------------------------------------------------------------------
ggplot(BP2, aes(x= MATTYPE, y= Sold, fill=MATTYPE)) + geom_bar(stat="identity") + 
  theme_minimal() + labs(title = "Anntal solgte av mattyper")
#-----------------------------------------------------------------------------
##Oppgave 3 / task 3 
FD1 %>% filter(Year==2013) %>% 
  filter(Month==6) %>%  
  group_by(Description) %>%
  summarise(Sold = sum(Sold)) %>%
  arrange(desc(Sold))
#-----------------------------------------------------------------------------
BP5 <- bind_rows(CHIPS, COOKIE, DRINK, CHICKEN, TURKEY, HAM, CHIP, BOTTLE, BEVERAGE, MUSHROOM)
BP5 <- BP4 %>% filter(Month==6)
BP5 <- setNames(aggregate(BP4$Sold, by=list(MATTYPE=BP4$Description), 
                          FUN=sum),c("MATTYPE", "Sold"))
#-----------------------------------------------------------------------------
BF5 <- bind_rows(CHIPS, COOKIE, DRINK, CHICKEN, TURKEY)
#-----------------------------------------------------------------------------
BF5  <- rename(BF5, Dato = Date)
#-----------------------------------------------------------------------------
BF5  <- rename(BF5, Sold = Sold)
#-----------------------------------------------------------------------------
BF5  <- rename(BF5, MATTYPE = Description)
#-----------------------------------------------------------------------------
ggplot(BF5, aes(x = Dato, y = Sold)) + 
  geom_line(aes(color = MATTYPE), size = 4) +
  scale_color_manual(values = c("dark orange", "dark green", 'dark red', 'dark blue', ' black')) +
  theme_minimal() + labs(title = "Anntal solgte av mattyper for mnd")
#-----------------------------------------------------------------------------







