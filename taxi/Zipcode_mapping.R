install.packages("as", dependencies=TRUE)

library(sp)
library(maptools)
library(zipcode)
zipcode = zipcode::

# grab the zip code boundaries
url <- "http://www2.census.gov/geo/tiger/GENZ2014/shp/cb_2014_us_zcta510_500k.zip"
fil <- "ztca.zip"

# don't waste bandwidth
if (!file.exists(fil)) { download.file(url, fil) }
unzip(fil, exdir="ztca")

# read them in (this takes a bit)
ztca <- readShapePoly("ztca/cb_2014_us_zcta510_500k.shp", verbose=TRUE)

# extract NY
ny <- ztca[as.character(ztca$ZCTA5CE10) %in% as.character(zipcode[zipcode$state=="NY",]$zip),]

# your points
latlongdata <- 
  structure(list(dropoff_longitude = c(-73.981705, -73.993553, 
                                       -73.973305, -73.988823, -73.938484, -74.015503, -73.95472, -73.9571, 
                                       -73.971298, -73.99794), dropoff_latitude = c(40.760559, 40.756348, 
                                                                                    40.762646, 40.777504, 40.684692, 40.709881, 40.783371, 40.776657, 
                                                                                    40.752148, 40.720535)), row.names = c(8807218L, 9760613L, 3175671L, 
                                                                                                                          10878727L, 2025038L, 5345659L, 14474481L, 1650223L, 684883L, 
                                                                                                                          9129975L), class = "data.frame", .Names = c("dropoff_longitude", 
                                                                                                                                                                      "dropoff_latitude"))
coordnts <- read.csv(file="/Users/Michael/Downloads/Github/capstone/coordinates.csv", header=TRUE, sep=",")

data <- coordnts[c(1,3,2,5,4)]


# make them all super spatial-like (must be in lon,lat format)
pts <- SpatialPoints(as.matrix(data[,2:3]))



# figure out where they are (this can take a bit)
dat <- pts %over% ny

# merge your data back in (there are many ways to do this)
dat$lon <- latlongdata$dropoff_longitude
dat$lat <- latlongdata$dropoff_latitude
rownames(dat) <- rownames(latlongdata)

head(dat,20)
nrow(dat)
write.csv(dat$GEOID10, file = "/Users/Michael/Downloads/Github/capstone/zipcode.csv", row.names=FALSE, col.names=TRUE, sep=",")

# make them all super spatial-like (must be in lon,lat format)
pts2 <- SpatialPoints(as.matrix(data[,4:5]))


# figure out where they are (this can take a bit)
dat2 <- pts2 %over% ny

# merge your data back in (there are many ways to do this)
dat2$lon <- latlongdata$pickup_longitude
dat2$lat <- latlongdata$pickup_latitude

head(dat2,20)
nrow(dat2)
write.csv(dat2$GEOID10, file = "/Users/Michael/Downloads/Github/capstone/zipcode2.csv", row.names=FALSE, col.names=TRUE, sep=",")