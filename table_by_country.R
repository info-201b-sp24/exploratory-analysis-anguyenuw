library("dplyr")
library("ggplot2")
setwd("C:/Users/mrche/info201/exploratory-analysis-anguyenuw")

players <- read.csv("csvfiles/user_data/users_with_RME.csv") %>%
  filter(Games > 30) %>%
  group_by(Location)

table_best_players <- players %>%
  slice_max(order_by=RME) %>% 
  select(Location, Username, RMERanking, RME, GlobalRank)

players <- players %>%
  left_join(table_best_players, join_by(Location))

table_display2 <- players %>%
  summarise("Players"=n(),
            "Average RME (2023)" = round(mean(RME.x), digits=1),
            "Best Player (2023)" = first(Username.y),
            "Best Player's RME Ranking (2023)" = first(RMERanking.y)) %>%
  arrange(desc(Players)) %>%
  slice_head(n=20)