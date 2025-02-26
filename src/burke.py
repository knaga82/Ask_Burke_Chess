from openai import AzureOpenAI

class Burke:
    # Burke is an AI assistant for chess
    ### Be sure to remove api_key before pushing to remote git repos!!!

    def __init__(self):
        self.client = AzureOpenAI(
            azure_endpoint = "https://[your account].openai.azure.com/", 
            api_key="[enter your key]",  
            api_version="2024-02-01"
        )

    def get_fen(self, pos_str):
        # Ask Burke to generate FEN notation of the position with a string representation of the position
        prompt = f"Convert this {pos_str} to Chess FEN notation and respond back with only the FEN notation."

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert in Chess FEN notation."},
                    {"role": "user", "content": prompt}
                ]
            )

            pos_fen = response.choices[0].message.content
        except:
            pos_fen = "Error: Could not get position FEN"

        if pos_fen is not None:
            return pos_fen
        else:
            return "Error: Could not get position FEN"


    def evaluate_position(self, pos_fen, num_words, context):
        # Ask Burke to evaluate position
        prompt = f"In less than {num_words} words, use this Chess FEN notation {pos_fen} to {context}\n"
        print(prompt)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant to chess players."},
                    {"role": "user", "content": prompt}
                ]
            )

            evaluation = response.choices[0].message.content
        except:
            evaluation = "Error: Could not get position evaluation"

        if evaluation is not None:
            return evaluation
        else:
            return "Error: Could not get position evaluation"
