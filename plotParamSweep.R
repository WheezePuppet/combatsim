
require(ggplot2)
require(stringr)

r <- read.csv("results.csv")

if (any(str_detect(r$value,"\\+"))) {
    r$value <- as.numeric(
        substr(r$value,str_locate(pattern="\\+",r$value)+1,length(r$value)))
    text <- "modifier"
} else {
    text <- "value"
}

p <- ggplot(r, aes(x=value, y=party_win_freq)) + geom_point() + geom_smooth() +
    ggtitle(paste0(r$combatant,"'s ",r$param, " ", text))  +
    xlab(paste(r$param, text))  +
    ylab("Party win %")  +
    ylim(c(0,1))

p <- p + geom_hline(yintercept=.5, color="red")

ggsave("plot.pdf",p)
