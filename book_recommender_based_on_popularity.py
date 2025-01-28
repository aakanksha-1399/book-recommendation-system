import pickle
import pandas as pd

books = pd.read_csv("Books.csv")
ratings = pd.read_csv("Ratings.csv")
users = pd.read_csv("Users.csv")
pd.set_option('display.max_columns', None)

# drop columns Image - URL _ M and S as they are the same
books = books.drop(['Image-URL-M', 'Image-URL-M'], axis = 1 )

# Popularity Based Recommendation System
# Criteria 1 - Min 250 people should have voted for the book
# Criteria 2 - Top 50, Highest Avg Rating books will be displayed

# Merge Ratings and Books on ISBN
rating_with_books = ratings.merge(books, on = "ISBN")

# Group by Book Title
num_rating_df = rating_with_books.groupby("Book-Title").count()['Book-Rating'].reset_index()
num_rating_df.rename(columns={'Book-Rating': 'num_ratings'}, inplace=True)

# Calculating the Avg Rating for each book
grouped = rating_with_books.groupby("Book-Title")
avg_rating = grouped['Book-Rating'].mean()
avg_rating_df = avg_rating.reset_index()

avg_rating_df.rename(columns={'Book-Rating': 'Avg Rating'}, inplace = True)

popularity_df = num_rating_df.merge(avg_rating_df, on = "Book-Title")

# # num_rating > 250
popular_books = (popularity_df[popularity_df['num_ratings'] >= 250].
                 sort_values('Avg Rating', ascending=False)).head(50)

top_50 = popular_books.merge(books, on = "Book-Title").drop_duplicates('Book-Title')[['Book-Title', 'Book-Author', 'Image-URL-L', 'num_ratings', 'Avg Rating']]
pickle.dump(top_50, open('top_50.pkl','wb'))