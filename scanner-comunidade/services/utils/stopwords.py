STOPWORDS = set(map(str.lower, {
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
    "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
    "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
    "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
    "when", "make", "can", "like", "time", "no", "just", "him", "know", "take",
    "people", "into", "year", "your", "good", "some", "could", "them", "see", "other",
    "than", "then", "now", "look", "only", "come", "its", "over", "think", "also",
    # Adicionadas para português e expressões comuns
    "de", "quem", "para", "mais", "com", "que", "um", "uma", "os", "as", "dos", "das", "na", "no", "nas", "nos", "ao", "aos", "às", "à", "por", "se", "em", "é", "ser", "foi", "são", "tem", "há", "vai", "fui", "tive", "está", "estão", "estava", "estavam", "pra", "pro", "pelo", "pela", "pelos", "pelas", "para mais", "com mais", "de mais", "por mais", "em mais"
})) 