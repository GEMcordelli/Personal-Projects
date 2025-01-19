From our EDA: Want to zero in on differences in song subject based on factors like gender of the artist, and how high the artist ranked over theri net carerr on the BB Top 100. 

  Anthroplogical/Social Psychological Lens: what kind of trends do we see in the types of songs that get popular? What does this say about the artist? What does this say about the audience? Why might certain gender substitutes be popular (baby,
you, thing, etc.) and why?

  Applied: how can we use these patterns to guide and predict future song creation and gage levels of popularity, and therefore be able to predict and leverage potential profits for artists, producers, concert venues,
etc.


Palomba Script: I've selected one of the song data points for further explortion by loading it in and parsing the text. I want to compare across similar genres and time periods,
with differing artist genders and see the stylistic change and similarities, and how these relate to song popularity
  * my script template is placed below my active script in the PalombaScript ipynb folder, and is derived from a script given to me by Professor Anthony Palomba form the Darden 
Business school, whom I am consulting for adivce and guidance on my project



12/12 - Palomba Script Update: For this specific song, Only Girl in the World, I want more stringent guidliens for how many times a line has to be repreated to be considered
part of a course. I hypothesize that this points to pop songs having more repetitive sequences outside of a chorus



*** NEWEST OBJECTIVE***
12/27 - Another Update: based on my most recent convo with Anthony, here is our current objective and future plans...

" my plan is to copy the same process I used for Only Girl In The World for every song that corresponded to the EDA I performed previously. Line 81 in the jupyter notebook I 
attached outputs a dataframe that includes some metadata about songs that reached #1 on the Billboard Top 100. The "genderdummy", "songsubject" and "gender" columns were added 
by me, and the remaining columns were already a part of the dataset. My thought was to use insights gained from the Lyrics_Analysis files (more specified song subject, other 
themes that may pop up such as repetition, emotion, etc) and add these as new columns in the EDA dataframe. Then, I could use some feature engineering to predict what features 
correlate most strongly to chart success. Further down the line, I thought I could juxtapose this with the same process on the songs that pool around the bottom of the
Billboard Top 100. "


**UPDATE: finished loading csvs for the first 20 songs in the top 100! My next step is to do a bit of EDA on the csvs
    - csvs-as-individuals: I want to do indivudal analysis on each songs lyrics so they can be reincorporated into the original dataframe, so I can incorporate the other metadata when creating algorithms
    - csvs-as-conglomerate: I also want to make one big franken-frame of every single csv, regardless of the speicifc song, so we can make some higher level observations abotu general patterns across lyrics (for example, we can use Fourier transformations to track word frequency; we could separate this by "pivot-wider"-ing the Section column of the csvs. Every csv has the same dataframe structure, so this shouldnt be too hard!)


** UPDATE: Now that we have all of our songs uploaded, I'm going to want to concat all of our csvs into one large dataframe and parse out the frame token by token to check for general trends. Then I will want to work on the individual song level in ordet to decipher differences in song sentiment, structure, topic modeling, etc. for comparison across different songs, all correlated to record success and demographic information.
