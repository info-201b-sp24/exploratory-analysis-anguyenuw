library("dplyr")
library("ggplot2")
setwd("C:/Users/mrche/info201/exploratory-analysis-anguyenuw")

players <- read.csv("csvfiles/user_data/users_with_RME.csv") %>%
  filter(Games > 50)

summary_info <- list()
summary_info <- players %>%
  arrange(RMERanking) %>%
  slice_min(RMERanking, n=10) %>%
  select(Username, RMERanking, RME, GlobalRank)

my_info <- players %>%
  filter(Username == "RMEfan")

data_per_digit <- data.frame(matrix(nrow=6, ncol=2))
for (digit in 1:6) {
  avg_RME <- players %>%
    filter((GlobalRank < 10 ^ digit) & (GlobalRank >= 10 ^ (digit - 1))) %>%
    summarize(mean=mean(RME))
}

top_10 <- players %>%
  filter(GlobalRank < 10)
top_10_avg_RME <- (top_10 %>%
  select(RME) %>% 
  summarize(mean=mean(RME)))[1,1]
top_100 <- players %>%
  filter((GlobalRank < 100) & (GlobalRank >= 10))
top_100_avg_RME <- (top_100 %>%
                     select(RME) %>% 
                     summarize(mean=mean(RME)))[1,1]
top_1000 <- players %>%
  filter((GlobalRank < 1000) & (GlobalRank >= 100))
top_1000_avg_RME <- (top_1000 %>%
                     select(RME) %>% 
                     summarize(mean=mean(RME)))[1,1]
top_10000 <- players %>%
  filter((GlobalRank < 10000) & (GlobalRank >= 1000))
top_10000_avg_RME <- (top_10000 %>%
                     select(RME) %>% 
                     summarize(mean=mean(RME)))[1,1]
top_100000 <- players %>%
  filter((GlobalRank < 100000) & (GlobalRank >= 10000))
top_100000_avg_RME <- (top_100000 %>%
                        select(RME) %>% 
                        summarize(mean=mean(RME)))[1,1]