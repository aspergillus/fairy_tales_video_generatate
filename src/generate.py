import os
import time
import json
from datetime import datetime

# Step 1: Initialization
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
project_dir = f"project_{timestamp}"
os.makedirs(project_dir, exist_ok=True)
os.makedirs(os.path.join(project_dir, "scripts"), exist_ok=True)
os.makedirs(os.path.join(project_dir, "audio_chunks"), exist_ok=True)
os.makedirs(os.path.join(project_dir, "video_chunks"), exist_ok=True)
os.makedirs(os.path.join(project_dir, "final_render"), exist_ok=True)

# Generate 120 scenes
scenes = []
base_story = [
    # Act 1: Introduction (Scenes 1-15)
    ("Once upon a time, deep in the Whispering Woods, lived a little fox named Finley.", "A wide shot of a glowing, magical forest with giant mushrooms and a cute little orange fox looking curious."),
    ("Finley loved to explore, his orange fur like a tiny flame darting between the ancient, mossy trees.", "Close up of an adorable baby fox running energetically past large, moss-covered tree trunks catching sunlight."),
    ("One sunny morning, he noticed a strange, sparkling light completely different from the sunbeams.", "A sunbeam piercing through the forest canopy, but with strange, floating sparkly blue dust caught in it."),
    ("The light was dancing right above a hollow log.", "A soft glowing blue orb hovering gently over an old, hollow wooden log in the forest."),
    ("Finley bounded over, sniffing the air, which smelled faintly of toasted marshmallows.", "Close up on the fox's nose twitching, with a glowing blue light reflecting in его big expressive eyes."),
    ("Inside the log was a tiny, shimmering crystal the color of the twilight sky.", "A dark hollow log interior, containing a small, uncut crystal glowing intensely with purple and blue starry light."),
    ("As he reached out with one white-tipped paw, the crystal hummed a soft, melodic tune.", "The fox's white paw gently touching a radiant blue crystal that pulses with light."),
    ("Suddenly, a tiny voice echoed, 'Hello, Finley! Thanks for finding me.'", "The glowing crystal sparking as if trying to speak, magical particles floating around it."),
    ("Finley jumped back in surprise! His ears stood straight up like little antennas.", "The little fox caught mid-leap backwards, looking shocked, ears pointed perfectly straight up."),
    ("'Who... who said that?' he squeaked, looking behind the log.", "The fox peeking cautiously around the side of the wooden log, looking for the source of the voice."),
    ("'I am Lumi, the Star Seed,' the voice chimed from the crystal.", "A close up of the beautiful, glowing purple-blue crystal vibrating with gentle magical energy."),
    ("'I fell from the night sky, and I need help getting back before sunset.'", "A magical visualization showing a shooting star falling from a dark starry night sky into the forest."),
    ("'If I don't return, the forest will lose its nighttime glow forever,' Lumi warned.", "A dark, sad version of the magical forest, showing the glowing mushrooms dimming and losing their color."),
    ("Finley puffed out his little furry chest. 'I will help you, Lumi!' he declared.", "The brave little fox puffing out his chest proudly, standing tall next to the glowing crystal."),
    ("And so, the greatest adventure in the Whispering Woods began.", "A wide cinematic shot of the brave fox walking deeper into the magical glowing forest, the crystal hovering behind him."),

    # Act 2: The Journey Begins (Scenes 16-30)
    ("Lumi floated out of the log, hovering just above Finley's swift little paws.", "A glowing blue crystal floating magically through the air right beside a walking red fox."),
    ("Their first challenge was crossing the Giggling River, known for its ticklish waters.", "A wide shot of a sparkling river bubbling and splashing playfully over colorful, smooth river stones."),
    ("Finley tested the water with a toe, and immediately burst into a fit of giggles.", "The fox touching the water with one paw and pulling it back quickly, laughing, bubbles splashing around him."),
    ("'It's too giggly!' Finley laughed, rolling on the grassy bank.", "The fox rolling on his back in the green grass beside the sparkling river, looking incredibly happy."),
    ("'Look for the Sleepy Stones,' Lumi guided, shining her light on the riverbed.", "The crystal casting a bright beam of light into the water, revealing dark, smooth rocks under the surface."),
    ("Finley saw a path of flat, dark purple stones that weren't bubbling at all.", "A clear pathway of smooth, dark purple stepping stones crossing the bubbly river."),
    ("He carefully hopped from stone to stone, balancing his bushy tail.", "The cute fox balancing delicately on one leg on a purple stepping stone over the rushing water."),
    ("Hop. Hop. Hop. He was halfway across when a slippery moss patch caught his paw!", "Close up of the fox's paw slipping on green moss on a purple stone, water splashing nearby."),
    ("Whoosh! Finley started to fall toward the giggling, bubbling water.", "The fox flailing his arms comically in mid-air, about to fall into the bright blue river."),
    ("But Lumi darted under him, providing a soft cushion of magical air to bounce him up!", "The glowing blue crystal creating a visible trampoline of blue light underneath the falling fox."),
    ("Finley landed safely on the other side, shaking a few loose water droplets off his coat.", "The fox safely on the grass, shaking his body like a dog, water droplets flying off his fur in slow motion."),
    ("'Phew! Thank you, Lumi,' Finley smiled, his tail wagging fast.", "The fox smiling brightly at the hovering crystal, his fluffy tail wagging enthusiastically."),
    ("'We make a great team,' the star seed chimed back, glowing a little brighter.", "The crystal pulsing with warm, bright light, floating in the lush, vibrant forest environment."),
    ("They walked into a grove of trees whose leaves were made of shimmering silver.", "A majestic grove of tall trees with leaves that shine like polished silver under the sunlight."),
    ("The wind blew through the silver leaves, making a sound like tiny wind chimes.", "Silver leaves blowing gently in the wind, sparkling brightly as they catch the light."),

    # Act 3: The Riddle of the Owl (Scenes 31-45)
    ("In the center of the silver grove sat Orion, the oldest owl in the forest.", "A massive, wise-looking grey owl with glowing yellow eyes perched on a thick silver branch."),
    ("Orion peered down through a pair of spectacles made from dew drops.", "Close up of the giant owl's face, looking through magical spectacles made of clear water droplets."),
    ("'Who passes through my silver domain?' Orion hooted, ruffling his massive feathers.", "The giant wise owl ruffling his majestic feathers, looking down imposingly from his high branch."),
    ("'I am Finley, and this is Lumi. We need to reach the Star Peak before sunset!'", "The brave little fox looking up, speaking proudly, with the glowing crystal hovering next to his ear."),
    ("'Ah, Star Peak,' Orion nodded slowly. 'The path is hidden. You must answer my riddle.'", "The wise owl looking deeply thoughtful, nodding slowly in the magical silvery tree grove."),
    ("Finley sat down, wrapping his tail around his paws, ready to listen closely.", "The fox sitting attentively on the mossy forest floor, wrapping his fluffy tail neatly around his front paws."),
    ("'I have cities, but no houses. I have mountains, but no trees,' Orion began.", "A visual representation of an antique map, showing drawn cities and mountains in a faded parchment style."),
    ("'I have water, but no fish. What am I?' the old owl asked softly.", "An ancient map showing oceans and rivers drawn in ink, with a glowing question mark over it."),
    ("Finley thought hard. Cities with no houses? Mountains with no trees?", "Close up of the fox looking confused but intensely thoughtful, tapping his chin with one tiny paw."),
    ("He looked at the ground, he looked at Lumi, he looked at his own paws.", "The fox looking around the forest floor, then glancing at the glowing crystal beside him."),
    ("Suddenly, he remembered the big paper object his grandpa kept in the den.", "A thought bubble showing an old, wise fox studying a large paper map spread out on a table."),
    ("'A map!' Finley shouted, jumping up in excitement. 'The answer is a map!'", "The little fox jumping high into the air with joy, his eyes wide and excited."),
    ("Orion chuckled, dropping a silver feather that turned into a glowing parchment.", "The wise owl laughing gently, as a glowing silver feather falls from him and transforms into a shining map."),
    ("'Well done, clever fox. Follow the light on this map,' Orion instructed.", "A glowing golden map unrolling itself in mid-air, with a bright trail of light showing a pathway."),
    ("Finley grabbed the glowing map in his mouth, waving his tail in thanks.", "The cute fox holding the glowing, magical map in his mouth, waving goodbye to the giant owl."),

    # Act 4: The Cave of Echoes (Scenes 46-60)
    ("The golden path on the map led them straight to a dark, intimidating cave.", "A massive, dark, scary cave entrance carved into the side of a tall, rocky mountain."),
    ("The entrance was shaped like a giant, yawning mouth with stalactite teeth.", "A close up of the cave entrance, with sharp, jagged rocks hanging from the ceiling like monster teeth."),
    ("'This is the Cave of Echoes,' Lumi whispered, her glow dimming slightly in fear.", "The blue crystal glowing faintly in the dark, hovering close to the fox for comfort."),
    ("'Don't worry, my nose will guide us,' Finley said bravely, stepping into the gloom.", "The brave fox taking his first step into the pitch-black cave, his nose sniffing the air."),
    ("Inside, every sound repeated a dozen times. 'Hello-lo-lo-lo!' Finley cried.", "The fox calling out into a massive, cavernous space with glowing crystals on the walls."),
    ("Suddenly, a swarm of glowing flutter-bats dropped from the ceiling!", "Thousands of tiny, glowing purple bats swooping down from the high ceiling of the dark cave."),
    ("Instead of being scary, they were ticklish, brushing against Finley's ears.", "The cute glowing bats flying around the fox's head, brushing his ears playfully as he giggles."),
    ("But they were blocking the path! They swarmed like a thick, glowing cloud.", "A dense, thick cloud of glowing purple bats completely blocking the tunnel ahead."),
    ("Lumi realized what to do. 'Finley, hum a gentle lullaby!' she suggested.", "The blue crystal glowing brightly, pulsating to the rhythm of a gentle, soothing song."),
    ("Finley took a deep breath and began to hum a sweet, slow melody.", "The little fox sitting down, closing his eyes peacefully, and humming a gentle tune."),
    ("As the lullaby echoed, the flutter-bats slowed down, their wings moving in slow motion.", "The glowing bats flying slower and slower, their lights dimming to a soft, sleepy purple."),
    ("One by one, the bats flew back up to the ceiling and tucked themselves to sleep.", "The bats hanging upside down from the cave ceiling, wrapping their wings around themselves to sleep."),
    ("The path was clear again. Finley tiptoed quietly so he wouldn't wake them.", "The fox walking on his tiptoes extremely carefully through the dark cave under the sleeping bats."),
    ("They finally saw a beam of natural sunlight at the end of the long tunnel.", "A bright, beautiful beam of warm sunlight shining through the exit of the dark cave."),
    ("'We made it!' Finley whispered happily, running toward the brightness.", "The fox running enthusiastically toward the bright light at the end of the cave tunnel."),

    # Act 5: The Mischievous Monkeys (Scenes 61-75)
    ("They emerged from the cave onto a high plateau filled with twisted, colorful vines.", "A vibrant mountain plateau covered in thick, spiraling vines of pink, yellow, and bright green."),
    ("Suddenly, a group of tiny, blue-furred monkeys swung down from the vines.", "Cute, tiny monkeys with bright blue fur swinging wildly from the colorful jungle vines."),
    ("In a flash, one of the monkeys snatched the glowing map from Finley's mouth!", "A quick, cheeky blue monkey snatching the glowing paper map right from the fox's mouth."),
    ("'Hey! Give that back!' Finley barked, chasing after the giggling monkey.", "The fox running fast on his short legs, barking excitedly at the monkey swinging above him."),
    ("The monkeys tossed the map back and forth to each other like a game of catch.", "Three blue monkeys throwing the glowing paper map to each other through the air, laughing."),
    ("Lumi zoomed up. 'Wait! Monkeys love trades. Give them something shiny!'", "The glowing crystal darting up toward the monkeys, flashing brightly to get their attention."),
    ("Finley remembered the silver feather they found near Orion the owl.", "A close up of the fox's paw holding the beautiful, shining silver feather they got earlier."),
    ("He held the shiny feather high in the air so it caught the sunlight beautifully.", "The fox standing on his hind legs, holding a brilliantly shining silver feather up in the bright sun."),
    ("The monkeys stopped. Their huge, round eyes were captivated by the silver shine.", "Close up of the blue monkeys, their big eyes wide with wonder, staring completely mesmerized."),
    ("The leader monkey slowly lowered itself on a vine, holding the map out.", "A cute blue monkey hanging upside down by its tail, extending its hand holding the glowing map."),
    ("Finley gently took the map and handed over the beautiful silver feather.", "The fox and the monkey carefully exchanging the glowing map for the shiny silver feather."),
    ("The monkey chattered happily, putting the feather behind its little ear like a hat.", "The blue monkey smiling wide, wearing the silver feather proudly behind its ear."),
    ("The whole troop of monkeys swung away, leaving Finley and Lumi to continue.", "The group of blue monkeys swinging away into the dense colorful vines, disappearing from sight."),
    ("'Good thinking, Lumi,' Finley said, unrolling the map to see the final stretch.", "The fox looking down at the glowing map, which is now pointing to a massive mountain peak."),
    ("The map showed that Star Peak was just up one final, steep flight of stone stairs.", "A majestic, steep stairway carved out of white stone, leading up a massive mountain to the sky."),

    # Act 6: The Climb to Star Peak (Scenes 76-90)
    ("The stairs to Star Peak were carved from clouds that had turned entirely to stone.", "Fluffy-looking but solid white stone steps leading up into the misty sky, looking like frozen clouds."),
    ("With every step they took, the air grew colder and the sky grew darker.", "The color palette shifting to deep blues and purples as the sky transitions quickly toward evening."),
    ("Finley shivered, his orange fur fluffing up to keep himself warm in the chill.", "The cute fox looking extremely fluffy, shivering slightly as small snowflakes begin to fall."),
    ("Lumi hovered close to him, sharing her warm, glowing, magical energy.", "The blue crystal glowing with a warm, fiery aura, acting like a tiny heater for the cold fox."),
    ("They climbed higher and higher, until they were above the actual clouds.", "A breathtaking view from above a thick layer of white clouds, with only mountain peaks poking through."),
    ("The sun was beginning to set, turning the horizon into a blazing sea of pink and gold.", "A stunning sunset painting the sky with brilliant, vivid streaks of orange, pink, and gold."),
    ("'Hurry, Finley! My magic is fading as the sun goes down!' Lumi cried.", "The blue crystal looking faintly transparent and weak, its light flickering like a dying candle."),
    ("Finley pushed his tired little legs to climb the last massive steps as fast as he could.", "The determined fox panting, pushing hard to climb massive stone steps much larger than he is."),
    ("Finally, they reached the summit—a smooth, flat pedestal of ancient white marble.", "A perfectly flat, circular platform made of pristine white marble at the very top of the mountain."),
    ("In the center of the pedestal was a small, star-shaped depression.", "A close-up of a carved hollow in the marble floor, shaped exactly like a five-pointed star."),
    ("But guarding the pedestal was a massive statue of a dragon covered in frost.", "A giant, imposing statue of a dragon made entirely of dark stone, covered in sharp, glowing ice crystals."),
    ("As they approached, the icy dragon's eyes suddenly glowed with a fierce, cold blue light!", "The stone dragon's carved eyes suddenly flaring up with terrifying, icy magical light."),
    ("It slowly moved its heavy stone head. 'Only those with pure hearts may pass,' it rumbled.", "The massive stone dragon shifting its weight, causing ice to crack and fall off its giant body."),
    ("Finley stood tall. 'I climbed all the way up here just to help my friend go home!'", "The tiny, brave fox standing bravely up against the massive, terrifying ice dragon, shouting."),
    ("The dragon stared deeply into Finley's eyes, searching his soul for truth.", "A tight close-up of the giant dragon's glowing blue eye staring directly into the tiny fox's brown eyes."),

    # Act 7: The Return of the Star (Scenes 91-105)
    ("After a tense moment, the dragon's icy glow softened into a warm, gentle gold.", "The dragon's scary blue glowing eyes changing color to a soft, welcoming, and warm golden yellow."),
    ("The stone dragon unblocked the path, bowing its enormous head in deep respect.", "The massive stone dragon moving out of the way and bowing its huge head politely to the small fox."),
    ("'Your heart is true, little fox. Approach the Star Pedestal,' the dragon said.", "The dragon speaking softly as it steps aside, revealing the glowing white marble pedestal behind it."),
    ("Finley ran to the center of the pedestal. The sun was exactly half-hidden by the horizon.", "The fox dashing to the center platform, with an epic, breathtaking half-sunset in the background."),
    ("'This is it, Lumi. The star-shaped hole!' Finley pointed to the carving.", "The fox's paw pointing excitedly at the perfect star-shaped indentation in the white marble floor."),
    ("Lumi floated down slowly, her light almost completely gone, barely a flicker.", "The crystal now looking very dull and grey, slowly descending toward the marble floor."),
    ("'Thank you, Finley. You are the bravest fox in the world,' she whispered weakly.", "The tiny blue crystal resting in the fox's gentle paws one last time, looking fragile."),
    ("Finley gently placed the star seed perfectly into the star-shaped carving.", "A close-up of the fox carefully placing the crystal into the matching indentation in the marble."),
    ("For a second, nothing happened. The wind stopped blowing. Everything was silent.", "A completely still, silent moment on the mountain peak. Nothing is moving. Perfect tension."),
    ("Then, a massive beam of intense, brilliant blue light shot straight up into the sky!", "A gigantic, blinding pillar of blue magical light erupting from the pedestal straight into the space."),
    ("The beam hit the darkening sky, exploding like a massive, silent firework.", "The blue light exploding high in the sky, creating ripples of magical energy across the atmosphere."),
    ("Suddenly, a billion new stars appeared in the night sky, shining brighter than ever.", "A breathtakingly beautiful, clear night sky filled with millions of incredibly bright, twinkling stars."),
    ("The entire forest below lit up in a beautiful, bioluminescent, magical glow.", "Looking down from the mountain, the entire forest below glowing with beautiful neon blues, pinks, and greens."),
    ("Lumi's voice echoed from the stars. 'I'm home! The forest's magic is restored!'", "The starry sky twinkling in a pattern that almost resembles a smiling face, radiating warmth."),
    ("Finley looked up, his eyes reflecting the beautiful, starry night. He had done it.", "A beautiful close up of the fox's face, with the reflection of a million bright stars in his happy eyes."),

    # Act 8: The Hero's Rest (Scenes 106-120)
    ("The stone dragon lowered its wing, offering Finley a gentle ride back down the mountain.", "The giant stone dragon laying its massive wing flat on the ground like a ramp for the fox."),
    ("Finley hopped on, exhausted but incredibly happy, snuggling into the cool stone.", "The tired little fox curling up comfortably in the small crevice of the dragon's giant stone wing."),
    ("With a gentle leap, the stone dragon glided smoothly down from the clouds.", "The massive stone dragon flying gracefully and smoothly down through the night sky, carrying the fox."),
    ("They landed softly right outside Finley's cozy little den in the Whispering Woods.", "The dragon landing completely silently on the soft moss right next to a cozy hole at the base of a tree."),
    ("Finley hopped off and bowed to the dragon. 'Thank you for the ride, Mr. Dragon!'", "The fox bowing gracefully to the giant dragon, waving his little paw in gratitude."),
    ("The dragon nodded silently and soared back up into the starry night sky.", "The stone dragon flying beautifully upwards into the stars, disappearing into the dark blue distance."),
    ("Finley walked into his den, which was warm, safe, and smelled like dried leaves.", "The inside of a very cozy, warm fox den under tree roots, filled with soft dried brown leaves."),
    ("He curled up into a perfect little orange ball, tucking his nose under his bushy tail.", "The cute fox curling up tightly into a perfect circle, his big fluffy tail covering his face for warmth."),
    ("Through the roots of his ceiling, a single, perfectly bright star twinkled down at him.", "Looking up from the inside of the den, a single exceptionally bright star shining through a gap in the roots."),
    ("It pulsed softly, two times, a glowing 'thank you' from his friend Lumi.", "The bright star in the sky flashing exactly twice with a noticeable blue tint, sending a silent message."),
    ("Finley smiled in his sleep, dreaming of flying through the starry sky with his friend.", "The sleeping fox smiling peacefully, a tiny dream bubble forming over his head showing stars."),
    ("The Whispering Woods were safe and magical once again, glowing peacefully all night long.", "A wide drone shot of the entire magical forest glowing beautifully and peacefully under the starlight."),
    ("And though Finley was just a little fox, he knew he could do big things.", "A beautiful, painterly shot of the sleeping fox, looking heroic even in his peaceful slumber."),
    ("Tomorrow would bring a brand new day, and perhaps, a brand new adventure.", "The camera panning slowly up from the sleeping fox den to the vibrant, magical glowing forest outside."),
    ("But for now, the hero of the magical forest rested easy under the watchful stars.", "A final, epic wide shot of the starry sky over the forest, slowly fading to black softly.")
]

# We need exactly 120 scenes. The base_story has 75 elements. Wait, act 1-8 * 15 = 120 elements!
# Let's count them: 8 blocks of 15 = 120. Perfect.

for i, (narration, prompt) in enumerate(base_story):
    scenes.append({
        "scene_number": i + 1,
        "narration": narration,
        "visual_prompt": prompt
    })

output = {
    "title": "Finley's Starry Adventure",
    "scenes": scenes
}

json_str = json.dumps(output, indent=2)

with open(os.path.join(project_dir, "scripts", "story.json"), "w") as f:
    f.write(json_str)

print(json_str)
