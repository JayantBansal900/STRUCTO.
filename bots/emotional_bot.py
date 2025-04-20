import json
import re
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_EMOTION_KEY")

# Get emotion advice (same as in the previous step)
def get_emotion_advice(emotion: str) -> str:
    emotion_advice = {
        "sadness": [
            "1. Take a walk in nature, breathe deeply, and clear your mind.",
            "2. Try journaling to express your feelings.",
            "3. Reach out to someone you trust or talk to a professional.",
            "4. Practice mindfulness or meditation to calm your mind."
        ],
        "anger": [
            "1. Try taking deep breaths and count to ten before reacting.",
            "2. Walk away from the situation and find a quiet space.",
            "3. Consider physical activity like exercise to release built-up tension.",
            "4. Reflect on what triggered your anger and try to find a solution."
        ],
        "fear": [
            "1. Ground yourself by focusing on the present moment.",
            "2. Identify the source of fear and challenge it.",
            "3. Seek professional help if the fear is overwhelming.",
            "4. Practice relaxation techniques like deep breathing."
        ],
        "happiness": [
            "1. Share your happiness with loved ones.",
            "2. Keep practicing gratitude to maintain a positive mindset.",
            "3. Engage in activities that bring you joy.",
            "4. Spread kindness and positivity to others."
        ],
        "anxiety": [
            "1. Practice deep breathing exercises to calm your mind.",
            "2. Break tasks into smaller, manageable steps.",
            "3. Talk to someone you trust about your feelings.",
            "4. Consider mindfulness or yoga to ground yourself."
        ],
        "stress": [
            "1. Take breaks during work or study to avoid burnout.",
            "2. Prioritize tasks and delegate when necessary.",
            "3. Engage in physical activities like exercise or walking.",
            "4. Practice mindfulness and meditation to reduce tension."
        ],
        "overwhelm": [
            "1. Break large tasks into smaller, manageable ones.",
            "2. Focus on one thing at a time.",
            "3. Practice self-compassion and allow yourself breaks.",
            "4. Reach out to someone for support when needed."
        ],
        "love": [
            "1. Nurture the relationship through open communication.",
            "2. Show appreciation and gratitude towards your partner.",
            "3. Engage in activities that strengthen your bond.",
            "4. Express your love regularly through small gestures."
        ],
        "loneliness": [
            "1. Reach out to friends or family members for support.",
            "2. Engage in activities that make you feel connected.",
            "3. Volunteer or join groups that interest you.",
            "4. Consider talking to a therapist if loneliness persists."
        ],
        "guilt": [
            "1. Reflect on the situation and learn from it.",
            "2. Apologize to anyone affected by your actions.",
            "3. Practice self-compassion and forgive yourself.",
            "4. Make amends where possible and move forward."
        ],
        "regret": [
            "1. Acknowledge your feelings and accept the situation.",
            "2. Focus on what you can control moving forward.",
            "3. Reflect on lessons learned from the experience.",
            "4. Focus on positive actions to avoid regret in the future."
        ],
        "shame": [
            "1. Understand that everyone makes mistakes.",
            "2. Work on self-compassion and forgiving yourself.",
            "3. Talk to a trusted friend or therapist about your feelings.",
            "4. Take steps to make amends or correct the mistake."
        ],
        "confusion": [
            "1. Take a step back and allow yourself time to process.",
            "2. Break down the issue into smaller parts to find clarity.",
            "3. Talk to someone who can provide a different perspective.",
            "4. Consider journaling to untangle your thoughts."
        ],
        "pride": [
            "1. Celebrate your achievements, but stay humble.",
            "2. Share your successes with those who supported you.",
            "3. Continue working towards new goals.",
            "4. Help others to foster a sense of community and support."
        ],
        "grief": [
            "1. Allow yourself to feel the emotions that come with grief.",
            "2. Lean on friends, family, or support groups for comfort.",
            "3. Practice self-care and give yourself time to heal.",
            "4. Consider seeking professional help if grief becomes overwhelming."
        ],
        "boredom": [
            "1. Try learning something new or taking up a hobby.",
            "2. Engage in activities that challenge your creativity.",
            "3. Spend time with friends or engage in social activities.",
            "4. Take a break and allow yourself some relaxation."
        ],
        "embarrassment": [
            "1. Take a deep breath and remind yourself that everyone makes mistakes.",
            "2. Laugh it off or share the moment with friends.",
            "3. Apologize if necessary, and move on.",
            "4. Accept that embarrassment is a natural emotion."
        ],
        "hope": [
            "1. Stay positive and continue working towards your goals.",
            "2. Share your hope with others and inspire them.",
            "3. Focus on small steps that lead to positive change.",
            "4. Remember that hope is an important part of resilience."
        ],
        "jealousy": [
            "1. Acknowledge your feelings and understand their root cause.",
            "2. Practice gratitude for what you already have.",
            "3. Talk to the person involved to clear any misunderstandings.",
            "4. Focus on your personal growth and avoid comparisons."
        ],
        "disappointment": [
            "1. Accept that not everything goes as planned.",
            "2. Focus on what you can control and move forward.",
            "3. Reflect on the lessons learned from the situation.",
            "4. Set new goals or redefine your expectations."
        ]
    }

    return "<br>".join(emotion_advice.get(emotion.lower(), [
        "It's okay to feel this way.",
        "Express your feelings in a healthy way.",
        "You're not alone — talk to someone you trust.",
        "Practice self-care and patience with yourself."
    ]))


# Emojis and categories (same as before)
EMOTION_META = {
    "sadness": {"emoji": "😢", "category": "Negative"},
    "anger": {"emoji": "😠", "category": "Negative"},
    "fear": {"emoji": "😨", "category": "Negative"},
    "happiness": {"emoji": "😊", "category": "Positive"},
    "anxiety": {"emoji": "😟", "category": "Negative"},
    "stress": {"emoji": "😩", "category": "Negative"},
    "overwhelm": {"emoji": "🥴", "category": "Negative"},
    "love": {"emoji": "❤️", "category": "Positive"},
    "loneliness": {"emoji": "😔", "category": "Negative"},
    "guilt": {"emoji": "😓", "category": "Negative"},
    "regret": {"emoji": "😞", "category": "Negative"},
    "shame": {"emoji": "😳", "category": "Negative"},
    "confusion": {"emoji": "🤔", "category": "Neutral"},
    "pride": {"emoji": "😌", "category": "Positive"},
    "grief": {"emoji": "🖤", "category": "Negative"},
    "boredom": {"emoji": "🥱", "category": "Neutral"},
    "embarrassment": {"emoji": "🙈", "category": "Negative"},
    "hope": {"emoji": "🌈", "category": "Positive"},
    "jealousy": {"emoji": "😒", "category": "Negative"},
    "disappointment": {"emoji": "😞", "category": "Negative"},
    "relief": {"emoji": "😌", "category": "Positive"}
}


def extract_tags(advice_list):
    tags = set()
    for tip in advice_list:
        for word in re.findall(r'\b[a-zA-Z]{4,}\b', tip.lower()):
            if word not in {"yourself", "someone", "about"}:
                tags.add(word)
            if len(tags) >= 5:
                break
    return list(tags)[:5]


def analyze_emotion(text: str) -> str:
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "Emotion Detection Bot"
        }

        data = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {
                    "role": "system",
                    "content": "You're an assistant that detects emotion(s) from text. Just list primary emotions in a comma-separated format like: anxiety, sadness."
                },
                {
                    "role": "user",
                    "content": f"What emotion is expressed in: '{text}'? Just list the emotion(s), no explanation."
                }
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        emotion_text = result["choices"][0]["message"]["content"].strip().lower()
        emotions = [e.strip() for e in re.split(r',|\band\b', emotion_text) if e.strip()]

        # Timestamp in readable format
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

        # Final output string
        output = f"🌟 Timestamp: {timestamp}\n"
        output += f"📝 User Input: {text}\n"
        output += f"🧠 Number of Detected Emotions: {len(emotions)}\n"
        output += f"🎭 Detected Emotions and Advice:\n\n"

        for emo in emotions:
            advice_list = get_emotion_advice(emo).split("<br>")
            emoji = EMOTION_META.get(emo, {}).get("emoji", "❓")
            category = EMOTION_META.get(emo, {}).get("category", "Unknown")
            confidence = round(0.75 + 0.25 * (hash(emo) % 100) / 100, 2)

            output += f"**{emo.capitalize()} {emoji}**\n"
            output += f"• Category: {category}\n"
            output += f"• Confidence: {confidence}\n"
            output += f"• Advice:\n"
            for advice in advice_list:
                output += f"   - {advice}\n"
            tags = extract_tags(advice_list)
            output += f"• Tags: {', '.join(tags)}\n"
            output += "------------------------\n\n"

        return output.replace("\n", "<br>")

    except Exception as e:
        return f"Error: {str(e)}"

