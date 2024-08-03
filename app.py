from flask import Flask,render_template,request
import pickle
import pandas
import numpy as np
popular_df = pandas.read_pickle('./popular.pkl')
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))
# search = pickle.load(open('search.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-L'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')
@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = 0
    for i,title in enumerate(pt.index):
        if user_input.lower() in title.lower():
            index = i
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))
        data.append(item)
    print(data)

    return render_template('recommend.html',data=data)

# @app.route('/search')
# def search_ui():
#     return render_template('search.html')

# @app.route('/search_books',methods=['post'])
# def searching():
#     user_search = request.form.get('user_search')
#     user_search=str(user_search)
#     crt_names=search[search['Book-Title'].str.contains(pat=user_search,case=False)].head(8)
#     name_data=crt_names.values.tolist()
#     print(name_data)
#     return render_template('search.html',name_data=name_data)

if __name__ == '__main__':
    app.run(debug=False)