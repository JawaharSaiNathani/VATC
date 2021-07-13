# Import Required Modules
import requests
from bs4 import BeautifulSoup as bs
from googlesearch import search
from ktrain import load_predictor
is_predictor = 1
print("Loading BERT Model...")
# Load BERT Model
try:
    predictor = load_predictor('model/bert_model')
    print("Model Loded Successfully")
except:
    is_precictor = 0
    print("Model not found")

# [ Function to get Code snippets from StackOverFlow ]
def get_stackoverflow_codes(link):
    res = requests.get(link)    # get HTML template
    soup = bs(res.text,"html.parser")
    alla = soup.select(".answer")

    # Function to get codes
    def get_answers(ans):
        fin_ans = []
        for i in range(len(ans)):
            user = ""
            code_section = ans[i].select(".js-post-body")[0]
            pres = code_section.select("pre")
            codes = []
            for j in range(len(pres)):
                codes.append(pres[j].select("code")[0].text.strip())
            code = '\n'.join(codes)
            vote = int(ans[i].select(".js-vote-count")[0].text.strip())
            
            coms = []
            comments = ans[i].select(".js-comments-list")[0].select(".js-comment")
            for j in range(len(comments)):
                sc = comments[j].select(".comment-score")[0].select('span')
                if len(sc) > 0:
                    score = int(sc[0].text.strip())
                else:
                    score = 0
                comment = comments[j].select(".comment-body")[0].select('span')[0].text.strip()
                usr = comments[j].select(".comment-body")[0].select('.comment-user')[0].text.strip()
                coms.append([usr,comment,score])
            fin_ans.append([user,code,vote,coms])
        return fin_ans

    alla = get_answers(alla)
    return alla

# [ Function to get Code snippets from GeeksForGeeks ]
def get_geeksforgeeks_codes(link):
    res = requests.get(link)
    soup = bs(res.text,"html.parser")

    codes = []
    cds = soup.select(".code-block")
    for i in range(len(cds)):
        code = ""
        lines = []
        line = cds[i].select(".code-container")[0].select('td')[0].select(".line")
        for x in line:
            l = x.text.strip()
            spaces = x.select(".spaces")
            space = ''
            if len(spaces) > 0:
                flag = 0
                for s in str(spaces):
                    if s == '>':
                        flag = 1
                    if s == '<' and flag == 1:
                        break
                    if flag == 1:
                        space += ' '
                space = space[:-1]
            l = space + l
            lines.append(l)
        code = '\n'.join(lines)
        codes.append(code)
    return codes

# [ Function to search links for search query ]
def search_web(query):
    global is_predictor

    gfg_link = ""
    for j in search(("site:geeksforgeeks.org "+query+" in python"), num=1, stop=1): # get GeeksForGeeks links
        gfg_link = j
    gfg_codes = get_geeksforgeeks_codes(gfg_link)
    sof_link = ""
    for j in search(("site:stackoverflow.com "+query+" in python"), num=1, stop=1): # get StackOverFlow links
        sof_link = j
    sof_codes = get_stackoverflow_codes(sof_link)

    # Categorise these posts using BERT Model
    for i in range(len(sof_codes)):
        votes = sof_codes[i][2]
        com_score = 0
        for j in range(len(sof_codes[i][3])):
            com_sent = ''
            if is_predictor == 1:   # check sentiment of comments
                com_sent = predictor.predict(sof_codes[i][3][j][1])
            else:
                com_sent = 'pos'
            if com_sent == 'neg':
                com_score += (-1*(sof_codes[i][3][j][2]+1))
            else:
                com_score += (sof_codes[i][3][j][2] + 1)
        score = votes + (com_score/4)   # Post score
        sof_codes[i].append(score)
    sof_codes.sort(key = lambda x: x[4])

    #   Prepare final codes snippets
    fin_codes = []
    flag = len(sof_codes)
    for i in range(len(sof_codes)-1,-1,-1):
        if sof_codes[i][4] > 10:
            flag = i
            fin_codes.append(['StackOverFlow',sof_link,sof_codes[i][1]])
        else:
            break
    for i in range(len(gfg_codes)):
        fin_codes.append(['GeeksForGeeks',gfg_link,gfg_codes[i]])
    for i in range(flag-1,-1,-1):
        fin_codes.append(['StackOverFlow',sof_link,sof_codes[i][1]])

    return fin_codes

if __name__=='__main__':
    query = input("Enter Search Query: ")
    final_codes = search_web(query)

    for x in final_codes:
        print(x[0])
        print('\n')
        print(x[2])
        print('\n\n')