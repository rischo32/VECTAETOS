// VORTEX — Simple deterministic language detector

export function detectLanguage(text) {

  const lower = text.toLowerCase();

  const slovakMarkers = [
    "čo", "prečo", "ako", "kto", "kedy",
    "preto", "ktorý", "ktorá", "ktoré",
    "nie", "áno", "je", "som", "si",
    "že", "by", "sa", "tvoj", "tvoja"
  ];

  const englishMarkers = [
    "what", "why", "how", "who", "when",
    "this", "that", "is", "are", "you",
    "your", "would", "could", "should"
  ];

  let skScore = 0;
  let enScore = 0;

  // diakritika = silný signál SK
  if (/[áäčďéíĺľňóôŕšťúýž]/.test(lower)) {
    skScore += 2;
  }

  slovakMarkers.forEach(word => {
    if (lower.includes(word)) skScore++;
  });

  englishMarkers.forEach(word => {
    if (lower.includes(word)) enScore++;
  });

  return skScore >= enScore ? "sk" : "en";
}
