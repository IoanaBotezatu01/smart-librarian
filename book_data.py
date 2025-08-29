# book_data.py
from typing import Dict

book_summaries_dict: Dict[str, str] = {
    "To Kill a Mockingbird": (
        "Set in the racially charged American South during the 1930s, this coming-of-age story "
        "follows young Scout Finch as she navigates a world of prejudice and injustice. "
        "Through her father Atticus’s courageous defense of a black man falsely accused of assault, "
        "Scout learns profound lessons about empathy, moral integrity, and the complexities of human nature."
    ),
    "The Great Gatsby": (
        "In the glittering world of 1920s America, Jay Gatsby’s lavish parties and mysterious past captivate "
        "his neighbors and former lover Daisy Buchanan. As Gatsby pursues the elusive American Dream and "
        "rekindles his romance with Daisy, the novel exposes the emptiness beneath wealth, the illusions of love, "
        "and the moral decay of society."
    ),
    "Pride and Prejudice": (
        "Set in Regency England, this witty and insightful novel explores the intricate dance of manners, "
        "marriage, and social status. Elizabeth Bennet, known for her intelligence and independence, "
        "must navigate misunderstandings and pride as she gradually discovers the true character of Mr. Darcy, "
        "challenging societal expectations along the way."
    ),
    "Moby-Dick": (
        "An epic tale of obsession and revenge, the story follows Captain Ahab’s relentless pursuit of the legendary "
        "white whale, Moby Dick. As the crew of the Pequod faces perilous seas and existential questions, "
        "the novel delves into themes of fate, madness, and humanity’s struggle against the forces of nature."
    ),
    "The Catcher in the Rye": (
        "Narrated by disaffected teenager Holden Caulfield, this novel captures the angst and alienation of youth. "
        "Wandering New York City after being expelled from school, Holden grapples with the phoniness of adulthood, "
        "the pain of loss, and his desperate search for authenticity and meaning."
    ),
    "Brave New World": (
        "In a technologically advanced future, society is engineered for stability and pleasure at the cost of "
        "individuality and freedom. Citizens are conditioned to conform, relationships are superficial, "
        "and true happiness is elusive. As Bernard Marx and others begin to question the system, "
        "the novel explores the dangers of unchecked scientific progress and the loss of humanity."
    ),
    "Jane Eyre": (
        "Orphaned and mistreated, Jane Eyre grows into a resilient and principled young woman. "
        "As a governess at Thornfield Hall, she encounters love, betrayal, and moral dilemmas, "
        "ultimately forging her own path to independence and self-respect in a world that seeks to limit her choices."
    ),
    "Animal Farm": (
        "This satirical allegory depicts a group of farm animals who overthrow their human owner in pursuit of equality "
        "and freedom. However, as the pigs seize power, the revolution devolves into tyranny and corruption, "
        "mirroring the rise and fall of political ideals and the dangers of unchecked authority."
    ),
    "The Hobbit": (
        "Bilbo Baggins, a timid and comfort-loving hobbit, is swept into an epic quest alongside a band of dwarves "
        "to reclaim their homeland and treasure from the fearsome dragon Smaug. Along the journey, "
        "Bilbo discovers courage, resourcefulness, and the value of friendship in a richly imagined fantasy world."
    ),
    "Fahrenheit 451": (
        "In a dystopian future where books are outlawed and critical thought is suppressed, fireman Guy Montag’s job "
        "is to burn literature and maintain conformity. As he encounters free thinkers and forbidden ideas, "
        "Montag begins to question the oppressive regime, embarking on a dangerous journey toward enlightenment and resistance."
    ),
    "1984": (
        "A dystopian society dominated by surveillance and propaganda. Winston Smith struggles to preserve "
        "his individuality and truth under a totalitarian regime. The novel is a chilling reflection on freedom, "
        "social control, and manipulation."
    ),
    "Harry Potter and the Sorcerer's Stone": (
        "Harry, an orphaned boy, discovers that he is a wizard and attends Hogwarts School of Witchcraft and Wizardry. "
        "There he forms lifelong friendships and faces the first signs of Voldemort’s return. "
        "The story introduces a magical world full of wonder while exploring themes of courage, choice, and friendship."
    ),
    "The Alchemist": (
        "Santiago, a young shepherd, dreams of finding treasure near the Egyptian pyramids. "
        "On his journey he meets characters who teach him to listen to the omens of the world and to trust his heart. "
        "The novel is a parable about following your dreams and embracing the journey."
    ),
    "Dune": (
        "On the desert planet Arrakis, Paul Atreides is thrust into a world of betrayal, prophecy, and ecological struggle. "
        "As rival factions vie for control of the spice, Paul must embrace his destiny as a possible messianic leader, "
        "balancing survival with the fate of civilizations."
    ),
    "The Little Prince": (
        "Through encounters on different planets, the Little Prince reflects on love, friendship, and the meaning of life. "
        "The story reminds adults that what is essential is invisible to the eye, offering a timeless meditation on innocence and responsibility."
    ),
    "The Book Thief": (
        "Narrated by Death, the story follows Liesel Meminger, a young girl in Nazi Germany who finds solace in stealing books "
        "and sharing them with others. Amidst the horrors of war, the novel explores the power of words, compassion, and resilience."
    ),
    "The Kite Runner": (
        "Amir and Hassan grow up together in Kabul, but a betrayal shatters their friendship. "
        "Years later, amid a war-torn Afghanistan, Amir seeks redemption for his past mistakes, "
        "making this a story of guilt, forgiveness, and redemption."
    ),
    "All the Light We Cannot See": (
        "Marie-Laure, a blind French girl, and Werner, a German boy fascinated by radios, experience World War II on parallel paths. "
        "Their stories converge in occupied France, offering a moving tale of resilience, humanity, and the light that guides us through darkness."
    ),
    "The Name of the Wind": (
        "Kvothe, a gifted musician and magician, recounts his extraordinary life story—from childhood in a troupe of performers "
        "to his time at the University—while seeking answers about the mysterious Chandrian. "
        "It is a tale of knowledge, identity, and the pursuit of greatness."
    ),
    "The Lord of the Rings: The Fellowship of the Ring": (
        "Frodo Baggins inherits the One Ring and sets out with a Fellowship to destroy it in the fires of Mount Doom. "
        "Along the way, the companions face trials of friendship, sacrifice, and courage against overwhelming darkness."
    ),
}

def get_summary_by_title(title: str) -> str:
    """Return the full summary for an exact title match, or an empty string if not found."""
    return book_summaries_dict.get(title, "")

def search_summaries_by_keyword(keyword: str) -> Dict[str, str]:
    """Return a dictionary of titles and summaries that contain the given keyword (case-insensitive)."""
    keyword_lower = keyword.lower()
    return {title: summary for title, summary in book_summaries_dict.items() if keyword_lower in summary.lower()}