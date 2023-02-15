from friendships.services import FriendshipService

class NewsFeedService(object):
    @classmethod
    def fanout_to_followers(cls, tweet):
        newsfeeds = [
            NewsFeed(user=follower, tweet=tweet)
            for follower in FriendshipService.get_followers(tweet)
        ]
        newsfeeds.append(NewsFeed(user=tweet.user, tweet=tweet))
        newsfeeds.objects.bulk_create(newsfeeds)