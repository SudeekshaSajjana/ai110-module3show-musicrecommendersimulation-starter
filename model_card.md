# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

MusicMatcher 1000
---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

It recommends songs based on genre, mood, and energy based on what is put in the user profile. This coule eventually be used for real users but right now, there could be more improvements made so that the song recommendations are more accurate, so for now it is for classroom exploration.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

The recommender looks at three things about each song: its genre, its mood, and its energy level. It compares those to what the user says they like, such as their favorite genre, favorite mood, and a target energy level, and hands out points for each match: a bigger bonus if the genre matches, a smaller bonus if the mood matches, and a partial bonus based on how close the song's energy is to the energy the user asked for. All those points get added up into one score per song, and the songs with the highest scores get recommended.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

In the catalog, there are 18 songs with various genres such as pop, lofi, rock, folk, metal, r&b, hiphop, slow stereo, etc. Some of the moods that are represented are nostalgic, melancholic, romantic, euphoric, happy, chill, intense, relaxed, moody, playful, wistful, etc. A couple parts that were missing is the multiple genre tags per song, the era the song is from, and language.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system does best when someone gives a clear, matching set of preferences, like "pop, happy, high energy" or "lofi, chill, low energy." In those cases the top song really does fit all three things they asked for. It also gets the small stuff right: when I asked for a mellow energy level, it picked mellow songs, and when I asked for an intense energy level, it picked intense songs, so the energy matching behaves the way you'd expect. And when a song matches on more than one thing, it always scores higher than a song that only matches one thing, which is exactly how it should work. So overall, for a straightforward listener whose genre, mood, and energy preferences naturally go together, the recommendations feel right.


---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

Most genres in the song library only have one song in them. So if a user says their favorite genre is "folk," the system doesn't really have a choice to make: it's always going to hand them that same one folk song, no matter what mood or energy level they asked for. For most genres the recommender isn't personalizing anything, it's just looking up the only song that is available, which means it can never learn or reflect that a user might like the genre but not that specific track.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I ran five made-up listener profiles through the recommender and compared their top results side by side to see whether the differences in output actually made sense given the differences in what each listener asked for.

**Profiles tested:**

| Profile | What they asked for | Top recommendation |
|---|---|---|
| A. High-Energy Pop Fan | pop, happy, energy 0.9 | Sunrise City |
| B. Chill/Acoustic Fan | lofi, chill, energy 0.3 | Library Rain |
| C. Aggressive Metal Fan | metal, aggressive, energy 0.95 | Iron Fist |
| D. Vague/No-Preference Listener | nothing specified | Sunrise City |
| E. Niche Genre Fan | folk, happy, energy 0.9 | Golden Hour Bloom |

**Comparisons between profiles:**

- **A vs. B:** The high-energy pop fan gets bright, upbeat songs, while the chill/acoustic fan's list shifts almost entirely to mellow, low-energy lofi tracks. This makes sense — these two listeners disagree on genre, mood, and energy, so it would be a red flag if their lists looked similar.
- **A vs. C:** Both A and C asked for high energy (0.9 and 0.95), but they get completely different top songs (Sunrise City vs. Iron Fist) because they asked for different genres and moods. This confirms that energy alone doesn't drive the recommendation — genre and mood still matter, which is the intended behavior.
- **B vs. C:** These two are near-opposite on energy (0.3 vs. 0.95) and get near-opposite results (soft lofi vs. hard metal). This is the clearest, most "obviously correct" pair in the test — it's reassuring that the two most different listeners in the group got the two most different playlists.
- **C vs. E:** Both profiles asked for a mood/energy combo that doesn't exist in their chosen genre (a "happy, high-energy folk song" isn't really in the catalog), so the recommender falls back to whatever partially matches. This exposes a weakness rather than a strength: instead of saying "we don't have that," the system just quietly hands back its best partial guess and presents it with the same confidence as a real match.
- **A vs. D:** This was the most surprising pair. The vague listener, who specified *no* preferences at all, got the exact same top song as the specific high-energy pop fan (Sunrise City) — but for a completely different, non-reason: every song scored 0.00, so the "winner" was just whichever song happened to be listed first in the CSV file. It looks like a recommendation, but it's really just a coincidence of file ordering.

**What surprised me most:** I expected the vague/no-preference listener to either get a random-looking mix or an error, not to land on the same top pick as a clearly-defined pop fan. It revealed that the system has no real notion of "I don't have enough information to recommend anything" — when every song ties at a score of 0, it still confidently returns a ranked top 3, and that ranking is silently determined by row order in the spreadsheet rather than anything about music. The second-biggest surprise was profile E: asking for a genre that barely fits the requested mood/energy doesn't produce a warning or a lower-confidence result, it just returns the least-bad option dressed up the same as every other recommendation.


---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

Next, I'd want to add more song features that actually affect taste, like valence, vocals vs. instrumental, tempo, and maybe even basic lyric themes, so two songs with the same genre and mood label but a very different feel wouldn't get treated as equally good matches. I'd also want the explanations to be more honest about confidence — right now it always sounds sure of itself, even when it's really just picking the least-bad option, so it should be able to say something like "this is a weak match" when nothing in the catalog fits well. To fix the "one song per genre" problem, I'd add more songs per genre and maybe mix in a little randomness or a rule that avoids recommending the same artist over and over, so the results feel less repetitive. Finally, I'd want the system to handle people whose taste isn't one clean genre/mood/energy combo — like someone who likes multiple genres, or wants "happy but calm," by letting preferences be more flexible instead of forcing an exact match.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Working on this project taught me that a recommendation isn't some deep understanding of taste, but it's really just a point system, and the recommendation is only as good as the rules someone decided to give it points for. The most interesting thing I discovered was how easily the system could be tricked or broken: giving it a genre with only one song in the catalog always returned that same song no matter what else I asked for, and giving it no preferences at all didn't make it say "I don't know" — it just quietly defaulted to whatever song happened to be listed first in the spreadsheet. Weird inputs like a negative or sky-high energy value, or leaving a field blank, could also throw the scoring off in ways I wouldn't have expected before testing it. This changed how I think about real apps like Spotify or YouTube — they feel like they "get" your taste, but under the hood they're probably running on rules and data limitations too, and a confident-looking recommendation doesn't always mean the system actually found a good match.

