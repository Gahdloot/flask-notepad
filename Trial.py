from app import BlogPost
all_post = BlogPost.query.order_by(BlogPost.date_posted).all()

a = len(all_post)

for num in range(a):
    print(BlogPost.query[num].title)
    print(BlogPost.query[num].content)
    print(BlogPost.query[num].author)
    print('___________________')


