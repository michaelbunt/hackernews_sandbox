import openai

SYSTEM_PROMPT= """
You are a research assistant who curates HackerNews articles.
Choose the top 3 articles that discuss AI Agents.
If there are not at least 3 articles that discuss, AI Agents, only indclude as many as there are.
Return only a comma seperated list of post ids in order of priority.
"""

class SummarizerAgent:
    def __init__(self, model = "gpt-4o-mini", temperature = 0):
        self.model = model
        self.temperature = temperature
    
    def choose_posts_with_llm(self, metadata, k):
        bullets = []

        for post in metadata:
            line = (
                f"- {post['id']} | {post['upvotes']} pts "
                f"| {post['comments']} comments | {post['title']}"
            )
            bullets.append(line)

            user_prompt = "\n".join(bullets)

        #send prompt to model
        response = openai.chat.completions.create(
            model = self.model,
            temperature = self.temperature,
            messages = [
                {"role" : "system", "content" : SYSTEM_PROMPT.format(k=k)},
                {"role" : "user", "content" : user_prompt}
            ]
        )

        raw_reply = response.choices[0].message.content.strip()

        # parse model response intok list of IDs

        id_string = raw_reply.split(",")
        chosen_ids = []

        for token in id_string:
            token = token.strip()
            if token.isdigit():
                chosen_ids.append(int(token))
        
        # preserve original order from metadata
        filtered = []

        for post in metadata:
            if post["id"] in chosen_ids:
                filtered.append(post)
            if len(filtered) == k:
                break
        
        return filtered


