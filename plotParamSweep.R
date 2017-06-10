
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

if (length(unique(r$combatant)) == 1) {
    title <- paste0(r$combatant,"'s ",r$param, " ", text)
    x.label <- paste(r$param, text)
} else {
    title <- paste0("Number of ", 
        strsplit(as.character(r$combatant[1]),split=" ")[[1]][2], "s")
    x.label <- title
}

p <- ggplot(r, aes(x=value, y=party_win_freq)) + geom_point() + geom_smooth() +
    ggtitle(title) +
    xlab(x.label) +
    ylab("Party win %")  +
    ylim(c(0,1))

p <- p + geom_hline(yintercept=.5, color="red")

ggsave("plot.pdf",p)
