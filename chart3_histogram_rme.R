library("dplyr")
library("ggplot2")
setwd("C:/Users/mrche/info201/exploratory-analysis-anguyenuw")

players <- read.csv("csvfiles/user_data/users_with_RME.csv") %>%
  filter(Games > 30)

RME_histogram <- ggplot(players, aes(x = RME)) + geom_histogram(binwidth = 50, colour = "black", fill = "lightblue") 
RME_histogram <- RME_histogram + labs(title="", 
                  subtitle="Players with at least 30 tournament scores from Jan 1 2023 to Aug 13 2023", 
                  y="Number of players", 
                  x="RME Rating")
RME_histogram

wompers <- scores_raw %>% filter(Score < 1300000)
wompers$Match.ID <- as.numeric(wompers$Match.ID)
womp <- ggplot(wompers, aes(x = Match.ID)) + 
  geom_histogram(binwidth = 10000, colour = "black", fill = "lightblue") +
  coord_cartesian(xlim = c(106000000,110000000), ylim = c(0, 9000))
womp

unique_users <- wompers
unique_users <- unique_users %>% group_by(User.ID) %>% slice_head(n=1)
womp <- ggplot(unique_users, aes(x = User.ID)) + 
  geom_histogram(binwidth = 100000, colour = "black", fill = "lightblue") +
  coord_cartesian(xlim = c(0,33000000), ylim = c(0, 150))
womp