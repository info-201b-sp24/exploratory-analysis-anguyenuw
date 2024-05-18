library("dplyr")
library("ggplot2")
setwd("C:/Users/mrche/info201/exploratory-analysis-anguyenuw")

table_players <- read.csv("csvfiles/user_data/users_with_RME.csv")
table_players <- table_players %>%
  filter(Games > 50) %>%
  group_by(Location)

table_best_players <- table_players %>%
  slice_max(order_by=RME) %>% 
  select(Location, Username, RMERanking, RME, GlobalRank)

table_players <- table_players %>%
  left_join(table_best_players, join_by(Location))

table_display <- table_players %>%
  summarise("Players"=n(),
            "Average RME" = mean(RME.x),
            "Average PP" = mean(PP),
            "Best Player" = first(Username.y),
            "Best Player's RME Ranking" = first(RMERanking.y)) %>%
  arrange(desc(Players)) %>%
  slice_head(n=10)