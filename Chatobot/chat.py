import os
import random
from nltk.chat.util import Chat, reflections
from utils.text_processing import preprocess_text, create_tfidf_vectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MovieChatbot:
    def __init__(self):
        self.movie_scripts = {}
        self.script_sentences = []
        self.stop_words = None
        self.vectorizer = None
        self.tfidf_matrix = None
        
        self.pairs = [
            [r"oi|olá|e aí", ["Olá! Vamos falar sobre Shrek?", "Oi! Pronto para discutir Shrek?"]],
            [r"tchau|adeus|até mais", ["Até logo! Hora de assistir Shrek de novo!", "Tchau! Que a força do ogro esteja com você!"]],
            [r"qual seu personagem favorito?", ["Eu adoro o Shrek, é claro! Mas o Burro é muito engraçado também!"]],
            [r"o que você sabe sobre (.*)\?", ["Me conte mais sobre %1, estou aprendendo sobre o universo Shrek!"]]
        ]
        self.chatbot = Chat(self.pairs, reflections)
    
    def load_script(self, title, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Arquivo {filepath} não encontrado!")
            
        with open(filepath, 'r', encoding='utf-8') as f:
            script = f.read()
        
        sentences, self.stop_words = preprocess_text(script)
        self.script_sentences = [(title, sent) for sent in sentences]
        self.vectorizer = create_tfidf_vectorizer(self.stop_words)
        self._update_tfidf()
        self.movie_scripts[title] = script
    
    def _update_tfidf(self):
        if self.script_sentences:
            sentences_only = [sent for _, sent in self.script_sentences]
            self.tfidf_matrix = self.vectorizer.fit_transform(sentences_only)
    
    def _find_most_relevant_sentence(self, user_input):
        if not self.script_sentences:
            return None, None
            
        user_vec = self.vectorizer.transform([user_input])
        similarities = cosine_similarity(user_vec, self.tfidf_matrix)
        max_idx = similarities.argmax()
        return self.script_sentences[max_idx]
    
    def respond(self, user_input):
        response = self.chatbot.respond(user_input)
        if response:
            return response
        
        title, sentence = self._find_most_relevant_sentence(user_input) or (None, None)
        
        if sentence:
            responses = [
                f"De acordo com a Wikipedia de {title}: {sentence}",
                f"Encontrei isso sobre {title}: {sentence}",
                f"No artigo da Wikipedia tem essa informação: {sentence}",
                f"Segundo a Wikipedia: {sentence}"
            ]
            return random.choice(responses)
        
        return "Não encontrei informações sobre isso no artigo. Quer me contar mais?"

def main():
    bot = MovieChatbot()
    
    script_path = os.path.join('data', 'scripts', 'shrek_wikipedia.txt')
    bot.load_script("Shrek", script_path)
    
    print("Chatbot do Shrek (digite 'tchau' para sair)")
    print("Você pode perguntar sobre qualquer coisa do filme Shrek!")
    
    while True:
        try:
            user_input = input("Você: ")
            if user_input.lower() in ['tchau', 'adeus', 'até mais']:
                print("Bot: Até mais! Lembre-se: Shrek é amor, Shrek é vida!")
                break
            
            response = bot.respond(user_input)
            print("Bot:", response)
        
        except KeyboardInterrupt:
            print("\nBot: Interrompido pelo usuário. Fiona ficaria triste!")
            break
        except Exception as e:
            print(f"Bot: Oops, algo deu errado ({e}). Vamos tentar novamente?")

if __name__ == "__main__":
    main()
