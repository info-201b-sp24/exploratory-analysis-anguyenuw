library("dplyr")
library("ggplot2")
setwd("C:/Users/mrche/info201/exploratory-analysis-anguyenuw")

c1_players <- read.csv("csvfiles/user_data/users_with_RME.csv")
c1_players <- c1_players %>%
  filter(Games > 50)

scatter <- ggplot(c1_players, aes(x = GlobalRank, y = RME)) + geom_point() 
scatter <- scatter + coord_cartesian(xlim = c(0,1000), ylim = c(1500, 3300))
scatter <- scatter + labs(title="Global Ranking VS RME Rating", 
               subtitle="Players with at least 50 tournament scores from Jan 1 2023 to Aug 13 2023", 
               y="RME Rating", 
               x="Global Rank")

scatter

