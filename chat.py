import pandas as pd

# Load our health data
df = pd.read_csv('health_data.csv')

print("HealthBot: Hi! I'm a simple bot. Ask me about a symptom or say 'quit'.")

while True:
    # 1. Get the user's input
    user_text = input("\nYou: ").lower()

    # 2. Check if they want to exit
    if user_text == "quit":
        print("HealthBot: Goodbye! Stay healthy.")
        break

    # 3. The "Librarian" Loop
    found_answer = False
    
    for index, row in df.iterrows():
        # Clean up the keywords from the CSV row
        keywords_list = str(row['Keywords']).split(',')
        
        # Check every keyword in that row
        for word in keywords_list:
            clean_word = word.strip().lower()
            
            # If the keyword is inside the user's sentence
            if clean_word in user_text:
                print("HealthBot:", row['Response'])
                found_answer = True
                break # Stop looking at keywords for this row
        
        if found_answer:
            break # Stop looking at other rows since we found a match

    # 4. If we went through the whole CSV and found nothing
    if not found_answer:
        print("HealthBot: I don't know that one. Try asking about 'fever' or 'diet'.")
        
    else:
        print("HealthBot: I don't know that one. .")
        