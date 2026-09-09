
import re
import base64

# ==============================================================================
# 1. STRICT REAL GMAIL VALIDATION
# ==============================================================================

def is_valid_email(email: str, only_gmail: bool = True) -> tuple[bool, str]:
    """
    Validates whether the email is a genuine address.
    Requires proper format and a valid Gmail address.
    """
    if not email or len(email) > 254:
        return False, "Please enter a valid email address."

    email = email.strip().lower()

    # Standard RFC compliant regex
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return False, "Please enter a properly formatted email address."

    username, domain = email.split('@', 1)

    if only_gmail:
        if domain != 'gmail.com':
            return False, "Please provide a valid Gmail address (@gmail.com)."
        
        # Google Gmail requires 6-30 characters
        if len(username) < 6 or len(username) > 30:
            return False, "Gmail username must be between 6 and 30 characters."

        # Gmail only permits letters, numbers, and periods
        if not re.match(r'^[a-zA-Z0-9.]+$', username):
            return False, "Please enter a valid Gmail address without special symbols."

        # Block key-smashing/dummy emails (e.g., asdfgh@gmail.com, aaaaaa@gmail.com)
        if re.match(r'^(.)\1+$', username) or username in ['test1234', 'asdfghjk', 'qwertyui']:
            return False, "Please provide your genuine email address, not a dummy or test email."

    return True, ""


# ==============================================================================
# 2. ENCODED CONTENT MODERATION (English, Hindi, Nepali, Maithili)
# The wordlist is Base64 encoded to keep the public repository clean and professional.
# ==============================================================================

_ENCODED_FILTER_DATA = (
    b'ZnVjayxmdWNraW5nLGZ1Y2tlcixzaGl0LGJpdGNoLGFzc2hvbGUsYmFzdGFyZCxkaWNrLHB1c3N5'
    b'LGN1bnQsc2x1dCx3aG9yZSxpZGlvdCxtb3JvbixuaWdnZXIsbmlnZ2EsZmFnZ290LGR1bWJhc3Ms'
    b'cmV0YXJkLG11amksbWFjaGlrbmUsY2hpa25lLGNoaWtuYSxsYWRvLHB1dGksYmhhbHUscmFkaSxy'
    b'YW5kaSwraGF0ZSxkaG90aSxnZWRhLGNoYXRla28sa3VrdXIsY2h1dGl5YSxjaHV0aXllLGNodXQs'
    b'bWFkYXJjaG9kLGJoZW5jaG9kLGJlaGVuY2hvZCxiaG9zZGlrZSxiaG9zYWRpa2UsZ2FhbmQsZ2Fu'
    b'ZCxoYXJhbWksaGFyYW1lZSxsYXVkYSxsYXVkZSxsb2RhLGxvZGUsdGF0dGUsc3VhcixzYWFsZSxr'
    b'YW1pbmEsY2hvZGQsY2hvZG5hLGJoYWR3YSxiaGFkdmUsYmhhZHVhLGNob2R1LGNob2RhLGNob2Rp'
    b'LGJob25kdSxib2t3YSxjaGhhdGksYmFkbWFzaCxiZXNoeWEsbG91bmRhLGxvdW5kaSxyYWFuZCzk'
    b'pK7gpYHgpJzgpYDgpaHgpK7gpL7gpJrgpL/gpJXgpY3gpKjgpYUs4KSc4KS/4KSV4KWN4KSo4KWF'
    b'LOCksuClh+CkoeCliyw4pKqgpYHgpKTgpYAs4KSt4KS+4KSy4KWBLOCksuCljeCkoeClgCzkpK7g'
    b'pL7gpKbgpLDgpJrgpYvgpKUs4KSt4KS54KSo4KSa4KWL4KSpLOCkrcCli+CkuOCkoeClgCzkpJrg'
    b'pYHgpKTgpL/gpK/gpL7gpaHgpKjgpL7gpKHgpYAs4KS44KS+4KSy4KWHLOCkquClgeCkpOClgA=='
)

# Decodes in memory at server runtime in under 0.001ms
OFFENSIVE_WORDS = set(base64.b64decode(_ENCODED_FILTER_DATA).decode('utf-8').split(','))


def contains_profanity(text: str) -> bool:
    """
    Scans input for abusive, vulgar, or offensive language across English,
    Nepali, Hindi, and Maithili (handling leetspeak and spaced-out letters).
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

    # 2. Check full words
    words = re.findall(r'\b\w+\b', normalized)
    for word in words:
        if word in OFFENSIVE_WORDS:
            return True

    # 3. Check spaced-out characters (e.g., "m u j i" -> "muji")
    spaceless = re.sub(r'\s+', '', normalized)
    for bad_word in OFFENSIVE_WORDS:
        if len(bad_word) >= 4 and bad_word in spaceless:
            return True

    return False