"""Catalogue content for The Sunday Kitchen."""

INSTRUCTORS = [
    {
        "id": "pranathi",
        "name": "Pranathi Chaliseemala",
        "role": "Pasta & pastry guide",
        "bio": (
            "Pranathi brings a patient, hands-on approach to dough, pastry and "
            "the small details that make a recipe feel approachable."
        ),
        "image": "images/instructors/pranathi.jpg",
        "alt": "Portrait of Pranathi Chaliseemala seated at a table",
        "position": "center",
    },
    {
        "id": "prakruti",
        "name": "Prakruti B",
        "role": "Bread & fermentation guide",
        "bio": (
            "Prakruti helps learners slow down, observe their dough and build "
            "confidence through repeatable kitchen rhythms."
        ),
        "image": "images/instructors/prakruti.jpg",
        "alt": "Portrait of Prakruti B wearing a colourful hat",
        "position": "center",
    },
    {
        "id": "amrutha",
        "name": "Amrutha Gowda",
        "role": "Seasonal cooking guide",
        "bio": (
            "Amrutha keeps the focus on flavour, seasonality and practical "
            "techniques that make everyday cooking feel generous."
        ),
        "image": "images/instructors/amrutha-upright.jpg",
        "alt": "Portrait of Amrutha Gowda standing in front of a warm golden backdrop",
        "position": "center top",
    },
]

INSTRUCTOR_BY_ID = {person["id"]: person for person in INSTRUCTORS}

WORKSHOPS = [
    {
        "slug": "handmade-pasta", "title": "Pasta, by hand", "eyebrow": "A little flour, a little patience",
        "description": "Roll, shape and fill fresh pasta with the kind of care that makes an ordinary supper feel like an occasion.",
        "long_description": "A hands-on class in fresh pasta dough, classic shapes and a simple seasonal sauce. Work from the first mound of flour to a plate worth lingering over. No machine or prior experience needed.",
        "level": "Beginner friendly", "duration": "3 hours", "price": "₹2,200",
        "image": "images/workshops/handmade-pasta.jpg", "alt": "Fresh pasta being prepared on a wooden counter",
        "skills": ["Mix and rest pasta dough", "Roll and shape by hand", "Make a seasonal pan sauce", "Cook and season pasta properly"],
        "ingredients": ["Flour", "Eggs and olive oil", "Seasonal herbs", "Market vegetables"],
        "schedule": [("10:00 am", "Coffee, introductions and ingredients"), ("10:20 am", "Dough-making demonstration and practice"), ("11:10 am", "Rolling, shaping and sauce preparation"), ("12:30 pm", "Cook, plate and share the table")],
        "sessions": [("pasta-2026-11-07", "Saturday, 7 November 2026 · 10:00 am"), ("pasta-2026-11-21", "Saturday, 21 November 2026 · 10:00 am")],
        "instructor_id": "pranathi",
    },
    {
        "slug": "sourdough-sunday", "title": "The slow art of sourdough", "eyebrow": "Good bread takes its time",
        "description": "Meet your starter, learn to read your dough and understand the rhythm behind a crusty loaf.",
        "long_description": "A practical introduction to starter health, fermentation cues, shaping and scoring. Handle dough at different stages and take home a clear practice process. Fermentation timing varies with temperature and starter activity.",
        "level": "Beginner friendly", "duration": "3.5 hours", "price": "₹2,500",
        "image": "images/workshops/sourdough-sunday.jpg", "alt": "Three rustic sourdough loaves on a flour-dusted counter",
        "skills": ["Understand starter activity", "Read fermentation cues", "Practise shaping", "Learn scoring and baking basics"],
        "ingredients": ["Wheat flour", "Water and active starter", "Salt", "Rice flour"],
        "schedule": [("9:30 am", "Starter check-in and flour talk"), ("10:00 am", "Mixing, folding and dough handling"), ("11:30 am", "Shaping and scoring practice"), ("12:15 pm", "Bake review and troubleshooting")],
        "sessions": [("bread-2026-11-08", "Sunday, 8 November 2026 · 9:30 am"), ("bread-2026-11-22", "Sunday, 22 November 2026 · 9:30 am")],
        "instructor_id": "prakruti",
    },
    {
        "slug": "little-patisserie", "title": "A little patisserie", "eyebrow": "Precision, patience, pastry",
        "description": "Practise crisp tart shells, silky fillings and finishing touches that make pastry feel special.",
        "long_description": "A guided patisserie session for curious bakers. Learn the logic behind shortcrust pastry, pastry cream and balanced decoration, with time to practise and ask questions.",
        "level": "Some baking experience helpful", "duration": "4 hours", "price": "₹2,800",
        "image": "images/workshops/little-patisserie.jpg", "alt": "Delicate pastry finished with berries",
        "skills": ["Make and line tart shells", "Prepare smooth pastry cream", "Understand setting and cooling", "Finish with fruit and texture"],
        "ingredients": ["Flour and butter", "Eggs and cream", "Vanilla", "Seasonal berries"],
        "schedule": [("10:00 am", "Pastry principles and mise en place"), ("10:30 am", "Mixing, resting and lining shells"), ("12:00 pm", "Pastry cream and filling"), ("1:00 pm", "Finishing and troubleshooting")],
        "sessions": [("pastry-2026-11-14", "Saturday, 14 November 2026 · 10:00 am"), ("pastry-2026-12-05", "Saturday, 5 December 2026 · 10:00 am")],
        "instructor_id": "pranathi",
    },
    {
        "slug": "regional-indian-table", "title": "The regional Indian table", "eyebrow": "Many kitchens, many stories",
        "description": "Explore a regional menu through spice balance, seasonal produce and useful techniques.",
        "long_description": "A technique-led class focused on a rotating regional menu per session. The class centres on tasting, balance and practical methods.",
        "level": "All levels", "duration": "3 hours", "price": "₹1,900",
        "image": "images/workshops/regional-indian-table.jpg", "alt": "A colourful table of food and fresh garnishes",
        "skills": ["Bloom and layer spices", "Balance salt, acidity and heat", "Build flavour with aromatics", "Plan a balanced menu"],
        "ingredients": ["Seasonal vegetables and pulses", "Whole and ground spices", "Fresh herbs", "Rice or regional grains"],
        "schedule": [("11:00 am", "Regional context and tasting notes"), ("11:20 am", "Spice and aromatics demonstration"), ("12:00 pm", "Small-group cooking practice"), ("1:15 pm", "Shared tasting and recap")],
        "sessions": [("indian-2026-11-15", "Sunday, 15 November 2026 · 11:00 am"), ("indian-2026-11-29", "Sunday, 29 November 2026 · 11:00 am")],
        "instructor_id": "amrutha",
    },
    {
        "slug": "seasonal-market-cooking", "title": "Cook with the season", "eyebrow": "Let the market lead",
        "description": "Build a flexible menu around produce at its best, with simple techniques that make ingredients shine.",
        "long_description": "A produce-first workshop on choosing ingredients, reducing waste and building a menu that changes with the market.",
        "level": "All levels", "duration": "2.5 hours", "price": "₹1,800",
        "image": "images/workshops/seasonal-market-cooking.jpg", "alt": "Fresh seasonal vegetables and greens",
        "skills": ["Choose and store fresh produce", "Build flavour with texture and acidity", "Plan a flexible menu", "Reduce avoidable kitchen waste"],
        "ingredients": ["Market vegetables", "Fresh herbs and citrus", "Grains or legumes", "Pantry staples"],
        "schedule": [("10:30 am", "Produce introductions and menu planning"), ("11:00 am", "Knife skills and flavour-building"), ("12:00 pm", "Cook, taste and adapt"), ("12:45 pm", "Storage notes and questions")],
        "sessions": [("season-2026-11-28", "Saturday, 28 November 2026 · 10:30 am"), ("season-2026-12-12", "Saturday, 12 December 2026 · 10:30 am")],
        "instructor_id": "amrutha",
    },
]

for workshop in WORKSHOPS:
    workshop["instructor"] = INSTRUCTOR_BY_ID[workshop["instructor_id"]]

COURSES = [
    {"slug": "cooking-foundations", "title": "Cooking foundations", "eyebrow": "Start with the essentials", "description": "Build confidence with knife skills, heat, seasoning, mise en place and repeatable weeknight methods.", "sessions": "6 sessions", "duration": "3 weeks", "level": "No experience needed", "price": "₹8,500", "outcomes": ["Safer, more consistent knife technique", "Understanding heat and pan control", "Seasoning and balancing flavour", "Planning and executing a simple menu"]},
    {"slug": "baking-fundamentals", "title": "Baking fundamentals", "eyebrow": "Learn the why, not just the recipe", "description": "Understand measurements, mixing methods, oven behaviour and how to troubleshoot everyday bakes.", "sessions": "5 sessions", "duration": "5 weeks", "level": "Beginner friendly", "price": "₹7,500", "outcomes": ["Accurate weighing and mise en place", "Creaming, folding and mixing methods", "Reading doneness cues", "Diagnosing common baking problems"]},
    {"slug": "artisan-skills-lab", "title": "The artisan skills lab", "eyebrow": "A deeper dive", "description": "A focused programme for learners ready to work on fermentation, dough, pastry and more precise technique.", "sessions": "8 sessions", "duration": "8 weeks", "level": "Some kitchen experience", "price": "₹14,000", "outcomes": ["Work with fermentation and resting times", "Dough handling and shaping", "Pastry texture and temperature control", "Plan practice and review results"]},
]

JOURNAL = [
    {"title": "A table, still warm", "category": "From the studio", "image": "https://images.unsplash.com/photo-1556911220-bff31c812dba?auto=format&fit=crop&w=1000&q=85", "alt": "Sunlit kitchen worktop prepared for a class"},
    {"title": "The lovely mess of making", "category": "Workshop notes", "image": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=1000&q=85", "alt": "Hands working at a flour-dusted counter"},
    {"title": "Fruit, cream, repeat", "category": "Seasonal inspiration", "image": "https://images.unsplash.com/photo-1464349095431-e9a21285b5f3?auto=format&fit=crop&w=1000&q=85", "alt": "A berry-topped cake"},
    {"title": "A loaf with a little patience", "category": "Baking diary", "image": "https://images.unsplash.com/photo-1589367920969-ab8e050bbb04?auto=format&fit=crop&w=1000&q=85", "alt": "Freshly baked crusty bread"},
]
