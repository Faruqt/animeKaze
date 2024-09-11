from datetime import datetime, timedelta

from app.models.models import User, Post
from app.tests.base import BaseTestCase


# Test User model
class TestUserModelCase(BaseTestCase):

    def test_password_hashing(self):
        u = User(username="Luffy")
        u.set_password("pirate")
        self.assert_equal(u.check_password("piracy"), False)
        self.assert_equal(u.check_password("pirate"), True)

    def test_follow(self, test_db):
        u1 = User(username="johndoe", email="johndoe@example.com")
        u2 = User(username="goldroger", email="goldroger@example.com")
        test_db.session.add(u1)
        test_db.session.add(u2)
        test_db.session.commit()
        self.assert_equal(u1.followed.all(), [])
        self.assert_equal(u1.followers.all(), [])

        u1.follow(u2)
        test_db.session.commit()
        self.assert_equal(u1.is_following(u2), True)
        self.assert_equal(u1.followed.count(), 1)
        self.assert_equal(u1.followed.first().username, "goldroger")
        self.assert_equal(u2.followers.count(), 1)
        self.assert_equal(u2.followers.first().username, "johndoe")

        u1.unfollow(u2)
        test_db.session.commit()
        self.assert_equal(u1.is_following(u2), False)
        self.assert_equal(u1.followed.count(), 0)
        self.assert_equal(u2.followers.count(), 0)

    def test_follow_posts(self, test_db):
        # create four users
        u1 = User(username="law", email="law@example.com")
        u2 = User(username="whitebeard", email="whitebeard@example.com")
        u3 = User(username="hawkins", email="hawkins@example.com")
        u4 = User(username="drake", email="drake@example.com")
        test_db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(
            content="luffy is the pirate king",
            author=u1,
            timestamp=now + timedelta(seconds=1),
        )
        p2 = Post(
            content="Sabo will finally consume the flare flare fruit ",
            author=u2,
            timestamp=now + timedelta(seconds=4),
        )
        p3 = Post(
            content="Akainu will have to pay for killing ace :(",
            author=u3,
            timestamp=now + timedelta(seconds=3),
        )
        p4 = Post(
            content="Zoro has gotten lost again. oh no!!",
            author=u4,
            timestamp=now + timedelta(seconds=2),
        )
        p5 = Post(
            content="Usopp is truly the pirate kings's sniper!!",
            author=u4,
            timestamp=now + timedelta(seconds=1),
        )

        test_db.session.add_all([p1, p2, p3, p4, p5])
        test_db.session.commit()

        # setup the followers
        u1.follow(u2)  # luffy follows sabo
        u1.follow(u4)  # luffy follows zoro
        u2.follow(u3)  # sabo follows ace
        u3.follow(u4)  # ace follows zoro
        test_db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()

        # check for posts by timestamp descending order
        self.assert_equal(f1, [p2, p4, p1, p5])
        # luffy can see his own post and that of sabo and zoro
        self.assert_equal(f2, [p2, p3])
        # sabo can see his own post and that of ace
        self.assert_equal(f3, [p3, p4, p5])
        # # ace can see his own post and that of zoro
        self.assert_equal(f4, [p4, p5])
        # zoro follows no one, so he can see only his own post

    def test_reported_posts(self, test_db):
        # create four users
        u1 = User(username="franky", email="franky@example.com")
        u2 = User(username="chopper", email="chopper@example.com")
        u3 = User(username="apoo", email="apoo@example.com")
        u4 = User(username="roger", email="roger@example.com")
        test_db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(
            content="luffy will become the pirate king",
            author=u1,
            timestamp=now + timedelta(seconds=1),
        )
        p2 = Post(
            content="Sabo has consumed the flare flare fruit ",
            author=u2,
            timestamp=now + timedelta(seconds=4),
        )
        p3 = Post(
            content="Akainu has to pay for killing ace :(",
            author=u3,
            timestamp=now + timedelta(seconds=3),
        )
        p4 = Post(
            content="Zoro will get lost again. haha!!",
            author=u4,
            timestamp=now + timedelta(seconds=2),
        )
        p5 = Post(
            content="Usopp will be the pirate kings's sniper!!",
            author=u4,
            timestamp=now + timedelta(seconds=1),
        )

        test_db.session.add_all([p1, p2, p3, p4, p5])
        test_db.session.commit()

        # setup the followers
        u1.follow(u2)  # luffy follows sabo
        u1.follow(u4)  # luffy follows zoro
        u2.follow(u3)  # sabo follows ace
        u2.follow(u1)  # sabo follows luffy
        u3.follow(u2)  # ace follows sabo
        u3.follow(u4)  # ace follows zoro
        u4.follow(u3)  # zoro follows ace
        test_db.session.commit()

        # report posts
        p1.report(u2)
        # post 1 reported by user2 named "sabo"
        p2.report(u3)
        # post 2 reported by user3 named "ace"
        p4.report(u1)
        # post 4 reported by user1 named "luffy"
        p3.report(u4)
        # post 3 reported by user4 named "zoro"
        test_db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()

        # check for posts by timestamp descending order excluding the reported posts
        self.assert_equal(f1, [p2, p1, p5])
        # luffy can see his own post and that of sabo and zoro minus post 4 that he reported
        self.assert_equal(f2, [p2, p3])
        # sabo can see his own post and that of ace and luffy minus post 1 that he reported
        self.assert_equal(f3, [p3, p4, p5])
        # ace can see his own post and that of zoro minus sabo's post that he reported
        self.assert_equal(f4, [p4, p5])
        # zoro can see his own post minus ace's post that he reported

    def test_not_interested_in_posts(self, test_db):
        # create four users
        u1 = User(username="capone", email="capone@example.com")
        u2 = User(username="brook", email="brook@example.com")
        u3 = User(username="oda", email="oda@example.com")
        u4 = User(username="shanks", email="shanks@example.com")
        test_db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(
            content="luffy the pirate king",
            author=u1,
            timestamp=now + timedelta(seconds=1),
        )
        p2 = Post(
            content="Sabo finally consumes the flare flare fruit ",
            author=u2,
            timestamp=now + timedelta(seconds=4),
        )
        p3 = Post(
            content="Akainu must pay for killing ace :(",
            author=u3,
            timestamp=now + timedelta(seconds=3),
        )
        p4 = Post(
            content="Zoro has gotten lost again. haha!!",
            author=u4,
            timestamp=now + timedelta(seconds=2),
        )
        p5 = Post(
            content="Usopp is the pirate kings's sniper!!",
            author=u4,
            timestamp=now + timedelta(seconds=1),
        )

        test_db.session.add_all([p1, p2, p3, p4, p5])
        test_db.session.commit()

        # mark posts as not interested
        p1.no_interest(u2)
        # post 1 reported by user2 named "sabo"
        p2.no_interest(u3)
        # post 2 reported by user3 named "ace"
        p4.no_interest(u1)
        # post 4 reported by user1 named "luffy"
        p3.no_interest(u4)
        # post 3 reported by user4 named "zoro"
        test_db.session.commit()

        # check the followed posts of each user
        f1 = u1.filter_posts().all()
        f2 = u2.filter_posts().all()
        f3 = u3.filter_posts().all()
        f4 = u4.filter_posts().all()

        # display all posts by timestamp descending order excluding posts user has no interest in
        self.assert_not_in_list(p4, f1)
        # luffy can see all other users' posts minus post 4 that he marked as not interested
        self.assert_not_in_list(p1, f2)
        # sabo can see all other users' posts minus post 1 that he marked as not interested
        self.assert_not_in_list(p2, f3)
        # ace can see all other users' posts minus post 2 that he marked as not interested
        self.assert_not_in_list(p3, f4)
        # zoro can see all other users' posts minus post 3 that he marked as not interested
