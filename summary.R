library("dplyr")
library("ggplot2")
setwd("C:/Users/mrche/info201/exploratory-analysis-anguyenuw")

players <- read.csv("csvfiles/user_data/users_with_RME.csv") %>%
  filter(Games > 30)

summary_top_5_RME <- players %>%
  arrange(RMERanking) %>%
  slice_min(RMERanking, n = 5) %>%
  select(RMERanking, Username, RME, GlobalRank)

summary_top_5_Osu <- players %>%
  arrange(GlobalRank) %>%
  slice_min(GlobalRank, n = 5) %>%
  select(GlobalRank, Username, RMERanking, RME)

my_info <- players %>%
  filter(Username == "RMEfan")

mean_RME_per_digit <- numeric(6)
mean_Games_per_digit <- numeric(6)
for (digit in 1:6) {
  mean_RME_per_digit[digit] <- players %>%
    filter((GlobalRank < 10 ^ digit) & (GlobalRank >= 10 ^ (digit - 1))) %>%
    summarize(mean=mean(RME))
  mean_Games_per_digit[digit] <- players %>%
    filter((GlobalRank < 10 ^ digit) & (GlobalRank >= 10 ^ (digit - 1))) %>%
    summarize(mean=mean(Games))
}
mean_RME_per_digit <- mean_RME_per_digit %>% unlist(use.names = FALSE)
mean_Games_per_digit <- mean_Games_per_digit %>% unlist(use.names = FALSE)

median_RME <- players %>%
  select(RME) %>%
  unlist(use.names=FALSE) %>%
  median()

mean_RME <- players %>%
  select(RME) %>%
  unlist(use.names=FALSE) %>%
  mean()