
Action: file_editor create /app/frontend/src/data/tips.js --file-text "// Daily rotating motivational tips written for 6th graders who are struggling.
// Warm, specific, no clichés like \"just believe\".

export const TIPS = [
  {
    quote:
      \"Getting stuck isn't a stop sign — it's the moment right before you learn something.\",
    tip: \"When your brain feels foggy, try teaching the problem out loud to a stuffed animal. Sounds silly, works magic.\",
    tag: \"Grit\",
  },
  {
    quote:
      \"You don't have to be smart. You have to be curious. Smart shows up on the way.\",
    tip: \"Today, pick ONE question you're afraid to ask. Ask it. You'll be surprised how many kids had the same one.\",
    tag: \"Curiosity\",
  },
  {
    quote: \"Small brave steps beat one giant scary leap.\",
    tip: \"Set a 10-minute timer. Do ONE tiny piece of homework. When it dings, stretch. Then decide if you want another 10.\",
    tag: \"Focus\",
  },
  {
    quote: \"Mistakes are your brain doing push-ups.\",
    tip: \"Redo one problem you got wrong last week — from memory. Your brain will thank you (with better grades).\",
    tag: \"Growth\",
  },
  {
    quote: \"Reading 10 minutes a day is like giving your brain a snack.\",
    tip: \"Read anything you love — comics, cereal boxes, story apps. Words are words. All of them make you smarter.\",
    tag: \"Reading\",
  },
  {
    quote:
      \"It's okay to not be a 'math person' yet. Yet is the most important word.\",
    tip: \"Draw the problem. Fractions become pizza slices. Decimals become dollars and cents.\",
    tag: \"Math\",
  },
  {
    quote: \"You are not behind. You are exactly where your practice has taken you.\",
    tip: \"Pick one topic today. Practice it 3 different ways: read it, say it, doodle it.\",
    tag: \"You've got this\",
  },
];

export const getTodayTip = () => {
  const day = Math.floor(Date.now() / (1000 * 60 * 60 * 24));
  return TIPS[day % TIPS.length];
};
"
Observation: Create successful: /app/frontend/src/data/tips.js
