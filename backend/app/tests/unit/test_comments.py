from datetime import datetime, timedelta

from app.models.models import User, Post, Comment, ChildComment

from app.tests.base import BaseTestCase


# Test Comment model
class TestCommentModelCase(BaseTestCase):

    def test_post_comment(self, test_db):
        # create four users
        u1 = User(username="kureha", email="kureha@example.com")
        u2 = User(username="boru", email="boru@example.com")
        u3 = User(username="otami", email="otami@example.com")
        u4 = User(username="crocodile", email="crocodile@example.com")
        test_db.session.add_all([u1, u2, u3, u4])

        now = datetime.utcnow()

        # create four posts
        p1 = Post(
            content="luffy the pirate king",
            author=u1,
            timestamp=now + timedelta(seconds=1),
        )
        p2 = Post(
            content="Sabo finally consumes the flare flare fruit ",
            author=u1,
            timestamp=now + timedelta(seconds=4),
        )
        p3 = Post(
            content="Akainu must pay for killing ace :(",
            author=u3,
            timestamp=now + timedelta(seconds=3),
        )
        p4 = Post(
            content="Zoro has gotten lost again. haha!!",
            author=u2,
            timestamp=now + timedelta(seconds=2),
        )

        test_db.session.add_all([p1, p2, p3, p4])
        test_db.session.commit()

        # create comment on posts
        c1 = Comment(
            content="luffy the pirate king",
            author=u1,
            timestamps=now + timedelta(seconds=1),
            post=p1,
        )
        c2 = Comment(
            content="Sabo finally consumes the flare flare fruit ",
            author=u2,
            post=p2,
            timestamps=now + timedelta(seconds=4),
        )
        c3 = Comment(
            content="Akainu must pay for killing ace :(",
            author=u3,
            post=p3,
            timestamps=now + timedelta(seconds=3),
        )
        c4 = Comment(
            content="Zoro has gotten lost again. haha!!",
            author=u4,
            post=p4,
            timestamps=now + timedelta(seconds=2),
        )

        test_db.session.add_all([c1, c2, c3, c4])
        test_db.session.commit()

        # check the comments dropped by the users
        self.assert_equal(p1.comments.all(), [c1])
        self.assert_equal(p2.comments.all(), [c2])
        self.assert_equal(p3.comments.all(), [c3])
        self.assert_equal(p4.comments.all(), [c4])

    def test_like_comment(self, test_db):
        # create four users
        u1 = User(username="veronica", email="veronica@example.com")
        u2 = User(username="taylor", email="taylor@example.com")
        u3 = User(username="yuriko", email="yuriko@example.com")
        u4 = User(username="young", email="young@example.com")
        test_db.session.add_all([u1, u2, u3, u4])

        now = datetime.utcnow()

        # create four posts
        p1 = Post(
            content="luffy the pirate king",
            author=u1,
            timestamp=now + timedelta(seconds=1),
        )
        p2 = Post(
            content="Sabo finally consumes the flare flare fruit ",
            author=u1,
            timestamp=now + timedelta(seconds=4),
        )
        p3 = Post(
            content="Akainu must pay for killing ace :(",
            author=u3,
            timestamp=now + timedelta(seconds=3),
        )
        p4 = Post(
            content="Zoro has gotten lost again. haha!!",
            author=u2,
            timestamp=now + timedelta(seconds=2),
        )

        test_db.session.add_all([p1, p2, p3, p4])
        test_db.session.commit()

        # create comment on posts
        c1 = Comment(
            content="luffy the pirate king",
            author=u1,
            timestamps=now + timedelta(seconds=1),
            post=p1,
        )
        c2 = Comment(
            content="Sabo finally consumes the flare flare fruit ",
            author=u2,
            post=p2,
            timestamps=now + timedelta(seconds=4),
        )
        c3 = Comment(
            content="Akainu must pay for killing ace :(",
            author=u3,
            post=p3,
            timestamps=now + timedelta(seconds=3),
        )
        c4 = Comment(
            content="Zoro has gotten lost again. haha!!",
            author=u4,
            post=p4,
            timestamps=now + timedelta(seconds=2),
        )

        test_db.session.add_all([c1, c2, c3, c4])
        test_db.session.commit()

        # like comments
        c1.like_comment_state(u1)
        c1.like_comment_state(u2)
        c1.like_comment_state(u3)
        # comment 1 liked by luffy and users 2 and 3
        c2.like_comment_state(u2)
        c2.like_comment_state(u3)
        # comment 2 liked by sabo and user 3
        c4.like_comment_state(u2)
        # comment 4 liked by user2
        c3.like_comment_state(u1)
        # comment 3 liked by user1
        test_db.session.commit()

        # check the comments liked by the users
        self.assert_equal(c1.likes.all(), [u1, u2, u3])
        self.assert_equal(c2.likes.all(), [u2, u3])
        self.assert_equal(c3.likes.all(), [u1])
        self.assert_equal(c4.likes.all(), [u2])


# Test Child comments model
class ChildCommentModelCase(BaseTestCase):

    def test_post_child_comment(self, test_db):
        # create four users
        u1 = User(username="hawkins", email="hawkins@example.com")
        u2 = User(username="nami", email="nami@example.com")
        u3 = User(username="nico", email="nico@example.com")
        u4 = User(username="robin", email="robin@example.com")
        test_db.session.add_all([u1, u2, u3, u4])

        now = datetime.utcnow()

        # create four posts
        p1 = Post(
            content="luffy the pirate king",
            author=u1,
            timestamp=now + timedelta(seconds=1),
        )
        p2 = Post(
            content="Sabo finally consumes the flare flare fruit ",
            author=u1,
            timestamp=now + timedelta(seconds=4),
        )
        p3 = Post(
            content="Akainu must pay for killing ace :(",
            author=u3,
            timestamp=now + timedelta(seconds=3),
        )
        p4 = Post(
            content="Zoro has gotten lost again. haha!!",
            author=u2,
            timestamp=now + timedelta(seconds=2),
        )

        test_db.session.add_all([p1, p2, p3, p4])
        test_db.session.commit()

        # create comment on posts
        c1 = Comment(
            content="luffy the pirate king",
            author=u1,
            timestamps=now + timedelta(seconds=1),
            post=p1,
        )
        c2 = Comment(
            content="Sabo finally consumes the flare flare fruit ",
            author=u2,
            post=p2,
            timestamps=now + timedelta(seconds=4),
        )
        c3 = Comment(
            content="Akainu must pay for killing ace :(",
            author=u3,
            post=p3,
            timestamps=now + timedelta(seconds=3),
        )
        c4 = Comment(
            content="Zoro has gotten lost again. haha!!",
            author=u4,
            post=p4,
            timestamps=now + timedelta(seconds=2),
        )

        test_db.session.add_all([c1, c2, c3, c4])
        test_db.session.commit()

        # create comment under comments
        cc1 = ChildComment(
            content="one piece is within reach",
            author=u1,
            timestamps=now + timedelta(seconds=1),
            comment=c1,
        )
        cc2 = ChildComment(
            content="Sabo finally consumes the flare flare fruit",
            author=u2,
            comment=c2,
            timestamps=now + timedelta(seconds=4),
        )
        cc3 = ChildComment(
            content="Akainu must pay for killing ace :(",
            author=u3,
            comment=c3,
            timestamps=now + timedelta(seconds=3),
        )
        cc4 = ChildComment(
            content="Zoro has gotten lost again. haha!!",
            author=u4,
            comment=c4,
            timestamps=now + timedelta(seconds=2),
        )

        # check the comments dropped by the users
        self.assert_equal(c1.comments.all(), [cc1])
        self.assert_equal(c2.comments.all(), [cc2])
        self.assert_equal(c3.comments.all(), [cc3])
        self.assert_equal(c4.comments.all(), [cc4])

    def test_like_child_comment(self, test_db):
        # create four users
        u1 = User(username="xin", email="xin@example.com")
        u2 = User(username="assert_equal", email="assert_equal@example.com")
        u3 = User(username="cavendish", email="cavendish@example.com")
        u4 = User(username="bonny", email="bonny@example.com")
        test_db.session.add_all([u1, u2, u3, u4])

        now = datetime.utcnow()

        # create four posts
        p1 = Post(
            content="luffy the pirate king",
            author=u1,
            timestamp=now + timedelta(seconds=1),
        )
        p2 = Post(
            content="Sabo finally consumes the flare flare fruit ",
            author=u1,
            timestamp=now + timedelta(seconds=4),
        )
        p3 = Post(
            content="Akainu must pay for killing ace :(",
            author=u3,
            timestamp=now + timedelta(seconds=3),
        )
        p4 = Post(
            content="Zoro has gotten lost again. haha!!",
            author=u2,
            timestamp=now + timedelta(seconds=2),
        )

        test_db.session.add_all([p1, p2, p3, p4])
        test_db.session.commit()

        # create comment on posts
        c1 = Comment(
            content="luffy the pirate king",
            author=u1,
            timestamps=now + timedelta(seconds=1),
            post=p1,
        )
        c2 = Comment(
            content="Sabo finally consumes the flare flare fruit ",
            author=u2,
            post=p2,
            timestamps=now + timedelta(seconds=4),
        )
        c3 = Comment(
            content="Akainu must pay for killing ace :(",
            author=u3,
            post=p3,
            timestamps=now + timedelta(seconds=3),
        )
        c4 = Comment(
            content="Zoro has gotten lost again. haha!!",
            author=u4,
            post=p4,
            timestamps=now + timedelta(seconds=2),
        )

        test_db.session.add_all([c1, c2, c3, c4])
        test_db.session.commit()

        # create comment under comments
        cc1 = ChildComment(
            content="one piece is within reach",
            author=u1,
            timestamps=now + timedelta(seconds=1),
            comment=c1,
        )
        cc2 = ChildComment(
            content="Sabo finally consumes the flare flare fruit",
            author=u2,
            comment=c2,
            timestamps=now + timedelta(seconds=4),
        )
        cc3 = ChildComment(
            content="Akainu must pay for killing ace :(",
            author=u3,
            comment=c3,
            timestamps=now + timedelta(seconds=3),
        )
        cc4 = ChildComment(
            content="Zoro has gotten lost again. haha!!",
            author=u4,
            comment=c4,
            timestamps=now + timedelta(seconds=2),
        )

        # like child comments
        cc1.like_child_comment(u1)
        cc1.like_child_comment(u2)
        cc1.like_child_comment(u3)
        # child comment under comment 1 liked by users 1, 2 and 3
        cc2.like_child_comment(u2)
        cc2.like_child_comment(u3)
        # child comment under comment 2 liked by users 2 and 3
        cc4.like_child_comment(u2)
        # child comment under comment 4 liked by user2
        cc3.like_child_comment(u1)
        # child comment under comment 3 liked by user1
        test_db.session.commit()

        # check the child comments liked by the users
        self.assert_equal(cc1.likes.all(), [u1, u2, u3])
        self.assert_equal(cc2.likes.all(), [u2, u3])
        self.assert_equal(cc3.likes.all(), [u1])
        self.assert_equal(cc4.likes.all(), [u2])
