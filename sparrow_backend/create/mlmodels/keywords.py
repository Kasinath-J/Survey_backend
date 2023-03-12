from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def split(s):
    t = s.split('(')
    t[1] = float(t[1][:-1])
    return {"value":t[0],"count":t[1]}

def keywords_fn(lst):

    # print("-----------------------------------------------------")
    # print(lst)
    # print("-----------------------------------------------------")
    # preprocess the documents by removing stop words and creating a document-term matrix
    try:
        stop_words = 'english'
        vectorizer = CountVectorizer(stop_words=stop_words)
        
        doc_term_matrix = vectorizer.fit_transform(lst)

        # train the LDA topic model
        num_topics = 1
        lda_model = LatentDirichletAllocation(n_components=num_topics, random_state=0)
        lda_model.fit(doc_term_matrix)

        # print the most important keywords for each topic
        feature_names = vectorizer.get_feature_names()
        temp = None
        for topic_idx, topic in enumerate(lda_model.components_):
            temp = "Topic {}:{}".format(topic_idx, ",".join(["{}({:.1f})".format(feature_names[i], topic[i]) for i in topic.argsort()[:-6:-1]]))

        keyword = temp.split(":")[1].split(",")
        keyword = list(map(split,keyword))
        
        return keyword
    
    except:
        pass
    