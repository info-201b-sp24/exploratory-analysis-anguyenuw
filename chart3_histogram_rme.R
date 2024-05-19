library("dplyr")
library("ggplot2")
setwd("C:/Users/mrche/info201/exploratory-analysis-anguyenuw")

players <- read.csv("csvfiles/user_data/users_with_RME.csv") %>%
  filter(Games > 30)

RME_histogram <- ggplot(players, aes(x = RME)) + geom_histogram(binwidth = 50, colour = "black", fill = "lightblue") 
RME_histogram <- RME_histogram + labs(title="Distribution of RME Ratings (up to Aug 13 2023)", 
                  subtitle="Players with at least 30 tournament scores from Jan 1 2023 to Aug 13 2023", 
                  y="Number of players", 
                  x="RME Rating")
RME_histogram