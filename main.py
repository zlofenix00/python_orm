from moduls import engine, Base
from moduls import User, Post
from sqlalchemy.orm import Session, joinedload


def create_user(session: Session, username: str, email: str | None = None) -> User:
    user = User(username=username, email=email)
    session.add(user)
    session.commit()
    print(user)
    return user


def get_user_by_id(session: Session, user_id: int) -> User | None:
    user = session.get(User, user_id)
    print("user by id", user_id, "value:", user)
    return user


def create_posts(session: Session, post_title: str, user: User) -> Post:
    post = Post(
        title=post_title,
        user_id=user.id,
        # user=user,
    )
    session.add(post)
    session.commit()
    print("crated post", post)
    return post


def show_user_with_posts(session: Session, user_id: int) -> User | None:
    user: User | None = session.get(User, user_id)
    if user is None:
        print("user not found")
        return

    print("************ user:", user.username)
    for post in user.posts:
        print("post", post.id, post.title)
    return user


def show_users_with_posts(
        session: Session,
        only_with_posts: bool = False,
) -> list[User]:
    users: list[User] = (
        session
        .query(User)
        .options(
            joinedload(
                User.posts,
                innerjoin=only_with_posts,
            )
        )
        .order_by(User.id)
        .all()
    )

    for user in users:

        print()
        print("************ user:", user.username)
        for post in user.posts:
            print("post", post.id, post.title)
        print()
    return users


def show_posts_with_users(session: Session) -> list[Post]:
    posts = (
        session
        .query(Post)
        .options(joinedload(Post.user))
        .order_by(Post.id)
        .all()
    )

    for post in posts:
        print()
        print("************ post:", post.id, post.title, post.user)

    return posts


def run_queries():
    with Session(engine) as session:
        user_john = create_user(session, username="john")
        user_sam = create_user(session, username="sam", email="sam@example.com")
        user_nick = create_user(session, username="nick", email="nick@example.com")

        create_posts(session, "Post by John", user=user_john)
        create_posts(session, "SQL John", user=user_john)

        create_posts(session, "Post by Sam", user=user_sam)
        create_posts(session, "PyCharm post", user=user_sam)
        create_posts(session, "Test post", user=user_sam)

        show_user_with_posts(session, user_john.id)
        show_user_with_posts(session, user_sam.id)
        show_users_with_posts(session)
        show_users_with_posts(session, only_with_posts=True)
        show_posts_with_users(session)


def main():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    run_queries()


if __name__ == '__main__':
    main()
