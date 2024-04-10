"""
This file is used to generate question_bank.csv

The formatting of the entries in the question bank was wrong
Spent time formatting the question by changing prompts
"""
from langchain_community.document_loaders.text import TextLoader
from openai import OpenAI
from langchain_text_splitters import CharacterTextSplitter

SAMPLE_Q = '''Which of the following populations is not in Hardy-Weinberg equilibrium?,"a population with 12 
homozygous recessive individuals (yy), 8 homozygous dominant individuals (YY), and 4 heterozygous individuals (Yy)",
"a population in which the allele frequencies do not change over time","p2 + 2pq + q2 = 1","a population undergoing 
natural selection","a population undergoing natural selection" '''
PROMPT = "From the information given below generate a question following the csv pattern:" \
         "question,answer_choice_0,answer_choice_1,answer_choice_2,answer_choice_3,correct_answer \n. " \
         "Add comma seperated values. Don't miss the comma and all the values\n" \
         "A sample question is :" \
         "{} \n\n information : {}"


def generate_testbench():
    raw_documents = TextLoader('textbook.txt').load()
    text_splitter = CharacterTextSplitter(chunk_size=10000, chunk_overlap=0)
    documents = text_splitter.split_documents(raw_documents)
    id = 1
    for doc in documents:
        content = doc.page_content
        client = OpenAI(
            api_key='XXXX',
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": PROMPT.format(SAMPLE_Q, content)},
            ],
        )
        response_text = response.choices[0].message.content
        f = open("question_bank.csv", "a")
        q = str(id) + "," + response_text
        f.write(q)
        f.write('\n')
        id += 1
        f.close()


if __name__ == '__main__':
    generate_testbench()
