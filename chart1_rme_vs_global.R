library("dplyr")
library("ggplot2")
library("scales")
setwd("C:/Users/mrche/info201/exploratory-analysis-anguyenuw")

players <- read.csv("csvfiles/user_data/users_with_RME.csv") %>%
  filter(Games > 30)

scatter <- ggplot(players, aes(x = GlobalRank, y = RME)) + 
  geom_point(size = 0.7)
scatter <- scatter + coord_cartesian(xlim = c(1,50000), ylim = c(500, 3300)) +
  scale_x_continuous(labels = scales::comma)
scatter <- scatter + labs(title="", 
                          subtitle="Players above rank 50,000 with at least 30 tournament scores from Jan 1 2023 to Aug 13 2023", 
                          y="RME Rating", 
                          x="Global Rank (as of May 17 2024)") 


scatter

scatter_log <- ggplot(players, aes(x = GlobalRank, y = RME)) + 
  geom_point(size = 0.7)
scatter_log <- scatter_log + coord_cartesian(xlim = c(1,1000000), ylim = c(500, 3300)) + 
  scale_x_continuous(trans='log10', labels = scales::comma)
scatter_log <- scatter_log + labs(title="", 
                          subtitle="Players with at least 30 tournament scores from Jan 1 2023 to Aug 13 2023", 
                          y="RME Rating", 
                          x="Global Rank (as of May 17 2024), log plot") 


scatter_log


scatterP <- ggplot(players, aes(x = RMERanking, y = PP)) + geom_point(size = 0.7) 
scatterP <- scatterP + coord_cartesian(xlim = c(0,10000), ylim = c(0, 29000))
scatterP <- scatterP + labs(title="Global Ranking VS RME Rating", 
                          subtitle="Players with at least 50 tournament scores from Jan 1 2023 to Aug 13 2023", 
                          y="PP", 
                          x="RMERanking")


