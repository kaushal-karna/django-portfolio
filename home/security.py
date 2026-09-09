import re

# ==============================================================================
# 1. STRICT EMAIL VALIDATION
# ==============================================================================

def is_valid_email(email: str, only_gmail: bool = True) -> tuple[bool, str]:
    """
    Validates whether the email is a genuine address.
    If only_gmail=True, requires a valid @gmail.com address.
    """
    if not email or len(email) > 254:
        return False, "Please enter a valid email address."

    email = email.strip().lower()

    # Standard email structure regex
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return False, "Please enter a properly formatted email address."

    username, domain = email.split('@', 1)

    # Gmail specific validation
    if only_gmail:
        if domain != 'gmail.com':
            return False, "Please provide a valid Gmail address (@gmail.com)."
        
        # Google requires Gmail usernames to be between 6 and 30 characters
        if len(username) < 6 or len(username) > 30:
            return False, "Gmail username must be between 6 and 30 characters."

        # Gmail only allows alphanumeric characters and periods
        if not re.match(r'^[a-zA-Z0-9.]+$', username):
            return False, "Please enter a valid Gmail address without special symbols."

        # Catch obvious repeated key-smash emails (e.g. asdfasdf@gmail.com, aaaaaa@gmail.com)
        if re.match(r'^(.)\1+$', username) or username in ['test123', 'asdfgh', 'qwerty', '123456']:
            return False, "Please provide your genuine email address, not a dummy or test email."
    else:
        # Check against common temporary/disposable email domains
        disposable_domains = [
            'mailinator.com', 'tempmail.com', '10minutemail.com', 'guerrillamail.com',
            'throwawaymail.com', 'yopmail.com', 'trashmail.com'
        ]
        if domain in disposable_domains:
            return False, "Temporary and disposable email addresses are not allowed."

    return True, ""


# ==============================================================================
# 2. MULTILINGUAL PROFANITY FILTER (English, Hindi, Nepali, Maithili)
# ==============================================================================

OFFENSIVE_WORDS = {
    # --- English ---
    'fuck', 'fucking', 'fucker', 'shit', 'bitch', 'asshole', 'bastard', 
    'dick', 'pussy', 'cunt', 'slut', 'whore', 'idiot', 'moron', 'nigger', 
    'nigga', 'faggot', 'dumbass', 'retard',

    # --- Nepali / Romanized Nepali ---
    'muji', 'machikne', 'chikne', 'chikna', 'lado', 'puti', 'bhalu', 
    'radi', 'randi', 'khate', 'dhoti', 'geda', 'chateko', 'kukur',

    # --- Hindi / Romanized Hindi ---
    'chutiya', 'chutiye', 'chut', 'madarchod', 'bhenchod', 'behenchod', 
    'bhosdike', 'bhosadike', 'gaand', 'gand', 'harami', 'haramee', 
    'lauda', 'laude', 'loda', 'lode', 'tatte', 'suar', 'saale', 'kamina', 
    'chodd', 'chodna', 'bhadwa', 'bhadve', 'bhadua', 'chodu',

    # --- Maithili ---
    'choda', 'chodi', 'bhondu', 'bokwa', 'chhati', 'badmash', 'beshya',
    'lounda', 'loundi', 'raand',

    # --- Devanagari Script (नेपाली, हिन्दी, मैथिली) ---
    'मुजी', 'माचिक्ने', 'चिक्ने', 'लाडो', 'पुती', 'भालु', 'रांडी', 'खाते',
    'मादरचोद', 'बहनचोद', 'भोसडीके', 'गांड', 'चुतिया', 'हरामी', 'लौडा', 
    'लोडा', 'कुकुर', 'साले', 'कमीना', 'भाडुआ', 'रंडी', 'झांट'
}


def contains_profanity(text: str) -> bool:
    """
    Detects vulgar, offensive, and abusive language in English, Hindi, Nepali, and Maithili.
    Handles obfuscations like 'f*u*c*k', 'm u j i', or '@' for 'a'.
    """
    if not text:
        return False

    # 1. Normalize characters (leetspeak conversion)
    normalized = text.lower()
    substitutions = {
        '@': 'a', '$': 's', '0': 'o', '1': 'i', '!': 'i', '3': 'e', '*': ''
    }
    for char, replacement in substitutions.items():
        normalized = normalized.replace(char, replacement)

    # 2. Check tokenized words
    words = re.findall(r'\b\w+\b', normalized)
    for word in words:
        if word in OFFENSIVE_WORDS:
            return True

    # 3. Check spaced-out words (e.g., "m u j i" -> "muji")
    spaceless = re.sub(r'\s+', '', normalized)
    for bad_word in OFFENSIVE_WORDS:
        # Only check words >= 4 characters to prevent false positives on substrings
        if len(bad_word) >= 4 and bad_word in spaceless:
            return True

    return False




