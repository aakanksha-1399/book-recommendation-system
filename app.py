import numpy as np
from flask import  Flask,render_template
import pickle
from flask import request


from book_recommender_collaborative_filter import collaborative_table, \
    similarity_table

popular_df = pickle.load(open('top_50.pkl','rb'))
collaborative_df = pickle.load(open('collaborative_table.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_table = pickle.load(open('similarity_table.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html')



@app.route("/top_50")
def top_50():
    return render_template("top_50.html",

                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image =list(popular_df['Image-URL-L'].values),
                           rating=[round(r, 2) for r in list(popular_df['Avg Rating'].values)])

@app.route("/recommend")
def recommend():
    return render_template("recommend.html")

@app.route("/recommend_books", methods = ['POST'])
def recommend_books():
    user_input = request.form.get('user_input')
    index = np.where(collaborative_table.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_table[index])),
                           key=lambda x: x[1], reverse=True)[1:7]

    data = []
    for i in similar_items:
        # print(collaborative_table.index[i[0]])
        item = []
        book_title = collaborative_table.index[i[0]]
        matched_row = books[books[
                                'Book-Title'].str.strip().str.lower() == book_title.strip().lower()]
        item.extend(list(
            matched_row.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(
            matched_row.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(
            list(matched_row.drop_duplicates('Book-Title')['Image-URL-L']))
        data.append(item)
    print(data)
        # print(matched_row)
    return render_template('recommend.html', data = data)

if __name__ == '__main__':
    app.run(debug=True)