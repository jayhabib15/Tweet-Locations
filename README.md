# Tweet-Locations

Who do you love?

There are a lot of existing maps that show the biggest team fan bases in each state, mapped by things like jersey sales or Facebook likes. Now you can try and figure out where all the fans of your favorite player are tweeting from.

We will use Twython Streaming API.

Generally: We will collect data from twitter by geographic location using the Twython equivalent of Twitter API (POST STATUS/filter). We will specify filter keys and grab data from all over the US from the previous day.

We will store the raw tweets' locations as strings of coordinates in a file, "coords."

Save the location to a text file for later use.
Format the location data so that it can be plotted on a map of the US that we generate using code from Purple America.
Make the maps of locations of tweets.
Make a gif using the images.
Data Plan

Summarize data sources, data formats, and how to obtain or generate the data you will be using We used Twython streamer (ouath2 required) to get the data and saved it to a file, "coords," which is a text file of strings. Map data is stored in csv files, and is parsed through with the appropriate csv reader. Photos are outputted as pngs.

Implementation Plan

Overview of you plan. Are you starting from existing code? What skills from the course will be be using to complete your project? etc. We use data from Purple America as well as similar methods to draw the map. We use all sorts of skills we acquired from the course, including (but not limited to) list comprehensions, parsing csv data, creating classes, writing functions, drawing and visualizing information, and using new, outside libraries.

External Libraries

requests
twython
matplotlib.pyplot
PIL
Milestones

First, we collect location data on tweets about some query. We then created images that show where in the US people tweeted about that query. Afterwards, we made a gif image to visualize the tweets appearing in the order in which we received them.

Instructions to run the code

To acquire tweet data: Run the gettweets.py program as follows in the terminal: python3 gettweets.py QUERY where QUERY is the keyword (i.e player name, but in theory you could search for ANYTHING) in the tweets you are searching through. This will add tweet data to the file "coords." Quit the program when you feel you have acquired enough tweets. It should be noted that gettweets.py never erases tweet data from older queries; in other words, empty the file every time you want to use fresh data.

To generate the maps with the coordinates "coords" acquired from gettweets.py: python3 map_generator.py election-data/results/US2012.csv election-data/boundaries/US-states.csv output.png 4000 SOLID coords An explanation of what each input is has been included in the program file. #NOTE: In line 51 of map_generator.py, there is an "if" parameter that will allow you to determine the numbers of tweets you want mapped. If it is set to 1, you will get every single picture. This could easily reach the hundreds. Adjust accordingly.

To generate the GIF image, run the following code in the terminal: convert -delay 10 -loop 0 = *.png final.gif

One limitation of this program is that it is limited by Twitter users who have their location made public; there are definitely many, many tweets you aren't grabbing because the users have their location set to private. Still, we thought this would be a fun way to track fan interest across the US.
