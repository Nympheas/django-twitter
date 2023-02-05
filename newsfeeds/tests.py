from django.test import TestCase

# Create your tests here.
def test_list(self):
    response = self.anonymous_client.get(NEWSFEEDS_URL)
    self.assertEqual(response.status_code, 403)

    response = self.linghu_client.post(NEWSFEEDS_URL)
    self.assertEqual(response.status_code, 405)

    response = self.linghu_client.get(NEWSFEEDS_URL)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data['newsfeeds']), 0)

    self.linghu_client.post(POST_TWEETS_URL, {'content': 'HELLO World'})
    response = self.linghu_client.get(NEWSFEEDS_URL)
    self.assertEqual(len(response.data['newsfeeds']), 1)

    self.linghu_client.post(FOLLOW_URL.format(self.dongxie.id))
    response = self.dongxie_client.post(POST_TWEETS_URL, {
        'content': 'Hello Twitter',
    })
    posted_tweet_id = response.data['id']
    response = self.linghu_client.get(NEWSFEEDS_URL)
    self.assertEqual(len(response.data['newsfeeds']), 2)
    self.assertEqual(response.data['newsfeeds'][0]['tweet']['id'], posted_tweet_id)