from datetime import datetime, timedelta
from app.models.models import User, Post
from app.tests.base import BaseTestCase


# Test Post model
class TestPostModelCase(BaseTestCase):

    def test_report_posts(self, test_db):
        # create two users
        u1 = User(
            username="luffy",
            first_name="Monkey",
            last_name="D.luffy",
            email="luffy@example.com",
        )
        u2 = User(username="sabo", email="sabo@example.com")
        u3 = User(username="ace", email="ace@example.com")
        test_db.session.add_all([u1, u2, u3])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(
            content="Kaido the pirate king",
            author=u1,
            timestamp=now + timedelta(seconds=1),
        )
        p2 = Post(
            content="Akainu finally consumes the flare flare fruit ",
            author=u1,
            timestamp=now + timedelta(seconds=4),
        )
        p3 = Post(
            content="Doflamingo must pay for killing ace :(",
            author=u3,
            timestamp=now + timedelta(seconds=3),
        )
        p4 = Post(
            content="Dragon has gotten lost again. haha!!",
            author=u2,
            timestamp=now + timedelta(seconds=2),
        )

        test_db.session.add_all([p1, p2, p3, p4])
        test_db.session.commit()

        # setup the followers
        u1.follow(u2)  # luffy follows sabo
        u2.follow(u1)  # sabo follows luffy
        test_db.session.commit()

        # report posts
        p1.report(u2)
        # post 1 reported by user2 named "sabo"
        p2.report(u2)
        # post 2 reported by user2 named "sabo"
        p2.report(u3)
        # post 2 reported by user3 named "ace"
        p4.report(u1)
        # post 4 reported by user1 named "luffy"
        test_db.session.commit()

        self.assert_equal(p1.reported.first(), u2)
        self.assert_equal(p2.reported.all(), [u2, u3])
        self.assert_equal(p4.reported.first(), u1)

        # confirm who reported which post
        self.assert_equal(p1.post_reported(u1), False)
        self.assert_equal(p1.post_reported(u2), True)

        # confirm who reported which post
        self.assert_equal(p4.post_reported(u2), False)
        self.assert_equal(p4.post_reported(u1), True)

    def test_interest_posts(self, test_db):
        # create two users
        u1 = User(
            username="Buggy",
            first_name="Monkey",
            last_name="D.luffy",
            email="emperor@example.com",
        )
        u2 = User(username="saka", email="saka@example.com")
        u3 = User(username="kane", email="kane@example.com")
        test_db.session.add_all([u1, u2, u3])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(
            content="Shanks the pirate king",
            author=u1,
            timestamp=now + timedelta(seconds=1),
        )
        p2 = Post(
            content="Naruto finally consumes the flare flare fruit ",
            author=u1,
            timestamp=now + timedelta(seconds=4),
        )
        p3 = Post(
            content="Itachi must pay for killing ace :(",
            author=u3,
            timestamp=now + timedelta(seconds=3),
        )
        p4 = Post(
            content="Madara has gotten lost again. haha!!",
            author=u2,
            timestamp=now + timedelta(seconds=2),
        )

        test_db.session.add_all([p1, p2, p3, p4])
        test_db.session.commit()

        # mark posts as not interested
        p1.no_interest(u2)
        # post 1 reported by user2 named "sabo"
        p2.no_interest(u3)
        # post 2 reported by user3 named "ace"
        p4.no_interest(u1)
        # post 4 reported by user1 named "luffy"
        p3.no_interest(u1)
        # post 3 reported by user4 named "zoro"
        test_db.session.commit()

        # check the posts marked as not interested by the users
        self.assert_equal(p1.not_interested.all(), [u2])
        self.assert_equal(p2.not_interested.all(), [u3])
        self.assert_equal(p4.not_interested.all(), [u1])
        self.assert_equal(p3.not_interested.all(), [u1])

    def test_like_posts(self, test_db):
        # create three users
        u1 = User(
            username="Junior",
            first_name="Akainu",
            last_name="D.luffy",
            email="akainu@example.com",
        )
        u2 = User(username="sanji", email="sanji@example.com")
        u3 = User(username="yagami", email="yagami@example.com")
        test_db.session.add_all([u1, u2])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(
            content="zoro the pirate king",
            author=u1,
            timestamp=now + timedelta(seconds=1),
        )
        p2 = Post(
            content="Law finally consumes the flare flare fruit ",
            author=u1,
            timestamp=now + timedelta(seconds=4),
        )
        p3 = Post(
            content="Garp must pay for killing ace :(",
            author=u3,
            timestamp=now + timedelta(seconds=3),
        )
        p4 = Post(
            content="Sanji has gotten lost again. haha!!",
            author=u2,
            timestamp=now + timedelta(seconds=2),
        )

        test_db.session.add_all([p1, p2, p3, p4])
        test_db.session.commit()

        # like posts
        p1.like_state(u1)
        p1.like_state(u2)
        p1.like_state(u3)
        # post 1 liked by luffy and users 2 and 3
        p2.like_state(u2)
        p2.like_state(u3)
        # post 2 liked by sabo and user 3
        p4.like_state(u2)
        # post 4 liked by user2
        p3.like_state(u1)
        # post 3 liked by user1
        test_db.session.commit()

        # check the posts liked by the users
        self.assert_equal(p1.likes.all(), [u1, u2, u3])
        self.assert_equal(p2.likes.all(), [u2, u3])
        self.assert_equal(p4.likes.all(), [u2])
        self.assert_equal(p3.likes.all(), [u1])
