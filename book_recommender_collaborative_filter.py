# Collaborative based filtering
import pickle

import pandas as pd
import numpy as  np
from sklearn.metrics.pairwise import cosine_similarity

# read the csv file
books = pd.read_csv("Books.csv")
ratings = pd. read_csv("Ratings.csv")
users = pd.read_csv("Users.csv")

pd.set_option('display.max_columns', None)
# now merge books and ratings
book_and_ratings = ratings.merge(books, on = "ISBN")

# keep users having more than 200 votes
users_with_200_votes = book_and_ratings.groupby("User-ID").count()['Book-Rating'] > 200
# boolean = s[s] and then this will give me only true cases and then when I use
# .index it helps me with getting the ids
read_users = users_with_200_votes[users_with_200_votes].index

# getting only those users who have rated more than 200 books
filtered_rating = book_and_ratings[book_and_ratings['User-ID'].isin(read_users)]

# get only books which have more than 50 votes abd then make sure to only get the true cases
books_rated = filtered_rating.groupby('Book-Title').count()['Book-Rating'] >= 50
famous_books = books_rated[books_rated].index

final_books_list = filtered_rating[filtered_rating['Book-Title'].isin(famous_books)]

collaborative_table = final_books_list.pivot_table(index = 'Book-Title', columns =
'User-ID', values = 'Book-Rating')

# fill na
collaborative_table.fillna(0, inplace = True )

# using cossine similarity - this is to get the Euclidean distance
# so that we cansee how similar something is
similarity_table = cosine_similarity(collaborative_table)

def recommend(book_name):
    # # fetch index from the bookname
    index = np.where(collaborative_table.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_table[index])),key = lambda x:x[1], reverse = True)[1:6]

    data = []
    for i in similar_items:
        # print(collaborative_table.index[i[0]])
        item = []
        book_title = collaborative_table.index[i[0]]
        matched_row = books[books['Book-Title'].str.strip().str.lower() == book_title.strip().lower()]
        item.extend(list(matched_row.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(matched_row.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(matched_row.drop_duplicates('Book-Title')['Image-URL-L']))
        data.append(item)
        # print(matched_row)
    return data


def main():
    data=recommend('Harry Potter and the Chamber of Secrets (Book 2)')
    print(data)
pickle.dump(collaborative_table, open('collaborative_table.pkl','wb'))
pickle.dump(books, open('books.pkl','wb'))
pickle.dump(similarity_table, open('similarity_table.pkl','wb'))

if __name__ == "__main__":
    main()