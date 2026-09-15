import discord
from discord.ext import commands
import random
import os
import io                 
from PIL import Image
from dotenv import load_dotenv  # NEW: Import dotenv

# Load environment variables from the .env file
load_dotenv()

# --- CONFIGURATION ---
TOKEN = os.getenv('DISCORD_TOKEN')  # NEW: Fetch token securely
IMAGE_DIR = './images'

# --- THEME CONFIGURATION ---
# The keys (e.g., 'sapphires') must match your folder names in /images/ exactly.
SUIT_CONFIG = {
    "sapphires": {
        "element": "Water 💧",
        "keywords": "Emotion, Intuition, Subconscious",
        "color": 0x0F52BA  # Sapphire Blue
    },
    "emeralds": {
        "element": "Earth 🌿",
        "keywords": "Material World, Finances, Stability",
        "color": 0x50C878  # Emerald Green
    },
    "rubies": {
        "element": "Fire 🔥",
        "keywords": "Passion, Willpower, Energy",
        "color": 0xE0115F  # Ruby Red
    },
    "crystals": {
        "element": "Air 💨",
        "keywords": "Intellect, Logic, Communication",
        "color": 0xA9C6D9  # Crystal/Pale Blue-Grey
    },
    "amethysts": {
        "element": "Spirit 🔮",
        "keywords": "Fate, Karma, Major Life Lessons, Destiny",
        "color": 0x9966CC  # Amethyst Purple
    }
}
# --- CARD MEANINGS (THE LORE) ---
# Keys must match the filename rank (e.g. 'Ace', 'King', 'The Magician')
CARD_MEANINGS = {
    # --- SUIT OF RUBIES (Wands / Fire) ---
    "Rubies": {
        "Ace": {
            "upright": "A sudden spark of inspiration. Like a Ruby dragon's breath, a new passion ignites within you. Seize this surge of energy.",
            "reversed": "Delays in your creative plans. The fire is there, but the wood is damp. Frustration or lack of focus."
        },
        "Two": {
            "upright": "Planning the hoard. You are looking out from your lair at the vast world, deciding where to fly next. Discovery and preparation.",
            "reversed": "Fear of the unknown. You are staying in the cave when you should be taking flight. Over-analysis."
        },
        "Three": {
            "upright": "Expansion and foresight. Your territory grows. Your ships (or wings) are coming in. Success is on the horizon.",
            "reversed": "Obstacles and delays. You are waiting for a hoard that hasn't arrived yet. Patience is required."
        },
        "Four": {
            "upright": "Celebration and homecoming. A safe lair established. Harmony, relaxation, and enjoying the heat of the hearth.",
            "reversed": "Conflict in the home or lair. Tension during what should be a celebration. instability."
        },
        "Five": {
            "upright": "Competition and conflict. Young dragons sparring. It is chaotic and noisy, but it hones your skills. A clash of egos.",
            "reversed": "Avoiding conflict. Shy of the fight. Alternatively, the conflict is over, and you are licking your wounds."
        },
        "Six": {
            "upright": "Victory and recognition. You return with the prize. Others look to you with respect. Pride and achievement.",
            "reversed": "Egotism or fall from grace. Your pride may be your undoing. A victory that feels hollow."
        },
        "Seven": {
            "upright": "Defensiveness. You stand atop your hoard, challenging all comers. You have the high ground, but the fight is lonely.",
            "reversed": "Overwhelmed. Too many challengers, not enough breath. You may need to yield ground to survive."
        },
        "Eight": {
            "upright": "Speed and movement. Events moving as fast as a diving dragon. Quick decisions, travel, and messages.",
            "reversed": "Chaos and haste. You are flying too fast and missing the details. A crash landing or delayed message."
        },
        "Nine": {
            "upright": "Resilience. Scales battered but unbroken. You are tired from the battle, but you have one last breath of fire left. Stand your ground.",
            "reversed": "Exhaustion. The fight has gone on too long. Your defenses are crumbling. It may be time to retreat."
        },
        "Ten": {
            "upright": "Burden. You are carrying too much gold; it weighs you down. Responsibility is crushing your ability to fly.",
            "reversed": "Release. Dropping the heavy load. Delegating tasks or realizing you don't need to carry the world."
        },
        "Page": {
            "upright": "The Messenger. A spark of curiosity. A young spirit eager to explore the world and find their own flame.",
            "reversed": "A bratty spirit. Impulsive, loud, and lacking follow-through. A message delayed or misunderstood."
        },
        "Knight": {
            "upright": "Action and adventure. Charming, bold, and hasty. Flying into danger just for the thrill of it.",
            "reversed": "Recklessness. A wildfire out of control. Arrogance and scattered energy."
        },
        "Queen": {
            "upright": "Confidence and warmth. She rules with charisma and vibrant energy. Attractive, influential, and independent.",
            "reversed": "Jealousy and temper. A dragon scorned. Demanding attention and lashing out when ignored."
        },
        "King": {
            "upright": "Vision and leadership. The Great Wyrm of Fire. He leads not by force, but by inspiring others to follow his vision.",
            "reversed": "Tyranny. An impulsive dictator. High expectations that no one can meet. Ruthlessness."
        }
    },
    # --- SUIT OF EMERALDS (Pentacles / Earth) ---
    "Emeralds": {
        "Ace": {
            "upright": "A new venture. Like a raw gem found in the deep earth, a tangible opportunity presents itself. Prosperity begins here.",
            "reversed": "A missed opportunity. The gold slipped through your claws. Poor investment or lack of planning."
        },
        "Two": {
            "upright": "Balance. Juggling two hoards at once. You are managing your resources well, but be careful not to drop one.",
            "reversed": "Overextended. Taking on more than you can carry. Financial disarray or lack of organization."
        },
        "Three": {
            "upright": "Teamwork and craftsmanship. Building the lair together. Collaboration brings stability and artful results.",
            "reversed": "Lack of cohesion. The work is shoddy; the team is not flying in formation. Criticism."
        },
        "Four": {
            "upright": "Conservation. You are curling tightly around your gold. Security and stability are yours, but are you trapped by your own greed?",
            "reversed": "Letting go. Spending the hoard. Generosity, or perhaps losing a bit of control over your assets."
        },
        "Five": {
            "upright": "Hardship. A dragon without a lair. Financial loss, isolation, or feeling left out in the cold.",
            "reversed": "Recovery. The storm is passing. You are finding a new shelter and rebuilding what was lost."
        },
        "Six": {
            "upright": "Generosity. Sharing the spoils. You are in a position to help younger drakes, or you are receiving help yourself.",
            "reversed": "Strings attached. A gift that is actually a debt. Selfishness or bad debts."
        },
        "Seven": {
            "upright": "Patience and assessment. Watching the eggs hatch. You have done the work; now you must wait for the rewards to grow.",
            "reversed": "Impatience. Digging up the seed to see if it's growing. Frustration with slow results."
        },
        "Eight": {
            "upright": "Mastery. Polishing the gem. Repetitive work that leads to perfection. honing a skill or trade.",
            "reversed": "Perfectionism. You are polishing the gem until it cracks. Obsession with detail or lack of ambition."
        },
        "Nine": {
            "upright": "Luxury and self-reliance. A magnificent, solitary lair. You have everything you need and enjoy the fruits of your labor alone.",
            "reversed": "Material instability. The lair is beautiful but the foundation is weak. Living beyond your means."
        },
        "Ten": {
            "upright": "Legacy. A hoard passed down through generations. Ancestral wealth, family stability, and long-term success.",
            "reversed": "Family disputes. Fighting over the inheritance. Tradition becoming a burden rather than a blessing."
        },
        "Page": {
            "upright": "A student of lore. Curious about the material world. A grounded young spirit eager to learn how to build.",
            "reversed": "Lazy or rebellious. Refusing to learn the basics. A lack of focus on practical matters."
        },
        "Knight": {
            "upright": "Methodical progress. The tortoise, not the hare. Reliable, hard-working, and stubborn. He gets the job done.",
            "reversed": "Stagnation. Stuck in the mud. So stubborn that you refuse to change course even when necessary."
        },
        "Queen": {
            "upright": "Nurturing and practical. She keeps the lair warm and the larder full. A master of domestic stability and nature.",
            "reversed": "Smothering or materialistic. Caring too much about appearances. Neglecting the spirit for the sake of the coin."
        },
        "King": {
            "upright": "The Entrepreneur. A master of the material plane. He turns stone into gold. Stable, wealthy, and authoritative.",
            "reversed": "Greed. The stereotypical hoarding dragon. Corrupt, miserly, and obsessed with status."
        }
    },

    # --- SUIT OF SAPPHIRES (Cups / Water) ---
    "Sapphires": {
        "Ace": {
            "upright": "Emotional awakening. A wellspring of psionic energy opens up. New love, intuition, or a spiritual breakthrough.",
            "reversed": "Blocked emotions. The well is dry. Repressed feelings or ignoring your intuition."
        },
        "Two": {
            "upright": "Partnership. Two dragons flying in sync. A union of souls, whether romantic or platonic. Mutual respect.",
            "reversed": "Disconnect. Miscommunication. The bond is strained or broken."
        },
        "Three": {
            "upright": "Community. The gathering of the flight. Celebration, friendship, and shared joy.",
            "reversed": "Isolation. Feeling like an outsider in your own flight. Overindulgence in the party."
        },
        "Four": {
            "upright": "Apathy. Offered a new gem, but you refuse to look at it. Boredom, meditation, or withdrawing into oneself.",
            "reversed": "Motivation returning. Waking from the slumber. You are ready to accept new opportunities."
        },
        "Five": {
            "upright": "Grief. Three eggs are broken; two remain. Focusing on what is lost rather than what still stands. Sorrow.",
            "reversed": "Acceptance. Moving past the grief. Seeing the two remaining eggs and finding hope."
        },
        "Six": {
            "upright": "Nostalgia. Echoes of the past. Revisiting an old lair or meeting a friend from a past life. Innocence.",
            "reversed": "Stuck in the past. Refusing to grow up. Idealizing a history that never happened."
        },
        "Seven": {
            "upright": "Illusion and choice. Many glittering prizes, but some are traps. Psionic confusion or daydreaming.",
            "reversed": "Clarity. The illusion fades. You see the true path and make a choice."
        },
        "Eight": {
            "upright": "Abandonment. Leaving the hoard behind. Searching for a higher truth. Walking away from something that no longer serves you.",
            "reversed": "Fear of change. Staying in a bad situation because it is familiar. Drifting aimlessly."
        },
        "Nine": {
            "upright": "Satisfaction. The 'Wish' card. Emotional fulfillment. You are content with who you are and what you have.",
            "reversed": "Smugness. Satisfaction that breeds complacency. Or getting what you wanted and realizing it wasn't enough."
        },
        "Ten": {
            "upright": "Harmony. The perfect family unit. Emotional stability and lasting happiness. The rainbow after the storm.",
            "reversed": "Broken home. Disharmony in the lair. A facade of happiness hiding deeper issues."
        },
        "Page": {
            "upright": "A dreamer. Artistic, intuitive, and sensitive. A messenger of love or psychic insight.",
            "reversed": "Emotional immaturity. A drama queen. Overwhelmed by feelings and unable to articulate them."
        },
        "Knight": {
            "upright": "The Romantic. Following the heart. Idealistic, charming, and in touch with their emotions.",
            "reversed": "Moody and jealous. An emotional manipulator. Action driven by fluctuating feelings."
        },
        "Queen": {
            "upright": "Compassionate and psychic. She sees the truth in your heart. Empathetic and healing.",
            "reversed": "Insecure. Playing the victim. Using emotions to manipulate others."
        },
        "King": {
            "upright": "Emotional balance. He controls the tides. Diplomatic, wise, and calm in a crisis.",
            "reversed": "Cold and manipulative. Repressing emotions to control others. Volatility masquerading as calm."
        }
    },

    # --- SUIT OF CRYSTALS (Swords / Air) ---
    "Crystals": {
        "Ace": {
            "upright": "Clarity. A breath of crystal-clear air. A breakthrough idea or a sharp truth that cuts through confusion.",
            "reversed": "Clouded judgment. Confusion. The idea is flawed or the truth is too painful to accept."
        },
        "Two": {
            "upright": "Stalemate. Caught between two winds. Blindfolded and unable to decide. A truce.",
            "reversed": "Decision made. The blindfold comes off. Moving out of limbo, for better or worse."
        },
        "Three": {
            "upright": "Heartbreak. A crystal shattered. Sorrow, betrayal, and painful separation. The truth hurts.",
            "reversed": "Healing. The pieces are being swept up. Recovery from trauma and forgiveness."
        },
        "Four": {
            "upright": "Rest. The dragon sleeps. Recovery after battle. Meditation and retreat from the chaos.",
            "reversed": "Restlessness. Burnout. You are forcing yourself to work when you need to sleep."
        },
        "Five": {
            "upright": "Hollow victory. Winning the argument but losing the friend. Ambition at the cost of honor. Sneakiness.",
            "reversed": "Resolving conflict. Putting down the weapons. Forgiving a betrayal."
        },
        "Six": {
            "upright": "Transition. Flying to calmer skies. Leaving a turbulent situation for a safer one. Passage.",
            "reversed": "Baggage. Taking your problems with you. Turbulent travel or inability to escape."
        },
        "Seven": {
            "upright": "Deception. The thief in the night. Strategy and stealth, or perhaps lying to get what you want.",
            "reversed": "Confession. The truth comes out. Returning what was stolen. Turning over a new leaf."
        },
        "Eight": {
            "upright": "Restriction. Trapped in a cage of your own making. Paralyzed by fear or overthinking.",
            "reversed": "Freedom. Breaking the chains. Realizing the cage door was open all along."
        },
        "Nine": {
            "upright": "Nightmare. Anxiety and worry keeping you awake. Fear of the future. The shadow in the mind.",
            "reversed": "Waking up. Realizing the fear was unfounded. Letting go of stress."
        },
        "Ten": {
            "upright": "Ruins. Rock bottom. Betrayal or failure. The only way to go is up.",
            "reversed": "Survival. Picking up the pieces. The worst is over, and you are still standing."
        },
        "Page": {
            "upright": "Curiosity. A sharp wit and a tongue to match. Spying, gossip, or a thirst for knowledge.",
            "reversed": "All talk. A gossipmonger. Paranoid or defensive without cause."
        },
        "Knight": {
            "upright": "Swift action. Flying with the wind. direct, intellectual, and incisive. No time for feelings.",
            "reversed": "Impulsive aggression. A loose cannon. Speaking without thinking and causing harm."
        },
        "Queen": {
            "upright": "Perceptive and unbiased. She rules with a sharp mind. Honest, independent, and clear-sighted.",
            "reversed": "Cold-hearted. Cruel or critical. Using intellect to belittle others."
        },
        "King": {
            "upright": "Authority and logic. The judge. He rules by law and reason. Fair but firm.",
            "reversed": "Manipulative genius. Using intelligence to dominate. A tyrant of the mind."
        }
    },
    # --- MAJOR ARCANA (Amethysts / Spirit) ---
    # Note: Use 'Amethysts' as the key if that is your folder name for Majors
    "Amethysts": {
        "The Magician": {
            "upright": "Manifestation. As the Amethyst dragon manipulates gravity, you have the tools to reshape your reality. As above, so below.",
            "reversed": "Trickery and blocked potential. You have the power but lack the will (or intent) to use it correctly."
        },
        "The Empress": {
            "upright": "Creation and abundance. The Mother of Dragons. Fertility, nature, and the birth of new ideas or life.",
            "reversed": "Dependence or emptiness. Creative block. Neglecting your own needs or the needs of your 'hatchlings'."
        },
        "The Chariot": {
            "upright": "Willpower and determination. Harnessing opposing forces (like fire and ice) to move forward. Victory through control.",
            "reversed": "Loss of control. The dragons are pulling in different directions. aggression without direction."
        },
        "Strength": {
            "upright": "Courage and compassion. Taming the beast within not with force, but with understanding. Inner fortitude.",
            "reversed": "Self-doubt or weakness. Letting fear control your actions. Raw emotion overpowering logic."
        },
        "The Wheel Of Fortune": {
            "upright": "Cycles and destiny. The great wheel turns; what is down will go up. Luck and karma are in motion.",
            "reversed": "Bad luck or resistance to change. Trying to stop the wheel. Breaking a cycle requires effort."
        },
        "The World": {
            "upright": "Completion and wholeness. The cycle is finished. You have gathered the ultimate hoard: wisdom.",
            "reversed": "Lack of closure. You are so close to the finish line but hesitating. Unfinished business."
        },
        "Judgement": {
            "upright": "Rebirth and calling. The Great Horn sounds. Shed your old scales and rise as something new. Absolution.",
            "reversed": "Self-doubt. Refusing the call. Holding onto past guilts that weigh you down."
        },
        "The Fool": {
            "upright": "New beginnings. A hatchling stepping off the ledge for the first time. Trust in your wings, even if you don't know how to fly yet.",
            "reversed": "Recklessness. Diving without looking. Naivety or foolish risks that could lead to a crash."
        },
        "The High Priestess": {
            "upright": "Hidden knowledge. The deep secrets of the Amethyst dragon. Trust your intuition and look beyond the veil of reality.",
            "reversed": "Secrets revealed or ignored. You are blocking your inner voice. Superficiality."
        },
        "The Emperor": {
            "upright": "Structure and authority. The Ancient Wyrm who establishes the laws of the territory. Stability, protection, and logic.",
            "reversed": "Rigidity. An abuse of power. A tyrant who controls with an iron claw. Lack of flexibility."
        },
        "The Hierophant": {
            "upright": "Tradition and mentorship. The Elder teaching the Draconic Prophecies. Conformity and spiritual guidance.",
            "reversed": "Rebellion. Breaking the ancient laws. Creating your own path outside of tradition."
        },
        "The Lovers": {
            "upright": "Union and choice. Two dragons spiraling in flight. A deep connection, harmony, or a critical decision about your values.",
            "reversed": "Disharmony. Misalignment of values. A bad choice or a broken bond."
        },
        "The Hermit": {
            "upright": "Introspection. Retreating to the deepest cavern to hibernate and reflect. Wisdom comes from solitude.",
            "reversed": "Isolation. Withdrawing too far. Loneliness or refusing to share your wisdom with the flight."
        },
        "Justice": {
            "upright": "Truth and law. The scales of the dragon are balanced. Cause and effect. You will get exactly what you deserve.",
            "reversed": "Unfairness. Dishonesty or avoiding accountability. The scales are tipped against you."
        },
        "The Hanged Man": {
            "upright": "Perspective. Suspended in a gravity field, upside down. Pause your action and look at the world differently. Sacrifice for wisdom.",
            "reversed": "Stalling. Unnecessary delay. You are hanging on for no reason. Fear of sacrifice."
        },
        "Death": {
            "upright": "Metamorphosis. Like a dragon shedding its skin to grow larger, you must let a part of your life end. A necessary transition.",
            "reversed": "Stagnation. You are clinging to the past. Refusing to let go of old scales or habits is preventing your rebirth."
        },
        "Temperance": {
            "upright": "Balance and alchemy. Mixing fire and ice to create steam. Patience and moderation are the keys to power.",
            "reversed": "Imbalance. Extremes. Volatility and lack of patience are causing the mixture to explode."
        },
        "The Devil": {
            "upright": "Addiction. The Dragon Sickness. Obsession with the hoard, greed, or material chains. You are trapped by your own desires.",
            "reversed": "Breaking free. Realizing the gold does not control you. Escaping a toxic situation."
        },
        "The Tower": {
            "upright": "Sudden change. The lair collapses. A shock to the system that destroys false structures. Hubris punished.",
            "reversed": "Averting disaster. You see the cracks in the ceiling and escape just in time. Or, fear of change."
        },
        "The Star": {
            "upright": "Hope and navigation. Flying by the constellations. Inspiration, renewal, and faith in the future.",
            "reversed": "Despair. Clouds block the stars. Feeling lost or disconnected from your purpose."
        },
        "The Moon": {
            "upright": "Illusion and fear. Shadows in the dark. Your psionics are confusing you. Things are not what they seem.",
            "reversed": "Clarity. The sun rises and dispels the shadows. Seeing through the deception."
        },
        "The Sun": {
            "upright": "Glory and vitality. Basking in the full light. Success, joy, and the power of a fully grown dragon.",
            "reversed": "Burnout. Too much heat. Or temporary sadness clouding your joy."
        }
        # Add the rest of your Majors here as you create them...
    }
}
# Setup bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def get_deck():
    """Scans the image folders to build the deck dynamically."""
    deck = []
    # Walk through the images directory
    for root, dirs, files in os.walk(IMAGE_DIR):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg', '.webp')):
                # Get the suit from the folder name (e.g., 'sapphires')
                suit_folder_name = os.path.basename(root).lower()
                
                # Get the rank from the filename (e.g., 'ace' from 'ace.png')
                rank = os.path.splitext(file)[0].replace('_', ' ').title()
                
                full_path = os.path.join(root, file)
                
                deck.append({
                    'suit_key': suit_folder_name, # used for looking up config
                    'rank': rank,
                    'path': full_path
                })
    return deck

@bot.event
async def on_ready():
    print(f'Dragon Tarot Bot connected as {bot.user}')
    print('---')
    print(f'Scanning {IMAGE_DIR}...')
    deck = get_deck()
    print(f'Found {len(deck)} cards.')
    print('Ready to read fates.')

@bot.command(name='draw')
async def draw_card(ctx, num_cards: int = 1):
    """Draws X cards with Gem Dragon lore. Usage: !draw"""
    deck = get_deck()
    
    if not deck:
        await ctx.send("No cards found!")
        return

    drawn_cards = random.sample(deck, min(num_cards, len(deck)))

    for card in drawn_cards:
        # 1. Basic Info
        suit_key = card['suit_key']   # e.g. 'rubies'
        rank_key = card['rank']       # e.g. 'Ace', 'King', 'The Magician'
        
        # 2. Get Generic Suit Data (Fallback)
        suit_data = SUIT_CONFIG.get(suit_key, {
            "element": "Unknown", "color": 0x000000
        })

        # 3. Determine Reversal
        is_reversed = random.choice([True, False])
        
        # 4. Fetch Specific Meaning from CARD_MEANINGS
        # We try to dig into: CARD_MEANINGS -> suit_key (Capitalized) -> rank_key -> 'upright'/'reversed'
        specific_meaning = "Meaning unclear. Consult the archives." # Default text
        
        try:
            # Note: We .title() the suit_key to match 'Rubies' in the dict
            deck_suit_data = CARD_MEANINGS.get(suit_key.title(), {}) 
            card_data = deck_suit_data.get(rank_key, {})
            
            if is_reversed:
                specific_meaning = card_data.get('reversed', "Reversed meaning hidden.")
            else:
                specific_meaning = card_data.get('upright', "Upright meaning hidden.")
        except Exception as e:
            print(f"Error fetching meaning: {e}")

        # 5. Formatting Display
        display_rank = rank_key
        if is_reversed:
            display_rank += " (Reversed)"
        
        # 6. Image Processing (Rotation)
        filename = os.path.basename(card['path'])
        
        if is_reversed:
            with Image.open(card['path']) as img:
                rotated_img = img.rotate(180)
                with io.BytesIO() as image_binary:
                    rotated_img.save(image_binary, 'PNG')
                    image_binary.seek(0)
                    file = discord.File(fp=image_binary, filename=filename)
                    
                    embed = discord.Embed(
                        title=f"{display_rank}",
                        description=f"*{specific_meaning}*\n\n**Suit:** {suit_key.title()} ({suit_data['element']})",
                        color=suit_data['color']
                    )
                    embed.set_image(url=f"attachment://{filename}")
                    await ctx.send(file=file, embed=embed)
        else:
            file = discord.File(card['path'], filename=filename)
            embed = discord.Embed(
                title=f"{display_rank}",
                description=f"*{specific_meaning}*\n\n**Suit:** {suit_key.title()} ({suit_data['element']})",
                color=suit_data['color']
            )
            embed.set_image(url=f"attachment://{filename}")
            await ctx.send(file=file, embed=embed)

# Run the bot
bot.run(TOKEN)