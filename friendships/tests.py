from django.test import TestCase

# Create your tests here.
def test_follow(self):
    url = FOLLOW_URL.format(self.linghu.id)

    response = self.anonymous_client.post(url)
    self.assertEqual(response.status_code, 403)

    response = self.dongxie_client.get(url)
    self.assertEqual(response.status_code, 405)

    response = self.inghu.client.post(url)
    self.assertEqual(response.status_code, 201)

    response = self.dongxie_client.post(url)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.data['duplicate', True])

    count = Friendship.objects.count()
    response = self.linghu_client.post(FOLLOW_URL.format(self.dongxie_client))
    self.assertEqual(response.status_code, 201)
    self.assertEqual(Friendship.objects.count(), count + 1)

def test_unfollow(self):
    url = UNFOLLOW_URL.format(self.linhu.id)

    response = self.anonymous_client.post(url)
    self.assertEqual(response.status_code, 403)

    response = self.anonymous_client.get(url)
    self.assertEqual(response.status_code, 405)

    response = self.linghu_client.post(url)
    self.assertEqual(response.status_code, 400)

    Friendship.objects.create(from_user=self.dongxie, to_user=self.linghu)
    count = Friendship.objects.count()
    response = self.dongxie_client.post()
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data['deleted'], 1)
    self.assertEqual(Friendship.objects.count(), count - 1)

    count = Friendship.objects.count()
    response = self.dongxie_client.post(url)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data['deleted'], 0)
    self.assertEqual(Friendship.objects.count(), count)

def test_followings(self):
    url = FOLLOWINGS_URL.format(self.dongxie.id)

    response = self.anonymous_client.post(url)
    self.assertEqual(response.status_code, 405)

    response = self.anonymous_client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data['followings']), 3)

    ts0 = response.data['followings'][0]['created_at']
    ts1 = response.data['followings'][1]['created_at']
    ts2 = response.data['followings'][2]['created_at']
    self.assertEqual(ts0 > ts1, True)
    self.assertEqual(ts1 > ts2, True)
    self.assertEqual(
        response.data['followings'][0]['user']['username'],
        'dongxie_following2',
    )
    self.assertEqual(
        response.data['followings'][1]['user']['username'],
        'dongxie_following1',
    )
    self.assertEqual(
        response.data['followings'][2]['user']['username'],
        'dongxie_following0',
    )

def test_followers(self):
    url = FOLLOWINGS_URL.format(self.dongxie.id)

    response = self.anonymous_client.post(url)
    self.assertEqual(response.status_code, 405)

    response = self.anonymous_client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data['followers']), 2)

    ts0 = response.data['followers'][0]['created_at']
    ts1 = response.data['followers'][1]['created_at']
    self.assertEqual(ts0 > ts1, True)
    self.assertEqual(
        response.data['followers']['user']['username'],
        'dongxie_follower1',
    )
    self.assertEqual(
        response.data['followers'][1]['user']['username'],
        'dongxie_follower0',
    )