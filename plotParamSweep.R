
require(ggplot2)
require(stringr)

r <- read.csv("results.csv")

r$val <- as.numeric(substr(r$val,str_locate(pattern="\\+",r$val)+1,length(r$val)))
p <- ggplot(r, aes(x=val, y=party_win_freq)) + geom_point() + geom_smooth() +
    ggtitle("How buff is enough?")  +
    xlab("Buff commoner's damage modifier")  +
    ylab("Party win %") 

print(p)
