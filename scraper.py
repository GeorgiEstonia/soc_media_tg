# inspired by https://scrapfly.io/blog/how-to-scrape-instagram/
import json
from typing import Optional
from urllib.parse import quote
from decouple import config
from scrapfly import ScrapeConfig, ScrapflyClient, ScrapeApiResponse
import pprint

class Scraper():

    def __init__(self, instagram_username):
        """
        Class that scarpes user data and post data using scrapfly service.

        Input:
        instagram_username: instagram username
        """
        self.instagram_username = instagram_username

    def scrape_user(self, username: str, session: ScrapflyClient):
        """scrape user's data"""
        result = session.scrape(
            ScrapeConfig(
                url=f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
                headers={"x-ig-app-id": "936619743392459"},
                asp=True,
            )
        )
        data = json.loads(result.content)
        return data["data"]["user"]


    def scrape_user_posts(self, user_id: str, session: ScrapflyClient, page_size=12, page_limit: Optional[int] = None):
        """scrape user's post data"""
        base_url = "https://www.instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&variables="
        variables = {
            "id": user_id,
            "first": page_size,
            "after": None,
        }
        page = 1
        while True:
            result = session.scrape(ScrapeConfig(base_url + quote(json.dumps(variables)), asp=True))
            posts = json.loads(result.content)["data"]["user"]["edge_owner_to_timeline_media"]
            for post in posts["edges"]:
                yield post["node"]
            page_info = posts["page_info"]
            if not page_info["has_next_page"]:
                break
            variables["after"] = page_info["end_cursor"]
            page += 1
            if page > page_limit:
                break
    
    def continuous_run(self):
        """
        Uses API key to activate scrapinf functions.
        """

        #retrieve key from env
        
        s_key = config('scrapfly_key', default="")
        
        result_user_posts = []
        with ScrapflyClient(key=s_key, max_concurrency=2) as session:
            result_user = self.scrape_user(self.instagram_username, session)
            result_user_posts = list(self.scrape_user_posts(result_user["id"], session, page_limit=5))
            print("done")
        
        pprint.pprint(result_user_posts)
        return result_user_posts
    
    
    def test_method_no_API(self):
        """
        Instagram has high security measures even for public data. Thus, I use scrapfly service to bypass them. scarpflyis expensive. Therefore, for testing purposes I just return a default string.
        
        """
        default = ['This HBCU homecoming season, take a look back at the 2022 HBCU NY Football Classic, the big matchup between Howard University and Morehouse College. Continuing our support for HBCUs, we sponsored the halftime show and partnered with HBCU Tools for School Foundation to provide scholarships to 100+ HBCU students. At the link in bio, learn more about our efforts to support HBCUs from our Chief Diversity Officer Melonie Parker.🎥: @saucierfilms','Creep out your friends this Halloween with our frightening Art Filters that will transform your selfies and videos into scary artworks, including:\U0001f7e0"Head of a Skeleton with a Burning Cigarette" #VincentvanGogh @vangoghmuseum\U0001f7e0"The Ghost of a Flea" #WilliamBlake @tate\U0001f7e0"Monk Talking to an Old Woman" #FranciscoGoya @princetonu_artmuseum\U0001f7e0"A Clown" #GeorgeLuks @mfaboston \U0001f7e0“Self-Portrait with Magic Scene” #PietervanLaer @theleidencollection Try it out in the @GoogleArtsCulture app and tag us to share your results!','BOO-lieve it or not, the Great Ghoul Duel #GoogleDoodle game is back and spookier than ever! 👻 This year, a group of ghosts are teaming up for their own version of trick-or-treat in the multiplayer interactive Halloween Doodle game. Head to our homepage through Halloween to go ghoul-to-ghoul against players from around the world. Swipe ➡️ to see more from today’s game. 🎃','Zero day exploits are among the most dangerous types of cyberattacks. Go behind the scenes with Project Zero, our specialized task force devoted to finding vulnerabilities before the attackers do. Tap the link in our bio to watch EP005, the final episode of the HACKING GOOGLE series, now streaming on YouTube.','New snack unlocked.','#F1 driver @danielricciardo burns rubber on a different track with a one of a kind #GoogleChrome x @McLaren bike in our Mountain View office. Now he won’t be late to any of his * very important * meetings.','We thought these costume ideas deserve a round of a-paws, and Google Trends agrees:\xa0🧙\u200d♀️ “Witch” was the most-searched Halloween costume last month in the U.S.🏴\u200d☠️ Searches for pirate costumes more than doubled over the last month in the U.S.👻 “Ghost” had the second-highest trending search volume for Halloween costumes this year in the U.S.🤠 Searches for cowboy costumes increased 165% over the last month in the U.S.\xa0Which one is your favorite? Vote in the comments, and tap the link in bio to learn more about Halloween trends in this year’s #GoogleFrightgeist. #GooglePixel #TeamPixel #Pixel7','Unlock the mysteries of the ancient civilizations of Mesoamerica (and save the world while you’re at it) in The Descent of The Serpent, the first-ever video game from Google Arts & Culture. 🎮 Created in partnership with @mnantropologia, the game will transport you back in time to search for hidden treasures in a multi-level maze of jungles, mountains, coasts and caves. Search Descent of the Serpent on Google Arts & Culture to play and drop your high score below! ⬇️','The better way to Wi-Fi. The new #NestWifi Pro is inspired by the home and built to perform.🏡 Designed to complement your space and be placed out in the open where Wi-Fi routers work best⚡ Built for advanced Wi-Fi 6E that delivers super fast speeds and a reliable connection🎨 Snow, Linen, Fog, and Lemongrass colors that blend in with your decor⭐️ A high gloss finish brings out the best in every color♻️ Made with over 60% recycled materials based on product weight'"Get Google's fastest Wi-Fi yet at GoogleStore.com",'High schoolers, lawyers, IT professionals, hobbyists — meet our bug hunters. Their backgrounds vary, but their job is the same: find undiscovered vulnerabilities by trying to hack Google. Tap the link in our bio to watch EP004 of the HACKING GOOGLE series, now streaming on YouTube.','Vast oak woodlands and lush willow groves once stretched from Palo Alto to San Jose and beyond, long before the rise of Silicon Valley. Now, our real estate and ecology teams are working to bring nature back into our built environment — restoring those critical habitats across our Bay Area campuses to create a welcoming environment for pollinators, birds, mammals and more. Swipe through to see some of the plants and animals that share our space, and tap the link in our bio to learn more about our restoration efforts.','Team McLaren and Google Chrome are engineered for speed.\xa0Watch Lando '"Norris use #Chrome's Password Manager to race against his own pit crew in "'under 3 seconds. 🏁🎉\xa0Tap our link in bio to race the clock in our Chrome Pit Crew mobile game! #USGP','Dance K-pop style with @googleartsculture lab and @vamuseum 🇰🇷 Take a tour of Hallyu! The Korean Wave with K-pop dancers @louise.quan @yanalesyk_ @juju_bon, @_bysherry and @uyenlex. The exhibition is a joyful celebration of South Korean pop culture and its impact on cinema, drama, music, fandom, beauty and fashion.\xa0 Featuring more than 200 objects and immersive experiences, you can dance to become part of the art with this unique installation created in collaboration with Google Arts & Culture Lab. Tag a K-culture fan who’d love to try this 👇 @lovekpopdancelondon','"Almost all the work I do is inspired by nature and how I feel as a Black woman in nature,” explains Portland-based artist Paula Champagne @makerchamp. Paula was a 🌿 natural 🌿 choice to create a landscape-inspired mural for the Google Portland office. “For this project, I thought about someone going on a nature walk and collecting leaves to create a collage,” she says. #GooglePortland #LifeAtGoogle','Try Google Photos’ new collage editor, which lets you make fun, shareable collages to give your pics a little something extra. We partnered with talented artists @lisacongdon and @shantell_martin to create exclusive designs for a limited time. Get inspired and transform your favorite memories.',"If you STAY game ready, you won't have to GET ready! With its 120Hz display, "'the new cloud gaming #Chromebook is designed to LEVEL UP your game. Check out its RGB keyboard and access to 1000+ games on chromebook.com. #ad @google',"POV: You can't stop taking photos with your new @googlepixel 📸 #Pixel7 "'#Pixel7Pro #MadeByGoogle','Celebrate the final weekend of #HispanicHeritageMonth with delicious empanadas from @AllRealMeal — a Latina-owned meal prep business. 🇵🇷Tap the link in bio to learn more about this business. #GrowWithGoogleIngredients:- homemade turnover pastry dough (or you can purchase frozen dough in the Latin foods section of your grocery store freezer)'"- grass-fed beef (season with a little sea salt, you don't need a lot "'because the olives are salty) - 1 cup recaito (prepare ahead of time or purchase premade)- 1 8-ounce can tomato sauce- 1 cup chopped dates- 6 finely chopped cloves of garlic - 1 cup spanish olives with pimentos- corn or vegetable oil for frying1. defrost dough if necessary to prepare for filling2. prepare frying pan with extra virgin olive oil3. begin frying garlic4. add grass fed and cook evenly as it begins to brown5. add dates first so they soften and cook down6. follow with recaito, tomato sauce, and olives 7. once beef filling is fully browned salt just to taste8. put beef filling in another container to cool in the fridge'"9. once filling has completely cooled you're ready to start preparing "'empanadas10. put about an 1/8th of a cup of filling in the center of each round of dough11. fold over and seal the edges with your fingers first, and then follow that with a fork all the way around on both sides12. repeat 13. heat oil at medium low to medium (to test readiness drop a tiny piece of empanada dough in oil and see if it rises to the top) 11. when oil is ready, put empanadas in the oil in small batches12. fry 2-3 minutes, making sure both sides are cooked evenly13. remove from oil and place on serving tray lined with paper towels to absorb excess oil14. finish with a sea salt and a little garlic powderNow that you know the basic production, you can try other fillings as well. Repeat the same steps, and remember to always prepare your sweet empanadas before your savory ones.Country Breakfast Empanadas: replace beef filling mixture with scrambled eggs, crumbled bacon and sausage, and cheddar cheese, finish by brushing with maple syrup and melted butter.','Meet the internet’s fire department, the elite team that answers the call when chaos ignites online. When our Detection and Response Team discovers an attacker, they have to be swift and precise. Tap the link in our bio to watch EP002 of the HACKING GOOGLE series, now streaming on YouTube.','Meet the new #Pixel7 and Pixel 7 Pro, the most advanced Google phones yet.🔍 Macro Focus helps you photograph the tiniest details📷 Super Res Zoom lets you take beautiful, detailed photos from a distance\U0001fa84 Magic Eraser removes distractions like photobombers with ease¹🌍 Live Translate works as you read, talk, or type to help you navigate different languages²🔋 Extreme Battery Saver lets you stay out longer with up to 72 hours of power³Explore both Pixel 7 and Pixel 7 Pro in stores or online today at GoogleStore.com¹Requires Google Photos app. May not work on all image elements²Not available in all languages or countries. Not available on all media or apps. See g.co/pixel/livetranslate for more information. Translation may not be instantaneous.³Estimated battery life based on testing using a median Pixel user battery usage profile across a mix of talk, data, standby, and use of other features. Average battery life during testing was approximately 31 hours. Battery testing conducted on a major carrier network. For “Up to 72 hours”: Estimated battery life based on testing using a median Pixel user battery usage profile across a mix of talk, data, standby, and use of limited other features that are default in Extreme Battery Saver mode (which disables various features including 5G connectivity). Battery testing conducted on a major carrier network. For both claims: Battery testing conducted in California in mid 2022 on pre-production hardware and software using default settings, except that, for the “up to 72 hours” claim only, Extreme Battery Saver mode was enabled. Battery life depends upon many factors and usage of certain features will decrease battery life. Actual battery life may be lower.','Make your next career move one that excites you. Swipe to find the high-growth industry + Google Career Certificate pairing that speaks to you. Visit the link in bio for more info. #GrowWithGoogle','“Being Puerto Rican, I view dominos as a cultural icon. More than a game, it represents a sense of gathering and community heavily tied to family tradition.” — Ana Cristina Quiñones, owner of @MateriaMadura, the Puerto Rican-based company that makes this domino set and other home goods.Swipe through to see how these dominos were made, and learn more about this Latina-owned sustainable design company at the link in bio. #GrowWithGoogle #HispanicHeritageMonth','Ramen or a cocktail? It’s always best to double check. That’s why @sxmplyNi uses our 2-Step Verification to keep his account safe. Tap the link in our bio to learn more and stay #SaferWithGoogle.','Everyone should be able to take a great selfie 🤳 — just ask @mollyburkeofficial.#Pixel7’s new #GuidedFrame helps blind and low-vision users get the pic with a combination of audio guidance, high-contrast visual animations, and haptic feedback.Pre-order Pixel 7 & Pixel 7 Pro at GoogleStore.com','Today on #NationalComingOutDay, we continue our support of the #LGBTQ+ community by celebrating the importance of coming out, and by acknowledging how challenging it can be for some due to a variety of personal circumstances. Choosing when and how to come out is a deeply personal decision.\xa0Tap the link in the bio to read the powerful coming out stories of four Googlers from around the world.','Go behind-the-scenes of today’s video #GoogleDoodle with Tito Puente Jr. and guest artist, Carlos Aponte, as they share inspiration behind the Doodle celebrating renowned “Nuyorican” percussionist, composer, songwriter, recording artist and bandleader — Tito Puente 🥁','Support the Indigenous community year-round with these tips from Cece Meadows of @pradosbeauty, a beauty brand for Xicana/Indigenous women. At the link in bio, learn how she became the first Native American makeup artist to head a New York Fashion Week show, and landed her products in retailers nationwide. #GrowWithGoogle #IndigenousPeoplesDay #HispanicHeritageMonth','First Look: Super Res Zoom on #Pixel7 Pro.Pre-order now at GoogleStore.com#MadeByGoogle','First Look: Macro Focus on #Pixel7Pre-order at GoogleStore.com#MadeByGoogle','Watchguards. Lookouts. Sentries. Who looks out for threats when they happen online? Meet the Google team that keeps a constant eye out for danger on the internet. Tap the link in our bio to watch EP001 of the HACKING GOOGLE series, now streaming on YouTube.','Snapshots from a Pixel-perfect day 📸Tap the link in our bio to catch up on all the news from this week’s #MadeByGoogle event. #TeamPixel #ShotOnPixel','Checking out the new Google Pixel devices at #MadeByGoogle ✨ #DayInTheLife #DITL','Your Google Pixel phone, watch, and buds work together to unlock all kinds of help throughout your day.🔄 Sync and switch between devices with ease¹💓 Take charge of your health with @Fitbit²🔈 Enjoy premium, immersive sound on-the-go🏃 Get turn-by-turn directions and speed through checkout³🏡 Control your smart home at the touch of a button⁴Connect, move, and stay synced with the Google Pixel Collection.¹Fast Pair requires location enabled. Devices sold separately.²Some features may require Fitbit account and mobile app.³Data rates may apply.  Google apps and services are not available in all countries or languages.⁴Connected home control requires compatible smart devices.','Any day at #GoogleAustin looks like a great day — thanks for showing us around, Antoinette! #Austin #LifeAtGoogle','Introducing #NestWifi Pro with Wi-Fi 6E, our sleekest, most stylish Wi-Fi system yet.💨 2x faster than Wi-Fi 6. (Combined speeds up to 5.4 Gpbs)¹🏠 Coverage for your entire home (up to 2200 square feet per router)²\U0001fa7a Self-monitoring and diagnosing✅ Simple set upPre-order it now at GoogleStore.com¹Up to 2x faster as compared to a Wi-Fi 6 router that supports 80 MHz channels. Wi-Fi 6E specifications are based on use of a Wi-Fi 6 or later generation client device that supports 160 MHz channels. Actual speeds depend on your internet service provider, network conditions, connected device, local regulations and environmental factors. Router placement and home size, materials and layout can affect how Wi-Fi signal travels. Poor router placement and larger homes or homes with thicker walls or long, narrow layouts may require extra Wifi points for full coverage.²Router placement and home size, materials and layout can affect how Wi-Fi signal travels. Poor placement and larger homes or homes with thicker walls or long, narrow layouts may need extra Wifi points for full coverage. Strength and speed of signal will also depend on your internet provider. More than 5 routers in a network may result in degraded performance and is not recommended.','Meet the 2nd-gen wired #NestDoorbell.🔔 The Nest Doorbell includes intelligent alerts, which can tell the difference between a person, package, animal, and vehicle.¹👀 See activity at your front door around the clock. Get peace of mind knowing you can check in 24/7 without having to recharge batteries.¹🚪 A taller, enhanced camera view lets you see people head to toe and packages left on the ground as close as 8 inches from your door.🌗 Get a sharp, vivid view of your front doorstep. HDR helps you see details in sunlight or shadows, while night vision helps you see in the dark.📹 3 hours of included event video history with support for 24/7 continuous video history.²🔌 If Wi-Fi goes out, the Nest Doorbell automatically records events for up to an hour. When it’s back online, you can see exactly what you missed.Buy now at GoogleStore.com¹Some features, including mobile notifications, remote control, video streaming, and video recording, require working internet and Wi-Fi.²Requires Nest Aware Plus subscription (sold separately)']
        print(f"The length of the default string is {len(default)} posts")
        return default
        